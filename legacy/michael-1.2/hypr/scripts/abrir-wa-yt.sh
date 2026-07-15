#!/bin/bash

WA_APP="/usr/bin/chromium --profile-directory=Default --app-id=hnpfjngllnobngcgfapefoaidbinmjnm"
YT_APP="/usr/bin/chromium --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod"

WA_CLASS="chrome-hnpfjngllnobngcgfapefoaidbinmjnm-Default"
YT_CLASS="chrome-cinhimbnkkaeohfgghhklpknlkffjgod-Default"

CURRENT_WS=$(hyprctl activeworkspace -j | jq -r '.id')

get_windows_by_class() {
    local class="$1"
    hyprctl clients -j | jq -r --arg class "$class" '.[] | select(.class == $class) | .address'
}

close_windows_by_class() {
    local class="$1"

    get_windows_by_class "$class" | while read -r addr; do
        if [ -n "$addr" ]; then
            hyprctl dispatch closewindow "address:$addr"
        fi
    done
}

wait_window() {
    local class="$1"

    for i in {1..80}; do
        addr=$(hyprctl clients -j | jq -r --arg class "$class" '.[] | select(.class == $class) | .address' | tail -n 1)

        if [ -n "$addr" ]; then
            echo "$addr"
            return 0
        fi

        sleep 0.1
    done

    return 1
}

apply_whatsapp_rules() {
    local addr="$1"

    hyprctl dispatch movetoworkspacesilent "5,address:$addr"
    hyprctl dispatch focuswindow "address:$addr"

    fullscreen=$(hyprctl clients -j | jq -r --arg addr "$addr" '.[] | select(.address == $addr) | .fullscreen')

    if [ "$fullscreen" != "0" ]; then
        hyprctl dispatch fullscreen 0
        sleep 0.2
    fi

    hyprctl dispatch setfloating
    sleep 0.2

    hyprctl dispatch resizeactive exact 1090 1130
    sleep 0.1

    hyprctl dispatch moveactive exact 80 35
}

apply_yt_rules() {
    local addr="$1"

    hyprctl dispatch movetoworkspacesilent "5,address:$addr"

    fullscreen=$(hyprctl clients -j | jq -r --arg addr "$addr" '.[] | select(.address == $addr) | .fullscreen')

    if [ "$fullscreen" != "0" ]; then
        hyprctl dispatch focuswindow "address:$addr"
        hyprctl dispatch fullscreen 0
        sleep 0.2
    fi

    hyprctl dispatch focuswindow "address:$addr"
    hyprctl dispatch setfloating
    sleep 0.2

    hyprctl dispatch resizeactive exact 700 1060
    sleep 0.1

    hyprctl dispatch moveactive exact 1190 70
}

# Fecha janelas antigas
close_windows_by_class "$WA_CLASS"
close_windows_by_class "$YT_CLASS"

sleep 1

# Abre WhatsApp
hyprctl dispatch exec "[workspace 5 silent; no_initial_focus] $WA_APP"

sleep 1

WA_ADDR=$(wait_window "$WA_CLASS")
if [ -n "$WA_ADDR" ]; then
    apply_whatsapp_rules "$WA_ADDR"
fi

# Abre YouTube Music
hyprctl dispatch exec "[workspace 5 silent; no_initial_focus] $YT_APP"

sleep 1

YT_ADDR=$(wait_window "$YT_CLASS")
if [ -n "$YT_ADDR" ]; then
    apply_yt_rules "$YT_ADDR"
fi

# Espera YouTube Music abrir/carregar
sleep 10

# Vai para o workspace do YouTube Music/WhatsApp
hyprctl dispatch workspace 5
sleep 0.5

# Foca diretamente o YouTube Music pelo endereço
if [ -n "$YT_ADDR" ]; then
    hyprctl dispatch focuswindow "address:$YT_ADDR"
fi

sleep 0.5

# Aperta espaço para dar play
ydotool key 57:1 57:0

sleep 0.5

# Volta para a workspace original
hyprctl dispatch workspace "$CURRENT_WS"
