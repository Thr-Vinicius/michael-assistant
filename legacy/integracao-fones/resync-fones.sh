#!/usr/bin/env bash
set -euo pipefail

LEFT_MAC="AA:BB:CC:DD:EE:01"
RIGHT_MAC="AA:BB:CC:DD:EE:02"

echo "Disconnecting headphones..."
bluetoothctl disconnect "$LEFT_MAC" || true
bluetoothctl disconnect "$RIGHT_MAC" || true

sleep 3

echo "Connecting headphones..."
bluetoothctl connect "$LEFT_MAC" || true
bluetoothctl connect "$RIGHT_MAC" || true

sleep 2

echo "Reapplying split stereo..."
"$HOME/split-fones.sh"


echo "Resuming playback..."

if command -v playerctl >/dev/null 2>&1; then
    playerctl play >/dev/null 2>&1 || true
elif command -v ydotool >/dev/null 2>&1; then
    ydotool key 57:1 57:0 >/dev/null 2>&1 || true
fi

echo "Done. Headphones resynced."
