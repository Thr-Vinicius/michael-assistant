#!/usr/bin/env bash

# Configuração base do Michael 2.0 Minimal Stable.
# Este arquivo é exemplo para o repositório.
# O config real do PC pode conter compatibilidades antigas.

MICHAEL_HOME="${MICHAEL_HOME:-$HOME/.local/share/michael}"
STATE_DIR="$MICHAEL_HOME/state"
LOG_DIR="$MICHAEL_HOME/logs"
AUDIO_DIR="$MICHAEL_HOME/audio"

RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
MICHAEL_RUNTIME_DIR="$RUNTIME_DIR/michael"

mkdir -p "$STATE_DIR" "$LOG_DIR" "$AUDIO_DIR" "$MICHAEL_RUNTIME_DIR"

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

    if [ -f "$file" ]; then
        last="$(cat "$file" 2>/dev/null || echo 0)"
    fi

    if [ "$((now - last))" -ge "$seconds" ]; then
        notify_basic "$title" "$msg"
        echo "$now" > "$file"
        log_michael "notify: $title - $msg"
    fi
}

apps_open() {
    if ! command -v hyprctl >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
        return 1
    fi

    hyprctl clients -j | jq -e '
        .[] | select(
            ((.class // "") | test("zen|zen-browser|chrome-cinhimbnkkaeohfgghhklpknlkffjgod-Default|chrome-hnpfjngllnobngcgfapefoaidbinmjnm-Default"; "i"))
            or
            ((.title // "") | test("Zen|WhatsApp"; "i"))
        )
    ' >/dev/null 2>&1
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
