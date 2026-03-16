import os
import time
import sys
from random import choice
import numpy as np
from glob import glob
import soundfile as sf
from datetime import datetime

from audio007.audio_utils import filtra, _toca, nivel, ganho_normalizador, wavfile_pra_array
from audio007.apontador import Apontador


filtro = 'filtro_equalizacao_hd_mic_ind_48k.wav'
modo = 'azimute'
##################################################################

try:
    print('Usando dir', sys.argv[1])
    nome = sys.argv[1][:-1]
except:
    print('Informe um diretório válido contendo as gravações '
            'como parâmetro do programa. Ex:\n '
            '>python estima_dicoico.py XYZ11jan22/')
    sys.exit(1)

try:
    seqs = np.loadtxt(sys.argv[2])
    seq = choice(seqs) 
except IndexError:
    print('Forneça o nome do arquivo com a sequência como segundo argumento')
    sys.exit(1)
except FileNotFoundError:
    print(f'Não consegui ler sequência do arquivo {sys.argv[2]}')
    sys.exit(1)

print(f'## Estima Gaiola equilabrado com sequência {seq}')

# entra dir com gravações
os.chdir(nome)
zero, tx = sf.read(glob(f'*_0.wav')[0])

filtro = '../' + filtro
print(f'Lendo filtro de {filtro}')
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

    sons = [glob(f'*_{int(az)}.wav')[0] for az in seq]

    estimativas = np.zeros((len(sons),4), dtype=object)

    for i,som in enumerate(sons):
        print(f'[{i}/{len(sons)}]', end='')
        ang = som.split('_')[-1].split('.')[0]
        ga = [ganho, ganho]
        _toca(som, filtro=filtro, ganho=ga)
        a.espera_botao()
        estimativa = a.quantos_graus()
        dist = a.distancia()
        estimativas[i] = [int(ang), estimativa, dist, som]
        print(f'Verdadeiro:{ang}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}, {som}')

now = datetime.now()
time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 

np.savetxt(f'estimativas_dicoico_{nome}_{time_str}.csv', estimativas, delimiter=',', fmt='%g, %g, %g, %s', header='verdadeiro, estimado, distancia, estimulo')
