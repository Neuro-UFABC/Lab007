import time
import sys
import os
import numpy as np
from pathlib import Path

from audio007.audio_utils import _tocagrava, ganho_normalizador
from audio007.carrinho import Carrinho

import sounddevice as sd
sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp
sd.default.latency = [0.1, 0.1]


##############################################
### MUDAR PARAMETROS DO EXPERIMENTO ABAIXO ###
##############################################

modo = 'azimute' #'eleva'

estimulo1 = '5tons500HzRampaCos5ms48kHz'
estimulo2 = '2tons0ms'

angulos = range(-90,91,15)

########################################################
### em teoria, não precisa mudar nada daqui em diante ##
########################################################


dir_suj = Path(sys.argv[1])
dir_suj.mkdir(exist_ok=True)

dir_estima = Path('para_estimar_ITD_ILD')
dir_gravacoes = Path('gravados')

os.chdir(dir_suj)
dir_estima.mkdir(exist_ok=True)
dir_gravacoes.mkdir(exist_ok=True)

est_path1 = f'../{estimulo1}.wav'
est_path2 = f'../{estimulo2}.wav'

ref = '../burstcos-70dB.wav'
gn1 = ganho_normalizador(est_path1, ref)
gn2 = ganho_normalizador(est_path2, ref)

with Carrinho(modo=modo) as c: 
    c.zera()
    time.sleep(5) # para conseguir apertar enter e ser o voluntario 
    _tocagrava(est_path1, f'/tmp/lixo1.wav', ganho=gn1) # TODO: o primeiro grava mal as vezes


    for ang in angulos:
        print(f'indo pro {modo}:', ang)
        px, py = c.anda_azim_mirado(ang)
        maxpasso =  np.max(np.abs([px,py]))
        print('esperando caixinha andar ', int(maxpasso) , ' passos')
        if c.modo == 'eleva':
            time.sleep(maxpasso/1600 + 0.5) 
        else: # azimute
            time.sleep(maxpasso/1600 + 0.5) #mudamos de 3200 pra 1600
        _tocagrava(est_path1, f'{dir_gravacoes}/{estimulo1}_{ang}.wav', ganho=gn1)
        _tocagrava(est_path2, f'{dir_estima}/{estimulo2}_{ang}.wav', ganho=gn2)
