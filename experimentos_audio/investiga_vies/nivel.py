import soundfile as sf
import pyloudnorm as pyln
import numpy as np

def nivel(som, taxa=None):
    if type(som) == str:
        data, rate = sf.read(som)
    else:
        data = som
        rate = taxa
    meter = pyln.Meter(rate)
    return meter.integrated_loudness(data)
    

def ganho_normalizador(estimulo, referencia, taxa=None):
    delta = nivel(referencia, taxa) - nivel(estimulo, taxa)
    return np.power(10.0, delta/20.0)

