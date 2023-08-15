import time

from audio007.audio_utils import grava_binaural, toca_grava
from audio007.carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


with Carrinho() as c:

    azimutes =  [90, 45, 0, -45, -90]
    for i,p in enumerate(azimutes):
        c.anda_azim(p)
        time.sleep(10)
        toca_grava('estimulo.wav', f'{i}.wav')
