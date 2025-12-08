import os
import sys
import time
import subprocess

AUDACITY_PATH = '/usr/bin/audacity'

# Função para enviar comandos via pipes
def send_command(command):
    TOFILE.write(command + EOL)
    TOFILE.flush()

# Função para obter resposta dos pipes
def get_response():
    result = ''
    while True:
        line = FROMFILE.readline()
        if not line:
            break
        result += line
        if line == '\n' and len(result) > 0:
            break
    return result

# Função para executar um comando e imprimir a resposta
def do_command(command):
    send_command(command)
    response = get_response()
    print(response)
    return response

# Função para processar todos os arquivos
def process_all_files(filepaths):
    for filepath in filepaths:
        print(f'Abrindo o arquivo {filepath}.')
        # Comando para abrir o Audacity com o arquivo
        command = [AUDACITY_PATH, filepath]
        subprocess.Popen(command, stderr=subprocess.DEVNULL) #stderr suprime as mensagens de erro
        time.sleep(0.2)
        # Esperar o arquivo ser carregado
        time.sleep(2.5)
        
        # Obter perfil de ruído dos primeiros 500ms
        do_command('SelectTime: Start=0 End=0.5')
        do_command('NoiseReduction: GetProfile')
        time.sleep(0.2)
        # Selecionar toda a faixa
        do_command('SelectAll')
        time.sleep(0.2)
        # Configurar os parâmetros de redução de ruído
        do_command('NoiseReduction: SetThreshold=48')
        do_command('NoiseReduction: SetSmoothing=3')
        time.sleep(0.2)
        # Aplicar redução de ruído
        do_command('NoiseReduction:')
        time.sleep(0.2)
        # Exportar o arquivo processado
        output_filepath = filepath.replace('.wav', '_denoised.wav')
        do_command(f'Export2: Filename={output_filepath} Format=WAV NumChannels=2')  # Use Channels=2 para estéreo
        time.sleep(0.2)
        # Fechar o projeto
        do_command('Close:')
        time.sleep(0.2)
        # Confirmar que o arquivo foi exportado e que o projeto foi fechado
        input('Pressione Enter após exportar o arquivo e fechar o projeto no Audacity...')

# Diretório com arquivos .wav
#input_path = input('Caminho da pasta\n') #/home/lab007/repos/Lab007/experimentos_audio/grava_orelha/XX
input_path = '/home/lab007/repos/Lab007/experimentos_audio/grava_orelha/Gustavo11out2024'

filepaths = [os.path.join(input_path, filename) for filename in os.listdir(input_path) if filename.endswith('.wav')]

# Configuração dos pipes
if sys.platform == 'win32':
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

# Iniciar Audacity com suporte a pipe no Ubuntu
subprocess.Popen([AUDACITY_PATH, '--pipe'])
input('Pressione Enter após o Audacity ser iniciado...')

# Abrir pipes
TOFILE = open(TONAME, 'w')
FROMFILE = open(FROMNAME, 'rt')

# Processar arquivos
process_all_files(filepaths)

# Fechar pipes
TOFILE.close()
FROMFILE.close()
