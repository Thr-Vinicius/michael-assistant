#!/usr/bin/env bash

MICHAEL_HOME="${MICHAEL_HOME:-$HOME/.local/share/michael}"
STATE_DIR="$MICHAEL_HOME/state"
LOG_DIR="$MICHAEL_HOME/logs"
AUDIO_DIR="$MICHAEL_HOME/audio"

RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
MICHAEL_RUNTIME_DIR="$RUNTIME_DIR/michael"

mkdir -p "$STATE_DIR" "$LOG_DIR" "$AUDIO_DIR" "$MICHAEL_RUNTIME_DIR"

# Estado novo persistente
PAUSED_FILE="$STATE_DIR/paused"

# Estado temporário: some ao reiniciar o PC
WELCOME_LAST_FILE="$MICHAEL_RUNTIME_DIR/welcome_last"

# Estado antigo, mantido por compatibilidade
LEGACY_PAUSED="$HOME/.jarvis_paused"
LEGACY_WELCOME="$HOME/.michael_welcome_played"

WELCOME_AUDIO="${MICHAEL_WELCOME_AUDIO:-$AUDIO_DIR/boas_vindas_senhor_pronto_para_mais_um_dia.mp3}"
WELCOME_COOLDOWN_SECONDS="${MICHAEL_WELCOME_COOLDOWN_SECONDS:-3600}"

log_michael() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG_DIR/michael.log"
}

notify_basic() {
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "$@"
    fi
}

notify_cooldown() {
    local key="$1"
    local seconds="$2"
    local title="$3"
    local msg="$4"

    local file="$STATE_DIR/notify_${key}_last"
    local now
    local last

    now="$(date +%s)"
    last="0"

    if [[ -f "$file" ]]; then
        last="$(cat "$file" 2>/dev/null || echo 0)"
    fi

    if (( now - last >= seconds )); then
        notify_basic "$title" "$msg"
        echo "$now" > "$file"
        log_michael "notify: $title - $msg"
    fi
}

is_paused() {
    [[ -f "$PAUSED_FILE" || -f "$LEGACY_PAUSED" ]]
}

set_paused() {
    touch "$PAUSED_FILE" "$LEGACY_PAUSED"
}

clear_paused() {
    rm -f "$PAUSED_FILE" "$LEGACY_PAUSED"
}

welcome_should_play() {
    local now
    local last

    now="$(date +%s)"
    last="0"

    # LEGACY_WELCOME antigo não manda mais na regra.
    # Mantemos só para compatibilidade visual/status antigo, mas a regra nova é por sessão + 1h.
    if [[ -f "$WELCOME_LAST_FILE" ]]; then
        last="$(cat "$WELCOME_LAST_FILE" 2>/dev/null || echo 0)"
    fi

    (( now - last >= WELCOME_COOLDOWN_SECONDS ))
}

set_welcome_played() {
    date +%s > "$WELCOME_LAST_FILE"
    touch "$LEGACY_WELCOME"
}

welcome_played() {
    [[ -f "$WELCOME_LAST_FILE" ]]
}

welcome_seconds_left() {
    local now
    local last
    local left

    now="$(date +%s)"
    last="0"

    if [[ -f "$WELCOME_LAST_FILE" ]]; then
        last="$(cat "$WELCOME_LAST_FILE" 2>/dev/null || echo 0)"
    fi

    left=$(( WELCOME_COOLDOWN_SECONDS - (now - last) ))

    if (( left < 0 )); then
        echo 0
    else
        echo "$left"
    fi
}

play_audio() {
    local file="$1"

    [[ -f "$file" ]] || return 1

    if command -v mpv >/dev/null 2>&1; then
        mpv --no-terminal --really-quiet "$file" >/dev/null 2>&1 &
        return 0
    fi

    if command -v ffplay >/dev/null 2>&1; then
        ffplay -nodisp -autoexit -loglevel quiet "$file" >/dev/null 2>&1 &
        return 0
    fi

    if command -v paplay >/dev/null 2>&1; then
        paplay "$file" >/dev/null 2>&1 &
        return 0
    fi

    return 1
}

set_system_volume() {
    local volume="$1"

    if command -v wpctl >/dev/null 2>&1; then
        wpctl set-volume @DEFAULT_AUDIO_SINK@ "$volume" >/dev/null 2>&1 || true
        log_michael "volume ajustado para $volume via wpctl"
        return 0
    fi

    if command -v pactl >/dev/null 2>&1; then
        pactl set-sink-volume @DEFAULT_SINK@ "$volume" >/dev/null 2>&1 || true
        log_michael "volume ajustado para $volume via pactl"
        return 0
    fi

    if command -v amixer >/dev/null 2>&1; then
        amixer set Master "$volume" >/dev/null 2>&1 || true
        log_michael "volume ajustado para $volume via amixer"
        return 0
    fi

    log_michael "não foi possível ajustar volume: nenhum controlador encontrado"
    return 1
}
