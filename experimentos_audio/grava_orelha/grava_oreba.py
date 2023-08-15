import time
import os
import numpy as np

from audio007.audio_utils import grava_binaural, toca_grava
from audio007.carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


quem = input('Nome do participante\n')
os.mkdir(quem)
os.chdir(quem)

with Carrinho() as c:
    c.zera()

    azimutes = range(-90,90,10)
    for az in azimutes:
        px, py = c.anda_azim(az)
        time.sleep(np.max(np.abs([px,py]))/3200 + 0.5)
        toca_grava('../burst500hz_silencio.wav', f'{quem}_{az}.wav')
