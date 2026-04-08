import sys
import time
import traceback
import sounddevice as sd

from estima_dicoico_equilibrado import dicoico
from grava_oreba import oreba
from mostra_estimativas import mostra
from estima_gaiola import gaiola
from gera_estimulos import processa_sujeito


# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------

def atualiza_dispositivos():
    print("Reiniciando dispositivos de áudio...")
    sd._terminate()
    sd._initialize()
    return sd.query_devices()


def limpa_tela():
    print("\033[H\033[J", end="")


def executa_bloco(func_bloco, nome):

    while True:

        try:
            func_bloco()
            break

        except Exception as e:

            print("\nERRO NO", nome)
            print(e)
            traceback.print_exc()

            resp = input(
                "\nPressione ENTER para tentar novamente ou digite 'pular' para pular o bloco: "
            )

            if resp.lower() == "pular":
                break


# ---------------------------------------------------------
# Blocos
# ---------------------------------------------------------

def bloco1(sujeito):

    print("""
######### 1 - Estima dicóico ############

Liga o apontador na USB
Pluga o fone de ouvido na saída de áudio
Posiciona o voluntário, mostra fone e apontador

Instruções:
“Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante a
execução da tarefa. As primeiras 5 tentativas são só pra treinar,
depois começa de verdade.”
""")

    input("Enter pra continuar")

    dicoico(
        sujeito,
        "diamante/",
        "sequencias.txt",
        filtro=None,
        treino=True,
        etapa=1
    )

    limpa_tela()


def bloco2(sujeito):

    print("""
######### 2 - Grava oreba ############

Liga a fonte dos motores de passo
Liga a H6 na USB e põe os microfones na orelha
Pluga o falante na saída de áudio
Zera o falante da gaiola

Instruções:
“Vamos gravar como os sons chegam na sua orelha. Mantenha a cabeça fixa
olhos abertos olhando sempre para o ponto de fixação.”
""")

    input("Enter pra continuar")

    atualiza_dispositivos()

    oreba(sujeito)

    print("\nGerando estímulos a partir das gravações...\n")
    processa_sujeito(sujeito)

    limpa_tela()


def bloco3(sujeito):

    print("""
######### 3 - Mostra os dados pro voluntário ############

Chama o voluntário pra ver os gráficos.

Instruções:
“Esse é o gráfico das média das estimativas em função dos azimutes.
Se as estimativas desviaram da linha preta, faça com mais cuidado.
Serão apresentados todos os azimutes com mesma frequência,
de -90 a 90.”
""")

    mostra(sujeito)

    limpa_tela()


def bloco4(sujeito):

    print("""
######### 4 - Estima gaiola ############

Liga o apontador na USB
Zera o falante da gaiola

Instruções:
“Você ouvirá sons do falante, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o
botão. Em seguida, abra os olhos para ver onde o falante realmente está.
Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”
""")

    input("Enter pra continuar")

    atualiza_dispositivos()

    gaiola(sujeito)

    limpa_tela()


def bloco5(sujeito):

    print(f"""
######### 5 - Estima dicóico ############

Pluga o fone de ouvido na saída de áudio

Instruções:
“Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante
a execução da tarefa.”
""")

    input("Enter pra continuar")

    dicoico(
        sujeito,
        f"{sujeito}/sintetico_naomanipulado/",
        "sequencias.txt",
        filtro=None,
        treino=False,
        etapa=2
    )

    limpa_tela()


def bloco6(sujeito):

    print("""
######### 6 - Mostra os dados pro voluntário ############

Chama o voluntário pra ver os gráficos.

Instruções:
“Esse é o gráfico das média das estimativas em função dos azimutes.
Se as estimativas desviaram da linha preta, faça com mais cuidado.
Serão apresentados todos os azimutes com mesma frequência,
de -90 a 90.”
""")

    mostra(sujeito)

    limpa_tela()


def bloco7(sujeito):

    print("""
######### 7 - Estima gaiola ############

Pluga o falante na saída de áudio
Zera o falante da gaiola

Instruções:
“Você ouvirá sons do falante, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o
botão. Em seguida, abra os olhos para ver onde o falante realmente está.
Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”
""")

    input("Enter pra continuar")

    gaiola(sujeito)

    limpa_tela()


def bloco8(sujeito):

    print("""
######### 8 - Estima dicóico ############

Pluga o fone de ouvido na saída de áudio

Instruções:
“Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante
a execução da tarefa.”
""")

    input("Enter pra continuar")

    dicoico(
        sujeito,
        f"{sujeito}/sintetico_naomanipulado/",
        "sequencias.txt",
        filtro=None,
        treino=False,
        etapa=3
    )

    limpa_tela()


def bloco9(sujeito):

    print("""
######### 9 - Mostra os dados pro voluntário ############

Chama o voluntário pra ver os gráficos.

Instruções:
“Esse é o gráfico das média das estimativas em função dos azimutes.
Se as estimativas desviaram da linha preta, faça com mais cuidado.
Serão apresentados todos os azimutes com mesma frequência,
de -90 a 90.”
""")

    mostra(sujeito)

    limpa_tela()


def bloco10(sujeito):

    print("""
######### 10 - Estima gaiola ############

Pluga o falante na saída de áudio
Zera o falante da gaiola

Instruções:
“Você ouvirá sons do falante, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados até apertar o
botão. Em seguida, abra os olhos para ver onde o falante realmente está.
Finalmente, feche os olhos e aperte o botão para continuar com a tarefa.”
""")

    input("Enter pra continuar")

    gaiola(sujeito)

    limpa_tela()


def bloco11(sujeito):

    print("""
######### 11 - Estima dicóico ############

Pluga o fone de ouvido na saída de áudio

Instruções:
“Você ouvirá sons no fone de ouvido, aponte pra onde acha que está e
aperte o botão. Mantenha a cabeça fixa e seus olhos fechados durante
a execução da tarefa.”
""")

    input("Enter pra continuar")

    dicoico(
        sujeito,
        "diamante/",
        "sequencias.txt",
        filtro=None,
        treino=True,
        etapa=4
    )

    limpa_tela()


def bloco12(sujeito):

    print("""
######### 12 - Mostra os dados pro voluntário ############

Chama o voluntário pra ver os gráficos.
""")

    mostra(sujeito)

    limpa_tela()


# ---------------------------------------------------------
# Registro
# ---------------------------------------------------------

BLOCOS = {
    1: bloco1,
    2: bloco2,
    3: bloco3,
    4: bloco4,
    5: bloco5,
    6: bloco6,
    7: bloco7,
    8: bloco8,
    9: bloco9,
    10: bloco10,
    11: bloco11,
    12: bloco12,
}


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("\nUso:\npython protocolo2.py SUJEITO [bloco_inicial]\n")
        sys.exit()

    sujeito = sys.argv[1]

    bloco_inicial = 1

    if len(sys.argv) >= 3:
        bloco_inicial = int(sys.argv[2])

    print(f"\nSujeito: {sujeito}")
    print(f"Iniciando no bloco {bloco_inicial}\n")

    for b in range(bloco_inicial, 13):

        func = BLOCOS[b]

        executa_bloco(lambda: func(sujeito), f"Bloco {b}")
