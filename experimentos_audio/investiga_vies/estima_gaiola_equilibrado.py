import os
import sys
import time
import numpy as np
from random import choice
from datetime import datetime
from audio007.audio_utils import grava_binaural, toca_audio, ganho_normalizador
from audio007.carrinho import Carrinho
from audio007.apontador import Apontador

##############################################
### MUDAR PARAMETROS DO EXPERIMENTO ABAIXO ###
##############################################

modo = 'azimute'

estimulo = '5tons500HzRampaCos5ms48kHz.wav'
ref_normaliza = 'tom500Hz70dB_referencia_para_falante.wav'


########################################################
### em teoria, não precisa mudar nada daqui em diante ##
########################################################
try:
    seqs = np.loadtxt(sys.argv[1])
    seq = choice(seqs) 
except IndexError:
    print('Forneça o nome do arquivo com a sequência como primeiro argumento')
    sys.exit(1)
except:
    print(f'Não consegui ler sequência do arquivo {sys.argv[1]}')
    sys.exit(1)

gn = ganho_normalizador(estimulo, ref_normaliza)

print(f'## Estima Gaiola equilabrado com sequência {seq}')
nome = input('Nome do participante\n')


with Carrinho(modo=modo) as c:
    c.zera()

    with Apontador(modo=modo) as a:
        #a.calibra_linear()
        #time.sleep(0.5)
        a.calibra()
        time.sleep(0.5)
        
        print('### Aperte o botão para começar ###')
        a.espera_botao()
        time.sleep(0.5)
        
        estimativas = np.zeros((len(seq),2))
        
        lastAng = -90

        for i,ang in enumerate(seq):
            print(f'[{i+1}/{len(seq)}]', end='')

            vel = 3000 if modo == 'azimute' else 2000  # precisa calibrar...
            # pro falante não bater na cara do cara
            if lastAng >= 85 and ang == -90:
                px, py = c.anda_azim_mirado(-75)
                time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
            elif lastAng <= -85 and ang == 90:
                px, py = c.anda_azim_mirado(75)
                time.sleep(np.max(np.abs([px,py]))/vel + 0.5)

            lastAng = ang
            px, py = c.anda_azim_mirado(ang)
            
            time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
            toca_audio(estimulo, ganho=gn)

            a.espera_botao()
            estimativa = a.quantos_graus()
            #dist = a.distancia()
            
            estimativas[i] = [ang, estimativa]
            print(f'Verdadeiro: {round(ang)}, Estimado: {round(estimativa)}')

now = datetime.now()
time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 
np.savetxt(f'estimativas_gaiola_{nome}_{estimulo[:-4]}_{time_str}.csv', estimativas, delimiter=',', fmt='%g', header='verdadeiro, estimado')
