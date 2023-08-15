import time

from audio007.audio_utils import grava_binaural, toca_grava
from audio007.carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


with Carrinho(modo='eleva') as c:
    c.zera() 
    elevas =  [-90, -45, 0, 45, 90]
    for i,e in enumerate(elevas):
        c.anda_eleva(e)
        time.sleep(10)
        toca_grava('estimulo.wav', f'{i}.wav')
