#!/usr/bin/env python3

import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata

import sounddevice as sd
import vosk

MODEL_PATH = os.path.expanduser("~/.local/share/michael/models/vosk")
MICHAEL_CMD = os.path.expanduser("~/.local/bin/michael-voice-command")
LOG_FILE = os.path.expanduser("~/.local/share/michael/logs/michael.log")
VOICE_LOCK_FILE = f"/run/user/{os.getuid()}/michael/voice.lock"
ACTIVATE_FILE = f"/run/user/{os.getuid()}/michael/activate_listen"
VOICE_LOCK_HANDLE = None

SAMPLERATE = 16000
BLOCKSIZE = 8000

ACTIVE_SECONDS = 5.0
EXTERNAL_ACTIVATION_COOLDOWN = 2.0
WAKE_VOLUME = "15%"

active_until = 0.0
last_external_activation_at = 0.0
saved_volume = None

LAST_TEXT = ""
LAST_AT = 0.0

WAKE_WORDS = {
    "michael",
    "maikel",
    "maicon",
    "mikel",
    "miguel",
    "michel",
    "miquel",
    "maiquel",
    "maicol",
    "maico",
}

COMMAND_KEYWORDS = {
    "musica",
    "music",
    "pausa",
    "pausar",
    "voltar",
    "ativar",
    "status",
    "estatus",
    "estados",
    "estado",
    "check",
    "verificar",
    "diagnostico",
    "teste",
    "ajuda",
    "comandos",
    "logs",
    "ultimos",
    "volume",
    "video",
    "videos",
    "muda",
    "trocar",
    "troca",
    "organizar",
    "organiza",
    "tempo",
    "clima",
    "previsao",
    "agenda",
    "calendario",
    "fone",
    "fones",
    "bluetooth",
    "resolver",
    "resync",
    "ressincronizar",
    "ressincroniza",
    "resincronizar",
    "resincroniza",
    "desligar",
    "encerrar",
}

ACTIVATION_AUDIO = os.environ.get(
    "MICHAEL_ACTIVATION_AUDIO",
    os.path.expanduser("~/.local/share/michael/audio/conf_1_som.mp3"),
)

CRITICAL_COMMANDS = {
    "desligar",
    "encerrar",
    "poweroff",
    "shutdown",
}

QUESTION_PREFIXES = (
    "como ",
    "por que ",
    "porque ",
    "o que ",
    "qual ",
    "quais ",
    "quando ",
    "onde ",
    "quem ",
)

FALLBACK_SOUNDS = [
    ACTIVATION_AUDIO,
    "/usr/share/sounds/freedesktop/stereo/message.oga",
    "/usr/share/sounds/freedesktop/stereo/complete.oga",
]


def acquire_single_instance_lock() -> None:
    global VOICE_LOCK_HANDLE

    os.makedirs(os.path.dirname(VOICE_LOCK_FILE), exist_ok=True)
    VOICE_LOCK_HANDLE = open(VOICE_LOCK_FILE, "w", encoding="utf-8")

    try:
        fcntl.flock(VOICE_LOCK_HANDLE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        VOICE_LOCK_HANDLE.write(str(os.getpid()))
        VOICE_LOCK_HANDLE.flush()
    except BlockingIOError:
        log("outro michael_voice.py já está rodando; encerrando instância duplicada")
        sys.exit(0)


def log(message: str) -> None:
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now}] voz: {message}\n")
    except Exception:
        pass


def notify(title: str, body: str) -> None:
    try:
        subprocess.Popen(
            ["notify-send", title, body],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def run_quiet(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )


def get_volume():
    if shutil.which("wpctl"):
        result = run_quiet(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"])
        match = re.search(r"([0-9]+(?:\.[0-9]+)?)", result.stdout)
        if match:
            return match.group(1)

    if shutil.which("pactl"):
        result = run_quiet(["pactl", "get-sink-volume", "@DEFAULT_SINK@"])
        match = re.search(r"(\d+)%", result.stdout)
        if match:
            return f"{int(match.group(1)) / 100:.2f}"

    return None


def set_volume(volume):
    if not volume:
        return

    if shutil.which("wpctl"):
        subprocess.Popen(
            ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", str(volume)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log(f"volume ajustado via wpctl para {volume}")
        return

    if shutil.which("pactl"):
        value = str(volume)
        if not value.endswith("%"):
            try:
                value = f"{round(float(value) * 100)}%"
            except Exception:
                pass

        subprocess.Popen(
            ["pactl", "set-sink-volume", "@DEFAULT_SINK@", value],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log(f"volume ajustado via pactl para {value}")


def lower_volume_for_listening():
    global saved_volume

    if saved_volume is None:
        saved_volume = get_volume()
        log(f"volume anterior salvo: {saved_volume}")

    set_volume(WAKE_VOLUME)


def restore_volume(reason=""):
    global saved_volume

    if saved_volume is None:
        return

    previous = saved_volume
    saved_volume = None
    set_volume(previous)
    log(f"volume restaurado para {previous}; motivo={reason}")


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.split())


def contains_wake(text: str) -> bool:
    words = set(text.split())
    return bool(words & WAKE_WORDS)


def has_command(text: str) -> bool:
    return any(cmd in text for cmd in COMMAND_KEYWORDS)


def is_critical_command(text: str) -> bool:
    return any(cmd in text for cmd in CRITICAL_COMMANDS)


def strip_leading_wake(text: str) -> str:
    parts = text.split(maxsplit=1)
    if parts and parts[0] in WAKE_WORDS:
        return parts[1] if len(parts) > 1 else ""
    return text


def looks_like_question(text: str) -> bool:
    body = strip_leading_wake(text)
    return any(body.startswith(prefix) for prefix in QUESTION_PREFIXES)


def play_activation_sound() -> None:
    for sound in dict.fromkeys(FALLBACK_SOUNDS):
        if not sound or not os.path.exists(sound):
            continue

        if shutil.which("mpv"):
            subprocess.Popen(
                ["mpv", "--no-terminal", "--really-quiet", sound],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log(f"som de ativação tocado: {sound}")
            return

        if shutil.which("ffplay"):
            subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", sound],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log(f"som de ativação tocado: {sound}")
            return

        if shutil.which("paplay"):
            subprocess.Popen(
                ["paplay", sound],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log(f"som de ativação tocado: {sound}")
            return

    log("nenhum som de ativação encontrado")


def route_text(text: str) -> None:
    try:
        env = os.environ.copy()
        env["MICHAEL_FROM_VOICE"] = "1"

        subprocess.Popen(
            [MICHAEL_CMD, text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
    except Exception as e:
        log(f"erro ao chamar roteador: {e}")

def should_ignore_duplicate(text: str) -> bool:
    global LAST_TEXT, LAST_AT

    now = time.time()

    if text == LAST_TEXT and now - LAST_AT < 1.5:
        return True

    LAST_TEXT = text
    LAST_AT = now
    return False


def handle_text(raw_text: str) -> None:
    global active_until

    text = normalize(raw_text)

    if not text:
        return

    log(f"ouvido: {text}")

    if should_ignore_duplicate(text):
        log(f"duplicado ignorado: {text}")
        return

    if looks_like_question(text):
        active_until = 0.0
        restore_volume("pergunta ignorada")
        log(f"pergunta ignorada para evitar ação acidental: {text}")
        return

    now = time.time()
    wake = contains_wake(text)
    command = has_command(text)
    critical = is_critical_command(text)
    active = now <= active_until

    # Exemplo: "Michael status" ou "Michael resolver"
    if wake and command:
        log(f"reconhecido direto: {text}")
        route_text(text)
        active_until = 0.0
        restore_volume("comando direto")
        return

    # Exemplo: "Michael"
    if wake and not command:
        active_until = now + ACTIVE_SECONDS
        log(f"ativação detectada; ouvindo por {ACTIVE_SECONDS:.0f}s")
        notify("Michael", "Estou ouvindo.")
        play_activation_sound()
        time.sleep(0.8)
        lower_volume_for_listening()
        return

    if active and command:
        log(f"reconhecido após ativação: {text}")
        active_until = 0.0
        restore_volume("comando após ativação")
        route_text(text)
        return

    # Michael 1.2: comandos só executam com wake word ou dentro da janela ativa.
    # Isso evita disparos acidentais quando o Vosk ouvir palavras soltas.
    if command:
        log(f"comando ignorado sem wake/ativação: {text}")
        return

    log(f"ignorado: {text} | wake={wake} command={command} active={active}")


def consume_external_activation():
    global active_until
    global last_external_activation_at

    if not os.path.exists(ACTIVATE_FILE):
        return

    try:
        os.remove(ACTIVATE_FILE)
    except FileNotFoundError:
        pass
    except Exception as e:
        log(f"erro removendo arquivo de ativação externa: {e}")

    now = time.time()

    if now - last_external_activation_at < EXTERNAL_ACTIVATION_COOLDOWN:
        log("ativação externa ignorada: debounce")
        return

    last_external_activation_at = now
    active_until = now + ACTIVE_SECONDS

    log(f"ativação externa detectada; ouvindo por {ACTIVE_SECONDS:.0f}s")
    notify("Michael", "Estou ouvindo.")
    play_activation_sound()
    time.sleep(0.5)
    lower_volume_for_listening()



def check_activation_timeout():
    global active_until

    if active_until and time.time() > active_until:
        active_until = 0.0
        restore_volume("timeout")


def audio_callback(indata, frames, time_info, status):
    if status:
        log(f"status áudio: {status}")

    audio_bytes = bytes(indata)

    if recognizer.AcceptWaveform(audio_bytes):
        try:
            result = json.loads(recognizer.Result())
        except Exception as e:
            log(f"erro lendo resultado Vosk: {e}")
            return

        handle_text(result.get("text", ""))


def main():
    if not os.path.exists(MODEL_PATH):
        log(f"modelo Vosk não encontrado em {MODEL_PATH}")
        notify("Michael", "Modelo Vosk não encontrado.")
        sys.exit(1)

    if not os.path.exists(MICHAEL_CMD):
        log(f"roteador não encontrado em {MICHAEL_CMD}")
        notify("Michael", "Roteador de voz não encontrado.")
        sys.exit(1)

    try:
        vosk.SetLogLevel(-1)

        global model
        global recognizer

        model = vosk.Model(MODEL_PATH)
        recognizer = vosk.KaldiRecognizer(model, SAMPLERATE)
        recognizer.SetWords(True)

        log("serviço de voz Michael iniciado")

        with sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback,
        ):
            while True:
                consume_external_activation()
                check_activation_timeout()
                sd.sleep(200)

    except KeyboardInterrupt:
        restore_volume("serviço parado")
        log("serviço de voz parado manualmente")
    except Exception as e:
        restore_volume("erro")
        log(f"erro no serviço de voz: {e}")
        notify("Michael", "Erro no serviço de voz. Veja os logs.")


if __name__ == "__main__":
    main()
