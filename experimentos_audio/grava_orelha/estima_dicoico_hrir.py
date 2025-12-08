import os
import time
import sys
from random import shuffle
import numpy as np
from glob import glob
from scipy.io.wavfile import read

from audio007.audio_utils import grava_binaural, toca_audio
from audio007.apontador import Apontador

#modo ='eleva' #'azimute'
modo = 'azimute'

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
    #sons = repete * list(glob('*.wav')) 
    hrirs = repete * list(glob('./HRIR/*.wav'))
    #shuffle(sons)
    estimativas = np.zeros((len(hrirs),4), dtype=object)
    som = '../chiadolongo_estereo.wav'
    
    for i,hrir in enumerate(hrirs):
        print(f'[{i}/{len(hrirs)}]', end='')
        print('Lendo filtro do arquivo', hrir)
        ang = hrir.split('_')[-1].split('.')[0]
        _, filtro_hrir = read(hrir)
        toca_audio(som, filtro=filtro_hrir)
        a.espera_botao()
        estimativa = a.quantos_graus()
        dist = a.distancia()
        estimativas[i] = [int(ang), estimativa, dist, som]
        print(f'Verdadeiro:{ang}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}, {som}')

np.savetxt(f'estimativas_dicoico_hrir_{nome}.csv', estimativas, delimiter=',', fmt='%g, %g, %g, %s', header='verdadeiro, estimado, distancia, estimulo')
