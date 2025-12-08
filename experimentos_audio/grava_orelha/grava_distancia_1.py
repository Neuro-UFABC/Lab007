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

estimulo = 'chiadolongoclique' #'varioscliques' #'burst500hz_silencio' #'beep500hz_silencio' #'estalo_silencio'
est_path = f'../{estimulo}.wav'


with Carrinho(modo='eleva') as c: #modo='azimute'
    print(est_path)
    toca_grava(est_path, f'/tmp/lixo.wav') # TODO: o primeiro grava mal as vezes
    input("Pressione enter para gravar o próximo")
    toca_grava(est_path, f'{quem}_{estimulo}_começo.wav')
    c.anda_xy_mm(0, -800)
    input("Pressione enter para gravar o próximo")
    toca_grava(est_path, f'{quem}_{estimulo}_meio.wav')
    c.anda_xy_mm(0, -800)
    input("Pressione enter para gravar o próximo")
    toca_grava(est_path, f'{quem}_{estimulo}_fim.wav')
