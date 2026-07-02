#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time

import sounddevice as sd
import vosk

SETUP_PENDING_FILE = "/home/arthur/.michael_setup_pending"
PAUSE_FILE = "/home/arthur/.jarvis_paused"
MODEL_PATH = os.path.expanduser("~/vosk-model")

SAMPLERATE = 16000
BLOCKSIZE = 8000

if not os.path.exists(MODEL_PATH):
    print(f"Model not found at {MODEL_PATH}", file=sys.stderr)
    sys.exit(1)

print("Loading Vosk model...")
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLERATE)
recognizer.SetWords(True)


def run_music():
    if os.path.exists(PAUSE_FILE):
        subprocess.Popen(["notify-send", "Michael", "Estou pausado 💤"])
        return

    cmd = (
        "hyprctl dispatch exec \"[workspace 4 silent; no_initial_focus] "
        "/usr/bin/chromium --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod\""
    )

    print("Abrindo YouTube Music...")
    subprocess.Popen(["notify-send", "Michael", "Abrindo YouTube Music 🎵"])
    subprocess.run(cmd, shell=True, check=False)


def pause_michael():
    subprocess.Popen(["/home/arthur/.local/bin/michael-pausa"])


def resume_michael():
    subprocess.Popen(["/home/arthur/.local/bin/michael-voltar"])


def confirm_setup():
    if not os.path.exists(SETUP_PENDING_FILE):
        return

    if os.path.exists(PAUSE_FILE):
        subprocess.Popen(["notify-send", "Michael", "Estou pausado 💤"])
        return

    # Confirmação expira em 30 segundos
    if time.time() - os.path.getmtime(SETUP_PENDING_FILE) > 30:
        os.remove(SETUP_PENDING_FILE)
        subprocess.Popen(["notify-send", "Michael", "Confirmação expirada"])
        return

    os.remove(SETUP_PENDING_FILE)
    subprocess.Popen(["notify-send", "Michael", "Correto. Abrindo setup ✅"])
    subprocess.Popen(["/home/arthur/.local/bin/abrir-setup"])


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)

    audio_bytes = bytes(indata)

    if recognizer.AcceptWaveform(audio_bytes):
        result = json.loads(recognizer.Result())
        text = result.get("text", "").lower()
        print(f"Heard: {text}")

        if "michael voltar" in text or "michael ativar" in text:
            resume_michael()
            return

        if "michael pausa" in text or "michael pausar" in text:
            pause_michael()
            return

        if "correto" in text:
            confirm_setup()
            return

        if "michael musica" in text or "michael música" in text:
            run_music()
            return


def main():
    print("Ouvindo: 'Michael música', 'Michael pausa', 'Michael voltar' ou 'correto'...")
    try:
        with sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback,
        ):
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
