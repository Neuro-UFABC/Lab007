import os
import sys
from random import shuffle
import numpy as np
from glob import glob

from audio007.audio_utils import grava_binaural, toca_audio
from audio007.apontador import Apontador

print('Usando dir', sys.argv[1])
nome = sys.argv[1][:-1]
os.chdir(nome)

with Apontador() as a:
    a.calibra()

    repete = 1
    sons = repete * list(glob('*.wav')) 
    shuffle(sons)
    estimativas = np.zeros((len(sons),2))

    for i,som in enumerate(sons):
        az = som.split('_')[-1].split('.')[0]
        toca_audio(som)
        a.espera_botao()
        estimativa = a.quantos_graus()
        estimativas[i] = [az, estimativa]
        print(f'Verdadeiro:{az}, Estimado:{estimativa}')

np.savetxt(f'estimativas_dicoico_{nome}.csv', estimativas, delimiter=',', fmt='%g', header='verdadeiro, estimado')
