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

estimulo = 'chiado'#'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
est_path = f'../{estimulo}.wav'

with Carrinho(modo='azimute') as c:
    c.zera()
    toca_grava(est_path, f'{quem}_{estimulo}.wav') # TODO: o primeiro grava mal
    azimutes = [-90]

    for az in azimutes:
        px, py = c.anda_azim_mirado(az)
        time.sleep(np.max(np.abs([px,py]))/3200 + 0.5)
        toca_grava(est_path, f'{quem}_{estimulo}_{az}.wav')
