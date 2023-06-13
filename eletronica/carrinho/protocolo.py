import time

from audio_utils import grava_binaural, toca_grava
from carrinho import Carrinho

with Carrinho() as c:
    c.sobe(1000)
    time.sleep(1)
    toca_grava('estimulo.wav', 'cima.wav')

    c.desce(1000)
    time.sleep(2)
    toca_grava('estimulo.wav', 'baixo.wav')
