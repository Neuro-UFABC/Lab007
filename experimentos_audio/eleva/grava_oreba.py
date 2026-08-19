import time
import sys
import os
import numpy as np
from pathlib import Path
import sounddevice as sd

from audio007.audio_utils import _tocagrava, ganho_normalizador
from audio007.carrinho import Carrinho



def oreba(sujeito):
    sd.default.device = ['h6', 'sysdefault']  # TODO: cuidado, depende do comp
    #sd.default.device = ['sysdefault', 'sysdefault']  # TODO: cuidado, depende do comp
    sd.default.latency = [0.1, 0.1]

    modo = 'eleva' #'azimute' 
    
    estimulo1 = 'estalo80senos4_testerampa5ms' #'chiado_300_3000_silencio_70db_falantinho'    
    
    #angulos = range(-90,91,15)
    angulos = range(-75,76,30)
    
    ########################################################
    ### em teoria, não precisa mudar nada daqui em diante ##
    ########################################################
    
    
    dir_suj = Path(sujeito)
    dir_suj.mkdir(exist_ok=True)
    
    dir_gravacoes = Path(f'{dir_suj}/gravados')
    
    #os.chdir(dir_suj)
    dir_gravacoes.mkdir(exist_ok=True)
    
    est_path1 = f'./estimulos/{estimulo1}.wav'
    
    ref = './estimulos/oitentasenos_estereo.wav'
    gn1 = ganho_normalizador(est_path1, ref)
    
    with Carrinho(modo=modo) as c: 
        c.raio=650         #original=800
        
        c.espera(c.zera())  #pro raio velho de 800 mm
        time.sleep(1) # para conseguir apertar enter e ser o voluntario 
        c.espera(c.anda_mm('grande', +150)) # pro raio novo de 650 mm
        
        _tocagrava(est_path1, f'/tmp/lixo1.wav', ganho=gn1) # TODO: o primeiro grava mal as vezes
    
    
        for ang in angulos:
            print(f'indo pro {modo}:', ang)
            c.espera(c.anda_azim_mirado(ang))
            _tocagrava(est_path1, f'{dir_gravacoes}/{estimulo1}_{ang}.wav', ganho=gn1)

        print(f'indo pro {modo}:', -90)
        c.espera(c.anda_azim_mirado(-90))


if __name__ == '__main__':
    oreba(sys.argv[1])
