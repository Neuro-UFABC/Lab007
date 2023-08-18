import time
from random import shuffle
import numpy as np

from audio007.audio_utils import grava_binaural, toca_audio
from audio007.carrinho import Carrinho
from audio007.apontador  import Apontador

nome = input('Nome do participante\n')

with Carrinho() as c:

    c.zera()

    with Apontador() as a:

        a.calibra()

        azimutes =  2 * list(range(-80,90,40))
        estimativas = np.zeros((len(azimutes),2))
        shuffle(azimutes)

        for i,az in enumerate(azimutes):
            print(az)
            px, py = c.anda_azim(az)
            time.sleep(np.max(np.abs([px,py]))/3200 + 0.5)
            toca_audio('burst500hz.wav')
            a.espera_botao()
            estimativa = a.quantos_graus()
            estimativas[i] = [az, estimativa]
            print(f'Verdadeiro:{az}, Estimado:{estimativa}')

np.savetxt(f'{nome}.csv', estimativas, delimiter=',', fmt='%g', header='azimute, estimativa')
