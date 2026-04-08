import os
import time
import sys
from random import choice, sample
import numpy as np
from glob import glob
from datetime import datetime
from pynput import keyboard
import sounddevice as sd

from audio007.audio_utils import filtra, _toca, nivel, ganho_normalizador, wavfile_pra_array
from audio007.apontador import Apontador
#from controlador_experimento import ControladorExperimento


modo = 'azimute'
##################################################################


def dicoico(sujeito, dir_ests, seqs, filtro, etapa=0, treino=False, calibra=False):    
    sd.default.device = ['sysdefault','sysdefault']  # TODO: cuidado, depende do comp
    seq = choice(np.loadtxt(seqs)) 
    print(f'## Estima Dicóico equilibrado com sequência {seq}')
    
    tx, ref_volume = wavfile_pra_array('tom500Hz70dB_referencia_para_fone.wav')
    
    tx, zero = wavfile_pra_array(glob(f'{dir_ests}/*_0.wav')[0])
    
    if filtro:
        tx, filtro_mic = wavfile_pra_array(filtro)
        zero = filtra(zero, filtro_mic)
    
    ganho = ganho_normalizador(zero, ref_volume, tx)
    
    
    #controlador = ControladorExperimento()
    sons = [glob(f'{dir_ests}/*_{int(az)}.wav')[0] for az in seq]
    resultados = np.zeros((len(sons),5), dtype=object)
    
    
    def trial(apontador, som, ganho, filtro):
        ang_real = som.split('_')[-1].split('.')[0]
    
        ga = [ganho, ganho]
        _toca(som, filtro=filtro, ganho=ga)
    
        t0 = time.perf_counter()
        apontador.espera_botao()
        tr = time.perf_counter() - t0
    
        estimativa = apontador.quantos_graus()
        print(f'Verdadeiro:{ang_real}, Estimado:{round(estimativa)}, {som}, tempo:{tr:.2f}\n')
        return ang_real, estimativa, tr
    
    
    with Apontador(modo) as a: 
        if calibra:
            a.calibra()
            time.sleep(0.5)
    
        print('### Aperte o botão para começar ###')
        a.espera_botao()
        time.sleep(0.5)
    
        #controlador.start()
    
        # trials de treino
        if treino:
            n_teste = 5
            for i,som in enumerate(sample(sons,n_teste)):
                #controlador.espera_se_pausado()
                print(f'[TESTE {i+1}/{n_teste}]', end='')
                ang, estimativa, tr = trial(a, som, ganho, filtro)
    
            print("\n### Treino finalizado ###")
            print("Explique a tarefa ao participante.")
            print("Pressione ENTER para iniciar a coleta.")
    
            #controlador.pausado = True
            #controlador.espera_se_pausado()
    
        # trials de verdade
        for i,som in enumerate(sons):
    
            #controlador.espera_se_pausado()
    
            print(f'[{i+1}/{len(sons)}]', end='')
                
            ang, estimativa, tr = trial(a, som, ganho, filtro)
            resultados[i] = [int(ang), estimativa, som, tr, filtro]
    
    
    now = datetime.now()
    time_str = now.strftime("%D__%H_%M_%S").replace('/','_') 
    
    os.makedirs(f'{sujeito}', exist_ok=True)
    np.savetxt(f'{sujeito}/estimativas_dicoico_etapa_{etapa}.csv', resultados, delimiter=',', fmt='%g, %g, %s, %g, %s', header='verdadeiro,estimado,estimulo,tempo resp,filtro', comments='')


if __name__ == '__main__':

    try:
        sujeito = sys.argv[1]
    except:
        print('Informe um diretório válido contendo as gravações '
                'como parâmetro do programa. Ex:\n '
                '>python estima_dicoico_equilibrado.py XYZ11jan22/ seq.txt comfiltro|semfiltro')
        sys.exit(1)
    
    try:
        dir_ests = sys.argv[2][:-1]
        print('Usando dir', sys.argv[2])
    except:
        print('Informe um diretório válido contendo as gravações '
                'como parâmetro do programa. Ex:\n '
                '>python estima_dicoico_equilibrado.py sujeito XYZ11jan22/ seq.txt comfiltro|semfiltro')
        sys.exit(1)
    
    try:
        seqs = sys.argv[3]
    except IndexError:
        print('Forneça o nome do arquivo com a sequência como segundo argumento:\n'
                '>python estima_dicoico_equilibrado.py sujeito XYZ11jan22/ seq.txt comfiltro|semfiltro')
        sys.exit(1)
    
    try:
        tem_filtro = sys.argv[4]
        if tem_filtro == 'comfiltro':
            filtro = '../filtro_equalizacao_hd_mic_ind_48k.wav' 
        elif tem_filtro == 'semfiltro':
            filtro = None
        else:
           raise IndexError 

    except IndexError:
        print('Diga "comfiltro" ou "semfiltro" como terceiro argumento!!')
        sys.exit(1)

    print('Estou assumindo etapa 0')
    dicoico(sujeito, dir_ests, seqs, filtro, etapa=0, treino=True)
