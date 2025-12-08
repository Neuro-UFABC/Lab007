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

estimulo = 'chiadomuitolongoAudacity' #'varioscliques' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
est_path = f'../{estimulo}.wav'


with Carrinho(modo='eleva') as c: #modo='azimute'
    print(est_path)
    toca_grava(f'../chiado.wav', f'/tmp/lixo.wav') # TODO: o primeiro grava mal as vezes
    input("Pressione enter para gravar")
    c.anda_xy_mm(0, -1800)
    toca_grava(est_path, f'{quem}_{estimulo}_começoprofim.wav')
