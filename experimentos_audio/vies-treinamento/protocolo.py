import sys
from estima_dicoico_equilibrado import dicoico
from grava_oreba import oreba
from mostra_estimativas import mostra
from estima_gaiola import gaiola
from gera_estimulos import processa_sujeito

import sounddevice as sd

def refresh_devices():
    sd._terminate()
    sd._initialize()
    return sd.query_devices()

def limpa_tela():
    print("\033[H\033[J", end="")

sujeito = sys.argv[1]

######## 1 ############
print('Pluga o fone de ouvido na saída de áudio')
print('Liga o ponteiro e põe o fone no cara!')
input('Enter pra continuar')
dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=False, etapa=1)
limpa_tela()

######## 2 ############
print('Pluga o falante na saída de áudio')
print('Liga a fonte dos motores de passo')
print('Zera o falante da gaiola')
print('Liga a H6 e põe mics nas oreba do cara!')
input('Enter pra continuar')
refresh_devices()
oreba(sujeito)
limpa_tela()

######## 3 ############
print('Gerando estimulos a partir das gravações')
processa_sujeito(sujeito)
print('Chame o cara pra ver os gráficos')
mostra(sujeito)
limpa_tela()

######## 4 ############
print('Plugue o falante na saída de áudio')
print('Desplugue a h6')
print('Liga o ponteiro!')
print('Zera o falante da gaiola')
input('Enter pra continuar')
refresh_devices()
gaiola(sujeito)
limpa_tela()

######## 5 ############
print('Pluga o fone de ouvido na saída de áudio')
input('Enter pra continuar')
dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=2)
limpa_tela()

######## 6 ############
print('Chame o cara pra ver os gráficos')
mostra(sujeito)
limpa_tela()


######## 7 ############
print('Plugue o falante na saída de áudio')
print('Zera o falante da gaiola')
input('Enter pra continuar')
gaiola(sujeito)
limpa_tela()

######## 8 ############
print('Pluga o fone de ouvido na saída de áudio')
input('Enter pra continuar')
dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=3)
limpa_tela()


######## 9 ############
print('Chame o cara pra ver os gráficos')
mostra(sujeito)
limpa_tela()


######## 10 ############
print('Plugue o falante na saída de áudio')
print('Zera o falante da gaiola')
input('Enter pra continuar')
gaiola(sujeito)
limpa_tela()


######## 11 ############
print('Pluga o fone de ouvido na saída de áudio')
input('Enter pra continuar')
dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=False, etapa=4)
limpa_tela()


######## 12 ############
print('Chame o cara pra ver os gráficos')
mostra(sujeito)
limpa_tela()
