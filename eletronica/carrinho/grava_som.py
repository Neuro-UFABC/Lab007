import time
import sounddevice as sd
from scipy.io.wavfile import write


def grava_binaural(segundos, fname):
    fs = 44100  # Sample rate

    if fname is None:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fname = f'gravacao-{timestr}.wav'
    print(f'Começando gravação de {segundos}s')
    rec = sd.rec(int(segundos * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(fname, fs, rec)  
    print(f'Gravação concluída. Salvo arquivo {fname}.')

if __name__ == '__main__':
    print('gravando 5s em lixo.wav')
    grava_binaural(5, 'lixo.wav')
