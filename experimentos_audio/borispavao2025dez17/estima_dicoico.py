import os
import time
import sys
from random import shuffle
import numpy as np
from glob import glob
import soundfile as sf
from datetime import datetime

from audio007.audio_utils import filtra, _toca, nivel, ganho_normalizador
from audio007.apontador import Apontador


filtro = '../filtro_equalizacao_hd_mic_ind.wav'
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


zero, tx = sf.read(glob(f'*_0.wav')[0])
filtro_mic, tx = sf.read(filtro)

zero_filtrado = filtra(zero, filtro_mic)
ganho = ganho_normalizador(zero_filtrado, zero, tx)


with Apontador(modo) as a: 
    a.calibra_linear()
    time.sleep(0.5)
    a.calibra()
    time.sleep(0.5)

    print('### Aperte o botão para começar ###')
    a.espera_botao()
    time.sleep(0.5)

    repete = 2 #4
    sons = repete * list(glob('*.wav')) 

    #sons_filtros = [(arq, f) for arq in sons for f in (None, filtro)]
    sons_filtros = [(arq, f) for arq in sons for f in (filtro, filtro)]


    shuffle(sons_filtros)
    estimativas = np.zeros((len(sons_filtros),5), dtype=object)

    for i,sf in enumerate(sons_filtros):
        som, fi = sf
        print(f'[{i}/{len(sons_filtros)}]', end='')
        ang = som.split('_')[-1].split('.')[0]
        if fi is None:
            ga = [1,1]
        else:
            ga = [ganho, ganho]
        _toca(som, filtro=fi, ganho=ga)
        a.espera_botao()
        estimativa = a.quantos_graus()
        dist = a.distancia()
        estimativas[i] = [int(ang), estimativa, dist, som, fi]
        print(f'Verdadeiro:{ang}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}, {som}, {fi}')

now = datetime.now()
time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 

np.savetxt(f'estimativas_dicoico_{nome}_{time_str}.csv', estimativas, delimiter=',', fmt='%g, %g, %g, %s, %s', header='verdadeiro, estimado, distancia, estimulo, filtro')
