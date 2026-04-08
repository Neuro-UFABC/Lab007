import sys
from estima_dicoico_equilibrado import dicoico
from grava_oreba import oreba
from mostra_estimativas import mostra
from estima_gaiola import gaiola
from gera_estimulos import processa_sujeito

import sounddevice as sd
import time

def refresh_devices():
    sd._terminate()
    sd._initialize()
    return sd.query_devices()

def limpa_tela():
    print("\033[H\033[J", end="")

sujeito = sys.argv[1]

print('######### 1 - Estima dicóico ############')
print('Liga o apontador na USB')
print('Pluga o fone de ouvido na saída de áudio')
print('Posiciona o voluntário, mostra fone e apontador')
print('')
print('Instruções: “Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante a')
print('            execução da tarefa. As primeiras 5 tentativas são só pra treinar,')
print('            depois começa de verdade.”')
print('')
input('Enter pra continuar')
try:
    #dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=True, etapa=1)
    dicoico(sujeito, 'diamante/', 'sequencias.txt', filtro=None, treino=True, etapa=1)
except:
    input('Problema! Aperte enter pra tentar de novo')
    #dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=True, etapa=1)
    dicoico(sujeito, 'diamante/', 'sequencias.txt', filtro=None, treino=True, etapa=1)
limpa_tela()

print('#########  2 - Grava oreba ############')
print('Liga a fonte dos motores de passo')
print('Liga a H6 na USB e põe os microfones na orelha')
print('Pluga o falante na saída de áudio')
print('Zera o falante da gaiola')
print('')
print('Instruções: “Vamos gravar como os sons chegam na sua orelha. Mantenha a cabeça fixa')
print('            olhos abertos olhando sempre para o ponto de fixação.”')
print('')
time.sleep(0.5)
input('Enter pra continuar')
try:
    refresh_devices()
    input('Enter pra continuar')
    refresh_devices()
    time.sleep(1)
    oreba(sujeito)
except:
    input('Problema! Aperte enter pra tentar de novo')
    refresh_devices()
    time.sleep(0.5)
    oreba(sujeito)
print('Gerando estímulos a partir das gravações')
processa_sujeito(sujeito)
limpa_tela()

print('#########  3 - Mostra os dados pro voluntário ############')
print('Chama o voluntário pra ver os gráficos.')
print('')
print('Instruções: “Esse é o gráfico das média das estimativas em função dos azimutes. Se')
print('            as estimativas desviaram da linha preta, faça com mais cuidado. Serão')
print('            apresentados todos os azimutes com mesma frequência, de -90 a 90.”')
print('')
mostra(sujeito)
limpa_tela()

print('######### 4 - Estima gaiola ############')
print('Liga o apontador na USB')
print('Zera o falante da gaiola')
print('')
print('Instruções: “Você ouvirá sons do falante, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o')
print('            botão. Em seguida, abra os olhos para ver onde o falante realmente está.')
print('            Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”')
print('')
input('Enter pra continuar')
try:
    refresh_devices()
    gaiola(sujeito)
except:
    input('Problema! Aperte enter pra tentar de novo')
    refresh_devices()
    gaiola(sujeito)
limpa_tela()

print('######### 5 - Estima dicóico ############')
print('Pluga o fone de ouvido na saída de áudio')
print('')
print('Instruções: “Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante a')
print('            execução da tarefa.”')
print('')
input('Enter pra continuar')
try:
    dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=2)
except:
    input('Problema! Aperte enter pra tentar de novo')
    dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=2)
limpa_tela()

print('#########  6 - Mostra os dados pro voluntário ############')
print('Chama o cara pra ver os gráficos')
print('')
print('Instruções: “Esse é o gráfico das média das estimativas em função dos azimutes. Se')
print('            as estimativas desviaram da linha preta, faça com mais cuidado. Serão')
print('            apresentados todos os azimutes com mesma frequência, de -90 a 90.”')
print('')
mostra(sujeito)
limpa_tela()


print('######### 7 - Estima gaiola ############')
print('Pluga o falante na saída de áudio')
print('Zera o falante da gaiola')
print('')
print('Instruções: “Você ouvirá sons do falante, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o')
print('            botão. Em seguida, abra os olhos para ver onde o falante realmente está.')
print('            Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”')
input('Enter pra continuar')
try:
    gaiola(sujeito)
except:
    input('Problema! Aperte enter pra tentar de novo')
    gaiola(sujeito)
limpa_tela()

print('######### 8 - Estima dicóico ############')
print('Pluga o fone de ouvido na saída de áudio')
print('')
print('Instruções: “Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante a')
print('            execução da tarefa.”')
print('')
input('Enter pra continuar')
try:
    dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=3)
except:
    input('Problema! Aperte enter pra tentar de novo')
    dicoico(sujeito, f'{sujeito}/sintetico_naomanipulado/', 'sequencias.txt', filtro=None, treino=False, etapa=3)
limpa_tela()


print('#########  9 - Mostra os dados pro voluntário ############')
print('Chama o cara pra ver os gráficos')
print('')
print('Instruções: “Esse é o gráfico das média das estimativas em função dos azimutes. Se')
print('            as estimativas desviaram da linha preta, faça com mais cuidado. Serão')
print('            apresentados todos os azimutes com mesma frequência, de -90 a 90.”')
print('')
mostra(sujeito)
limpa_tela()


print('######### 10 - Estima gaiola ############')
print('Pluga o falante na saída de áudio')
print('Zera o falante da gaiola')
print('')
print('Instruções: “Você ouvirá sons do falante, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o')
print('            botão. Em seguida, abra os olhos para ver onde o falante realmente está.')
print('            Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”')
input('Enter pra continuar')
try:
    gaiola(sujeito)
except:
    input('Problema! Aperte enter pra tentar de novo')
    gaiola(sujeito)
limpa_tela()


print('######### 11 - Estima dicóico ############')
print('Pluga o fone de ouvido na saída de áudio')
print('')
print('Instruções: “Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e')
print('            aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante a')
print('            execução da tarefa.”')
print('')
input('Enter pra continuar')
try:
    #dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=False, etapa=4)
    dicoico(sujeito, 'diamante/', 'sequencias.txt', filtro=None, treino=True, etapa=4)
except:
    input('Problema! Aperte enter pra tentar de novo')
    #dicoico(sujeito, 'sintetico_variaITD_ILDzero/', 'sequencias.txt', filtro=None, treino=False, etapa=4)
    dicoico(sujeito, 'diamante/', 'sequencias.txt', filtro=None, treino=True, etapa=4)
limpa_tela()


print('#########  12 - Mostra os dados pro voluntário ############')
print('Chama o cara pra ver os gráficos')
print('')
mostra(sujeito)
limpa_tela()
