import sys
import soundfile as sf
import numpy as np

from audio007.audio_utils import filtra, _toca, nivel, ganho_normalizador, wavfile_pra_array

a_calibrar = sys.argv[1]
ref = 'burstcos-70dB.wav'

print(a_calibrar, ref)
gn = ganho_normalizador(a_calibrar, ref)

tx, som = wavfile_pra_array(a_calibrar)
somlongo = np.vstack((som,)*10) 
_toca(somlongo, ganho=gn, taxa=tx)

#from scipy.io.wavfile import write, read
#write('burstlongo.wav', tx, somlongo)


print(a_calibrar, gn)
