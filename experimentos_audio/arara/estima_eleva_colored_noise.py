from random import shuffle
import sys
import time
import numpy as np
from audio007.arara import Arara
from audio007.audio_utils import toca_audio
from audio007.apontador import Apontador
import colorednoise as cn

nome = sys.argv[1]

arara = Arara()
arara.desabilita_caixas()


with Apontador('eleva') as aponta:
    
    aponta.calibra_linear()
    time.sleep(0.5)
    aponta.calibra()
    time.sleep(0.5)

    print('### Aperte o botão para começar ###')
    aponta.espera_botao()
    time.sleep(0.5)
    

    repete = 1
    falantes = repete * list(range(1,8))
    #falantes = repete * np.ones(7)

    #betas = [-3, -2, -1, -1/2, 0, 1/2, 1] #colored noise exponent
    betas = np.linspace(-3,0,len(falantes)) #colored noise exponent
    shuffle(betas)
    #betas = np.ones(7)*(1/2)
    samples = 2**16
    audios = [cn.powerlaw_psd_gaussian(b, samples) for b in betas]
    
    
    shuffle(falantes)
    estimativas = np.zeros((len(falantes),4), dtype=object)
    for i,el in enumerate(falantes):
        print('Tentativa', i,)
        arara.habilita_caixa(el)
        #toca_audio('burst500hz.wav') #('chiadocurto.wav')
        #audio_idx = np.random.randint(0, len(betas), 1)[0]
        
        # toca som
        toca_audio(audios[i])
        time.sleep(0.5)

        # le resposta
        aponta.espera_botao()
        estimativa = aponta.quantos_graus()
        dist = aponta.distancia()
        verdadeiro = arara.angulo_falante(el)
        estimativas[i] = [verdadeiro, estimativa, dist, betas[i]]
        print(f'  Verdadeiro:{verdadeiro}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}, beta:{betas[i]}')

        # dá feedback
        passos_volta = 3200
        aponta.habilita_motor()
        time.sleep(0.5)
        precisa_andar = int((verdadeiro-estimativa)/360 * passos_volta)
        #print('vou andar', precisa_andar)
        aponta.anda(precisa_andar)
        time.sleep(abs(precisa_andar/1600)*4)
        aponta.desabilita_motor()

        arara.desabilita_caixas()

np.savetxt(f'estimativas_arara_{nome}.csv', estimativas, delimiter=',', fmt='%g, %g, %g, %g', header='verdadeiro, estimado, distancia, beta')
