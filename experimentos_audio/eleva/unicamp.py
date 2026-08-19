from glob import glob
import sys
import os
from os.path import basename

from audio007.audio_utils import toca_grava

pessoa = sys.argv[-1]
os.mkdir(pessoa)
os.chdir(pessoa)

# faz diretorio com nome da pessoa e entra nele

for pos in ['alto', 'meio', 'baixo']:
    input(f'Mexa a caixa para posição {pos} e aperte qqer tecla...')
    for stim in glob('../estimulos/*.wav'):
        print(stim)
        toca_grava(stim, f'{pessoa}-{pos}-{basename(stim)}')
