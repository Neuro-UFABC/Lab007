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

estimulo = 'chiadolongocliqueamp90_estereo' #'varioscliques' #'chiadolongoclique' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
est_path = f'../{estimulo}.wav'


with Carrinho(modo='eleva') as c: #modo='azimute'
    c.zera()
    time.sleep(3) 
    toca_grava(est_path, f'/tmp/lixo.wav') # TODO: o primeiro grava mal as vezes
    px, py = c.anda_azim_mirado(45)
    maxpasso =  np.max(np.abs([px,py]))
    time.sleep(maxpasso/1600) 
    px, py = c.anda_diagonal(375) # estamos em raio = 800+375 = 1185
    maxpasso =  np.max(np.abs([px,py]))
    time.sleep(maxpasso/1600) 

    toca_grava(est_path, f'{quem}_{estimulo}_{c.raio}.wav')
    while c.raio >= 375:
        px, py = c.anda_diagonal(-585)
        print('indo pro raio:', c.raio)
        maxpasso =  np.max(np.abs([px,py]))
        print('esperando caixinha andar ', int(maxpasso) , ' passos')
        if c.modo == 'eleva':
            time.sleep(maxpasso/1600 + 0.5) #mudamos de 3200 pra 1600
        else: # azimute
            time.sleep(maxpasso/3200 + 0.5) 
        toca_grava(est_path, f'{quem}_{estimulo}_{c.raio}.wav')
