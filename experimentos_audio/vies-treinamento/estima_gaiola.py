import os
import sys
import time
import numpy as np
from random import shuffle
from datetime import datetime
from audio007.audio_utils import grava_binaural, toca_audio, ganho_normalizador
from audio007.carrinho import Carrinho
from audio007.apontador import Apontador


def gaiola(suj):
    modo = 'azimute'
    
    estimulo = '5tons500HzRampaCos5ms48kHz.wav'
    ref = 'burstcos-70dB.wav'
    
    gn = ganho_normalizador(estimulo, ref)
    
    ang_max = 90
    ang_min = -90
    ang_passo = 15
    repete = 1
    
    
    with Carrinho(modo=modo) as c:
        c.zera()
    
        with Apontador(modo=modo) as a:
            a.calibra()
            time.sleep(0.5)
            
            print('### Aperte o botão para começar ###')
            a.espera_botao()
            time.sleep(0.5)
            
            angulos =  repete * list(range(ang_min,ang_max+1,ang_passo))
            estimativas = np.zeros((len(angulos),3))
            
            shuffle(angulos)
                
            lastAng = -90
    
            for i,ang in enumerate(angulos):
                print(f'[{i+1}/{len(angulos)}]', end='')
    
                vel = 3000 if modo == 'azimute' else 2000  # precisa calibrar...
                # pro falante não bater no apontador
                if ((lastAng == 90 and ang == -90) or (lastAng == -90 and ang == 90)):
                    px, py = c.anda_azim_mirado(0)
                    time.sleep(np.max(np.abs([px,py]))/vel + 1.5)
    
                lastAng = ang
                px, py = c.anda_azim_mirado(ang)
                
                time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
                toca_audio(estimulo, ganho=gn)
    
                t0 = time.perf_counter()
                a.espera_botao()
                estimativa = a.quantos_graus()
                tr = time.perf_counter() - t0
                
                estimativas[i] = [ang, estimativa, tr]
                print(f'Verdadeiro: {round(ang)}, Estimado: {round(estimativa)}')
    
                print('Feche o olho e aperte o botão de novo pra ir pro próximo')
                time.sleep(0.5)
                a.espera_botao()
    
    now = datetime.now()
    time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 
    np.savetxt(f'{suj}/estimativas_gaiola_{estimulo[:-4]}_{time_str}.csv', estimativas, delimiter=',', fmt='%g', header='verdadeiro,estimado,tempo_resp', comments='')


if __name__ == '__main__':
    suj = sys.argv[1]
    gaiola(suj)
