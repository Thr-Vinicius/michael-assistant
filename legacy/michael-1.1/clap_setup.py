#!/usr/bin/env python3
import os
import subprocess
import time

import numpy as np
import sounddevice as sd

PAUSE_FILE = "/home/arthur/.jarvis_paused"

THRESHOLD = 1.5
RISE_THRESHOLD = 0.7
CLAP_GAP = 0.8
MIN_GAP_BETWEEN_CLAPS = 0.18
COOLDOWN = 20.0

last_volume = 0
last_clap = 0
last_action = 0


def callback(indata, frames, time_info, status):
    global last_volume, last_clap, last_action

    volume = float(np.max(np.abs(indata)))
    rise = volume - last_volume
    last_volume = volume
    now = time.time()

    if volume > THRESHOLD and rise > RISE_THRESHOLD:
        if now - last_action < COOLDOWN:
            return

        if now - last_clap < MIN_GAP_BETWEEN_CLAPS:
            return

        if now - last_clap <= CLAP_GAP:
            if os.path.exists(PAUSE_FILE):
                print("Michael pausado. Ignorando palmas/estalos.")
                subprocess.Popen(["notify-send", "Michael", "Estou pausado 💤"])
                last_clap = 0
                return

            print(f"👏👏 Duas palmas detectadas! volume={volume:.3f} rise={rise:.3f}")
            subprocess.Popen(["notify-send", "Michael", "Confirmação necessária 👏"])
            subprocess.Popen(["/home/arthur/.local/bin/michael-setup-request"])
            last_action = now
            last_clap = 0
        else:
            print(f"👏 Palma detectada: volume={volume:.3f} rise={rise:.3f}")
            last_clap = now


with sd.InputStream(callback=callback, channels=1, samplerate=44100):
    print("Ouvindo 2 palmas rápidas...")
    while True:
        time.sleep(1)
