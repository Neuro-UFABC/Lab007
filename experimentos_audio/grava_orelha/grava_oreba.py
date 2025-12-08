import time
import os
import numpy as np

from audio007.audio_utils import grava_binaural, toca_grava
from audio007.carrinho import Carrinho

import sounddevice as sd
sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp

##############################################
### MUDAR PARAMETROS DO EXPERIMENTO ABAIXO ###
##############################################

modo = 'azimute' #'eleva'

estimulo = 'chiado_300_3000_silencio_75db'
#'chiadolongocliqueamp90_estereo' #'sweep_log_100_16k_10s_estereo' #'chiadolongocliqueamp90_filtrado100_15k.wav'  #'chiadolongoclique' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio' #'chiadolongocliqueamp45' #'chiadolongoclique' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'

angulos = range(-90,91,15)

########################################################
### em teoria, não precisa mudar nada daqui em diante ##
########################################################


quem = input('Nome do participante\n')
os.mkdir(quem)
os.chdir(quem)

est_path = f'../{estimulo}.wav'

with Carrinho(modo=modo) as c: 
    c.zera()
    toca_grava(est_path, f'{quem}_{estimulo}.wav') # TODO: o primeiro grava mal as vezes


    for ang in angulos:
        print(f'indo pro {modo}:', ang)
        px, py = c.anda_azim_mirado(ang)
        maxpasso =  np.max(np.abs([px,py]))
        print('esperando caixinha andar ', int(maxpasso) , ' passos')
        if c.modo == 'eleva':
            time.sleep(maxpasso/1600 + 0.5) 
        else: # azimute
            time.sleep(maxpasso/1600 + 0.5) #mudamos de 3200 pra 1600
        toca_grava(est_path, f'{quem}_{estimulo}_{ang}.wav')
