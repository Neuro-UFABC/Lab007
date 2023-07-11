import sys
import time
from random import shuffle
from apontador import Apontador
from glob import glob
import pathlib
from datetime import datetime

import sounddevice as sd
from scipy.io.wavfile import read

n_repet = 2

def importa_sons(quem):
    print("Importando sons pra sujeito", quem)
    sons = glob(f'../sons/{quem}/*.wav')
    return sons

nome = " ".join(sys.argv[1:])
print('Experimento para sujeito', nome)

estimulos = importa_sons(nome) * n_repet
shuffle(estimulos)
print("Estímulos", estimulos)

def arquivo_para_angulo(nome):
    arq = pathlib.PurePath(nome).name
    return int(arq.split('.')[0].replace('m','-').replace('p','+'))

if __name__ == '__main__':

    estimativas = []
    def salva_dados():
        with open(f"{nome}.log", "a") as f:
            for som, angulo, com_fim in estimativas:
                f.write(f"{som},{angulo},{com_fim}\n")
    
    with Apontador() as a:
        print(a.calibra())
    
        for est in estimulos:
            print("### Esperando apertar botão para começar!")
            a.espera_botao()
            taxa_wav, dados = read(est)
            sd.play(dados, taxa_wav)
            sd.wait()
            print('angulo:', arquivo_para_angulo(est))
            print("### Aponte para a posição percebida")
            ts = str(datetime.now())
            
            print("### Esperando apertar botão para finalizar!")
            a.espera_botao()
            estimativa = a.quantos_graus()
            estimativas.append((
                pathlib.PurePath(est).name,
                estimativa,
                ts + ',' + str(datetime.now())))
            print("\tposição estimada:", estimativa)

            time.sleep(0.5)
    salva_dados()        
    

