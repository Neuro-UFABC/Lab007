import numpy as np

def risefall_kernel(Fs, duration, risetime, offsetrise, decaytime):
    # SYNTAX: kernel = risefall_kernel(Fs,duration,risetime,offsetrise,decaytime)

    # duration=1
    # Fs=44100
    # risetime=0.005
    # offsetrise=0.001
    # decaytime=0.05

    timevec = np.arange(1, duration * Fs + 1) / Fs

    rcRISE = 0.5 - 0.5 * np.cos(2 * np.pi * (1 / risetime) / 2 * (timevec - offsetrise))
    rcRISE[timevec < offsetrise] = 0
    rcRISE[timevec > offsetrise + risetime] = 1

    rcDECAY = 0.5 - 0.5 * np.cos(2 * np.pi * (1 / decaytime) / 2 * (-timevec + timevec[-1]))
    rcDECAY[timevec < timevec[-1] - decaytime] = 1

    kernel = rcRISE * rcDECAY

    return kernel
