import os
import sys
import time
import numpy as np
from random import shuffle
from datetime import datetime
from audio007.audio_utils import grava_binaural, toca_audio
from audio007.carrinho import Carrinho
from audio007.apontador import Apontador

##############################################
### MUDAR PARAMETROS DO EXPERIMENTO ABAIXO ###
##############################################

modo = 'azimute' #'eleva'

estimulo = 'chiado_300_3000_silencio_75db.wav'

ang_min = -90
ang_max = 90
ang_passo = 45
repete = 1

########################################################
### em teoria, não precisa mudar nada daqui em diante ##
########################################################
nome = input('Nome do participante\n')


with Carrinho(modo=modo) as c:
    c.zera()

    with Apontador(modo=modo) as a:
        a.calibra_linear()
        time.sleep(0.5)
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

            vel = 3200 if modo == 'azim' else 2000  # precisa calibrar...
            # pro falante não bater no apontador
            if ((lastAng >= 45 and ang == -90) or (lastAng <= -45 and ang == 90)):
                px, py = c.anda_azim_mirado(0)
                time.sleep(np.max(np.abs([px,py]))/vel + 0.5)

            lastAng = ang
            px, py = c.anda_azim_mirado(ang)
            
            time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
            toca_audio(estimulo)

            a.espera_botao()
            estimativa = a.quantos_graus()
            dist = a.distancia()
            
            estimativas[i] = [ang, estimativa, dist]
            print(f'Verdadeiro: {ang}, Estimado: {estimativa}')

now = datetime.now()
time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 
np.savetxt(f'estimativas_gaiola_{nome}_{time_str}.csv', estimativas, delimiter=',', fmt='%g', header='verdadeiro, estimado, distancia')
