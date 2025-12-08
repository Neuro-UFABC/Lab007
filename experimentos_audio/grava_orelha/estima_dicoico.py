import os
import time
import sys
from random import shuffle
import numpy as np
from glob import glob
from scipy.io.wavfile import read

from audio007.audio_utils import grava_binaural, toca_audio
from audio007.apontador import Apontador

#_, filtro_mic = read('filtroSandro06jun2024.wav')
#_, filtro_mic = read('filtro_eq_hp_mic.wav')

filtro_mic = None
modo = 'azimute' #'eleva'
ganho = 1

##################################################################

try:
    print('Usando dir', sys.argv[1])
    nome = sys.argv[1][:-1]
    os.chdir(nome)
except:
    print('Informe um diretório válido contendo as gravações '
            'como parâmetro do programa. Ex:\n '
            '>python estima_dicoico.py XYZ11jan22/')
    sys.exit(1)


with Apontador(modo) as a: #'azimute' ou 'eleva'
    a.calibra_linear()
    time.sleep(0.5)
    a.calibra()
    time.sleep(0.5)

    print('### Aperte o botão para começar ###')
    a.espera_botao()
    time.sleep(0.5)

    repete = 2
    sons = repete * list(glob('*.wav')) 
    shuffle(sons)
    estimativas = np.zeros((len(sons),4), dtype=object)

    for i,som in enumerate(sons):
        print(f'[{i}/{len(sons)}]', end='')
        ang = som.split('_')[-1].split('.')[0]
        if filtro_mic is not None:
            print('Usando filtro!')
            toca_audio(som, filtro=filtro_mic)
        else:
            toca_audio(som, ganho=ganho)
        a.espera_botao()
        estimativa = a.quantos_graus()
        dist = a.distancia()
        estimativas[i] = [int(ang), estimativa, dist, som]
        print(f'Verdadeiro:{ang}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}, {som}')

np.savetxt(f'estimativas_dicoico_{nome}.csv', estimativas, delimiter=',', fmt='%g, %g, %g, %s', header='verdadeiro, estimado, distancia, estimulo')
