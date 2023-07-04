import time

from audio_utils import grava_binaural, toca_grava
from carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


with Carrinho() as c:

    posicoes =  [51, 440, 336, 354, 454]
    for i,p in enumerate(posicoes):
        c.sobe_mm(p)
        time.sleep(15)
        toca_grava('estimulo.wav', f'{i}.wav')
