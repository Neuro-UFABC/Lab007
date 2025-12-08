import os
import sys
import time
import numpy as np
from random import shuffle
from collections import Counter
from audio007.audio_utils import grava_binaural, toca_audio
from audio007.carrinho import Carrinho
from audio007.apontador import Apontador

##############################################
### MUDAR PARAMETROS DO EXPERIMENTO ABAIXO ###
##############################################

modo = 'azimute' #'eleva'

estimulo = 'chiadolongocliqueamp90_estereo_fastonset.wav' #'chiadolongocliqueamp90_estereo_slowonset.wav'

ang_min = -90
ang_max = 90
ang_passo = 15
repete = 5

########################################################
### em teoria, não precisa mudar nada daqui em diante ##
########################################################
nome = input('Nome do participante\n')

# Verifica se existe um arquivo de interrupção anterior
arquivo_interrompido = f'estimativas_freefield_{nome}_interrompida.csv'
sons_apresentados = set()
dados_previos = None
if os.path.exists(arquivo_interrompido):
    print('Recuperando experimento interrompido...')
    dados_previos = np.genfromtxt(arquivo_interrompido, delimiter=',', skip_header=1)
    if dados_previos.size > 0:
        angulos_apresentados = {int(ang) for ang in dados_previos[:, 0]}  # Captura os ângulos dos sons já apresentados

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
        
        if dados_previos is not None and dados_previos.size > 0:
            counter1 = Counter(angulos_apresentados)
            counter2 = Counter(angulos)
            result_counter = counter2 - counter1
            angulos = list(result_counter.elements())
            shuffle(angulos)
            print(angulos)
            
        estimativas = np.zeros((len(angulos), 3))
        sons = repete * [estimulo] * len(angulos)
        shuffle(sons)
        
        lastAng  = 0

        for i,ang in enumerate(angulos):
            print(f'[{i+1}/{len(angulos)}]', end='')
            if ((lastAng >= 45 and ang == -90) or (lastAng <= -45 and ang == 90)):
                px, py = c.anda_azim_mirado(0)
                time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
            lastAng = ang
            px, py = c.anda_azim_mirado(ang)
            
            vel = 3200 if modo == 'azim' else 2000  # precisa calibrar...
            time.sleep(np.max(np.abs([px,py]))/vel + 0.5)
            toca_audio(sons[i]),
            a.espera_botao()
            estimativa = a.quantos_graus()
            dist = a.distancia()
            
            # Se a estimativa estiver fora da faixa aceitável, interrompe e salva os dados parciais
            if not (-100 <= estimativa <= 100):
                print('Estimativa fora do intervalo (-100 a 100). Interrompendo experimento...')
                parcial = estimativas[:i] # Mantém apenas os dados coletados até o erro
                # Se houver dados prévios carregados, adicionamos aos novos dados
                if dados_previos is not None and dados_previos.size > 0:
                    parcial = np.vstack((dados_previos, parcial))
                # Salva todos os dados no arquivo de interrupção
                np.savetxt(arquivo_interrompido, parcial, delimiter=',', fmt='%g', header='verdadeiro, estimado, distancia')
                sys.exit(1) # Sai do script
            
            estimativas[i] = [ang, estimativa, dist]
            print(f'Verdadeiro: {ang}, Estimado: {estimativa}')

np.savetxt(f'estimativas_freefield_{nome}.csv', estimativas, delimiter=',', fmt='%g', header='verdadeiro, estimado, distancia')
