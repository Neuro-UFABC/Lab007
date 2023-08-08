import time

from audio_utils import grava_binaural, toca_grava
from carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


with Carrinho(modo='eleva') as c:
    c.zera() 
    azimutes =  [-90, -45, 0, 45, 90]
    for i,p in enumerate(azimutes):
        c.anda_azim(p)
        time.sleep(10)
        toca_grava('estimulo.wav', f'{i}.wav')
