import time
import os
import numpy as np

from audio007.audio_utils import grava_binaural, toca_grava
from audio007.carrinho import Carrinho

import sounddevice as sd

sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp


quem = input('Nome do participante\n')
os.mkdir(quem)
os.chdir(quem)

estimulo = 'chiadolongocliqueamp90' #'chiadolongoclique' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
#estimulo = 'chiadolongocliqueamp45' #'chiadolongoclique' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
est_path = f'../{estimulo}.wav'

with Carrinho(modo='azimute') as c:  #modo='azimute' modo='eleva'
    c.zera()
    toca_grava(est_path, f'{quem}_{estimulo}.wav') # TODO: o primeiro grava mal as vezes

    azimutes = range(0,2,1)

    for az in azimutes:
        print('indo pro ponto:', az)
        px = 70
        c.anda_xy_mm(0, px)
        maxpasso =  np.abs(px)
        print('esperando caixinha andar ', int(maxpasso) , ' passos')
        if c.modo == 'eleva':
            time.sleep(maxpasso/1600 + 0.5) 
        else: # azimute
            time.sleep(maxpasso/1600 + 0.5) #mudamos de 3200 pra 1600
        toca_grava(est_path, f'{quem}_{estimulo}_{az}.wav')
