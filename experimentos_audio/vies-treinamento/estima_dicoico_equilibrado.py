import os
import time
import sys
from random import choice
import numpy as np
from glob import glob
from datetime import datetime
from pynput import keyboard

from audio007.audio_utils import filtra, _toca, nivel, ganho_normalizador, wavfile_pra_array
from audio007.apontador import Apontador
from controlador_experimento import ControladorExperimento


modo = 'azimute'
##################################################################

try:
    print('Usando dir', sys.argv[1])
    nome = sys.argv[1][:-1]
except:
    print('Informe um diretório válido contendo as gravações '
            'como parâmetro do programa. Ex:\n '
            '>python estima_dicoico_equilibrado.py XYZ11jan22/ seq.txt comfiltro|semfiltro')
    sys.exit(1)

try:
    seqs = np.loadtxt(sys.argv[2])
    seq = choice(seqs) 
except IndexError:
    print('Forneça o nome do arquivo com a sequência como segundo argumento:\n'
            '>python estima_dicoico_equilibrado.py XYZ11jan22/ seq.txt comfiltro|semfiltro')
    sys.exit(1)
except FileNotFoundError:
    print(f'Não consegui ler sequência do arquivo {sys.argv[2]}. Ex:\n'
           '>python estima_dicoico_equilibrado.py XYZ11jan22/ seq.txt comfiltro|semfiltro')
    sys.exit(1)

try:
    tem_filtro = sys.argv[3]
    if tem_filtro == 'comfiltro':
        filtro = '../filtro_equalizacao_hd_mic_ind_48k.wav' 
    elif tem_filtro == 'semfiltro':
        filtro = None
    else:
       raise IndexError 
except IndexError:
    print('Diga "comfiltro" ou "semfiltro" como terceiro argumento!!')
    sys.exit(1)

    

print(f'## Estima Gaiola equilabrado com sequência {seq}')

tx, ref_volume = wavfile_pra_array('tom500Hz70dB_referencia_para_fone.wav')

# entra dir com gravações
os.chdir(nome)

tx, zero = wavfile_pra_array(glob('*_0.wav')[0])

if filtro:
    tx, filtro_mic = wavfile_pra_array(filtro)
    zero = filtra(zero, filtro_mic)

ganho = ganho_normalizador(zero, ref_volume, tx)


controlador = ControladorExperimento()
sons = [glob(f'*_{int(az)}.wav')[0] for az in seq]
estimativas = np.zeros((len(sons),4), dtype=object)

with Apontador(modo) as a: 
    #a.calibra_linear()
    #time.sleep(0.5)
    a.calibra()
    time.sleep(0.5)

    print('### Aperte o botão para começar ###')
    a.espera_botao()
    time.sleep(0.5)

    controlador.start()
    for i,som in enumerate(sons):

        controlador.espera_se_pausado()

        print(f'[{i+1}/{len(sons)}]', end='')
        ang = som.split('_')[-1].split('.')[0]
        ga = [ganho, ganho]
        _toca(som, filtro=filtro, ganho=ga)
        a.espera_botao()
        estimativa = a.quantos_graus()
        #dist = a.distancia()
        estimativas[i] = [int(ang), estimativa, som, filtro]
        print(f'Verdadeiro:{ang}, Estimado:{round(estimativa)}, {som}\n')

now = datetime.now()
time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 

np.savetxt(f'estimativas_dicoico_{nome}_{time_str}.csv', estimativas, delimiter=',', fmt='%g, %g, %s, %s', header='verdadeiro, estimado, estimulo, filtro')
