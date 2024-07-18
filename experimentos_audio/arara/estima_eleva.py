from random import shuffle
import sys
import time
import numpy as np
from audio007.arara import Arara
from audio007.audio_utils import toca_audio
from audio007.apontador import Apontador

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
    elevas = repete * list(range(1,8))
    shuffle(elevas)
    estimativas = np.zeros((len(elevas),3), dtype=object)
    for i,el in enumerate(elevas):
        arara.habilita_caixa(el)
        toca_audio('burst500hz.wav') #('chiadocurto.wav')
        time.sleep(0.5)
        aponta.espera_botao()
        estimativa = aponta.quantos_graus()
        dist = aponta.distancia()
        estimativas[i] = [int(el), estimativa, dist]
        print(f'Verdadeiro:{el}, Estimado:{round(estimativa)}, Distancia:{round(dist,2)}')
        arara.desabilita_caixas()

np.savetxt(f'estimativas_arara_{nome}.csv', estimativas, delimiter=',', fmt='%g, %g, %g', header='verdadeiro, estimado, distancia')
