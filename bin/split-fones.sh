#!/usr/bin/env bash
set -euo pipefail

# Split stereo audio between two Bluetooth headphones using PipeWire.
# Left channel goes to one headphone, right channel goes to another.

LEFT_DEVICE="bluez_output.41_42_FF_D2_DA_FB.1"
RIGHT_DEVICE="bluez_output.41_42_FF_89_D2_08.1"
VIRTUAL_SINK="split_lr"

# Volume-base dos dois fones físicos.
# Depois disso, o volume normal do sistema deve controlar o split_lr.
PHYSICAL_VOLUME="${MICHAEL_FONES_PHYSICAL_VOLUME:-99%}"
VIRTUAL_VOLUME="${MICHAEL_FONES_VIRTUAL_VOLUME:-40%}"

echo "Checking Bluetooth devices..."

if ! pactl list short sinks | grep -q "$LEFT_DEVICE"; then
    echo "Left device not found: $LEFT_DEVICE"
    echo "Connect both Bluetooth headphones and try again."
    exit 1
fi

if ! pactl list short sinks | grep -q "$RIGHT_DEVICE"; then
    echo "Right device not found: $RIGHT_DEVICE"
    echo "Connect both Bluetooth headphones and try again."
    exit 1
fi

echo "Checking virtual sink..."

if ! pactl list short sinks | grep -q "$VIRTUAL_SINK"; then
    echo "Creating virtual sink: $VIRTUAL_SINK"

    pactl load-module module-null-sink \
        sink_name="$VIRTUAL_SINK" \
        channels=2 \
        channel_map=front-left,front-right \
        sink_properties=device.description="Bluetooth L/R Split"
fi

sync_volumes() {
    echo "Syncing headphone volumes..."

    pactl set-sink-mute "$LEFT_DEVICE" 0 || true
    pactl set-sink-mute "$RIGHT_DEVICE" 0 || true
    pactl set-sink-mute "$VIRTUAL_SINK" 0 || true

    pactl set-sink-volume "$LEFT_DEVICE" "$PHYSICAL_VOLUME" || true
    pactl set-sink-volume "$RIGHT_DEVICE" "$PHYSICAL_VOLUME" || true
    pactl set-sink-volume "$VIRTUAL_SINK" "$VIRTUAL_VOLUME" || true

    pactl set-default-sink "$VIRTUAL_SINK" || true
}

echo "Setting default sink to $VIRTUAL_SINK..."
pactl set-default-sink "$VIRTUAL_SINK"

echo "Removing old links..."

pw-link -d "$VIRTUAL_SINK:monitor_FL" "$LEFT_DEVICE:playback_FL" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FL" "$LEFT_DEVICE:playback_FR" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FR" "$RIGHT_DEVICE:playback_FL" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FR" "$RIGHT_DEVICE:playback_FR" 2>/dev/null || true

pw-link -d "$VIRTUAL_SINK:monitor_FL" "$RIGHT_DEVICE:playback_FL" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FL" "$RIGHT_DEVICE:playback_FR" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FR" "$LEFT_DEVICE:playback_FL" 2>/dev/null || true
pw-link -d "$VIRTUAL_SINK:monitor_FR" "$LEFT_DEVICE:playback_FR" 2>/dev/null || true

echo "Connecting left channel..."
pw-link "$VIRTUAL_SINK:monitor_FL" "$LEFT_DEVICE:playback_FL"
pw-link "$VIRTUAL_SINK:monitor_FL" "$LEFT_DEVICE:playback_FR"

echo "Connecting right channel..."
pw-link "$VIRTUAL_SINK:monitor_FR" "$RIGHT_DEVICE:playback_FL"
pw-link "$VIRTUAL_SINK:monitor_FR" "$RIGHT_DEVICE:playback_FR"

sync_volumes

echo "Done. Bluetooth split stereo is active."
