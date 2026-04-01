import os
import numpy as np
import soundfile as sf
import scipy.signal as sig
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def circ_mean(angles):
    """Circular mean of phase angles."""
    return np.angle(np.mean(np.exp(1j * angles)))


def ipd2itd(ipd, freq):
    """Convert interaural phase difference to ITD (seconds)."""
    return ipd / (2 * np.pi * freq)


def filtro500Hz(x, fs):
    """Bandpass around 500 Hz."""
    b, a = sig.butter(4, [450/(fs/2), 550/(fs/2)], btype='band')
    return sig.filtfilt(b, a, x)


def risefall_onset(t, onset, duracao, risetime, decaytime):
    """
    Python equivalent of MATLAB risefall_onset using raised cosine.

    envelope = risefall_onset(t, onset, duracao, risetime, decaytime)

    Parameters
    ----------
    t : ndarray
        Time vector (seconds)
    onset : float
        Envelope onset time
    duracao : float
        Total duration of envelope
    risetime : float
        Rise time
    decaytime : float
        Decay time
    """

    uptime = duracao - decaytime - risetime

    # rising envelope
    envelopesobe = 0.5 * (1 - np.cos(2 * np.pi * (1/(2*risetime)) * (t - onset)))

    envelopesobe = envelopesobe.copy()
    envelopesobe[t < onset] = 0
    envelopesobe[t > onset + risetime] = 1

    offset = onset + risetime + uptime

    # falling envelope
    envelopedesce = 0.5 * (1 + np.cos(2 * np.pi * (1/(2*decaytime)) * (t - offset)))

    envelopedesce = envelopedesce.copy()
    envelopedesce[t < offset] = 1
    envelopedesce[t > offset + decaytime] = 0

    envelope = envelopesobe * envelopedesce

    return envelope


# ---------------------------------------------------------
# Extract ITD / ILD
# ---------------------------------------------------------

def extract_itd_ild(folder, azim, filtro_file):

    filtro, fs = sf.read(filtro_file)

    onset1 = 17093
    window = np.arange(-fs//50, fs//50)

    idxbase = onset1 + np.arange(-750, -250)
    idx2a6ms = np.arange(int(0.002*fs), int(0.006*fs))

    dur_rampa = np.array(
        [0,0]
    )

    ITD = np.zeros((len(azim), len(dur_rampa)))
    ILD = np.zeros_like(ITD)

    absL = np.zeros_like(ITD)
    absR = np.zeros_like(ITD)

    for ai, a in enumerate(azim):

        file = f"{folder}/para_estimar_ITD_ILD/2tons0ms_{a}.wav"
        som, fs = sf.read(file)

        # equalization
        som[:,0] = sig.convolve(som[:,0], -filtro[:,0], mode='same')
        som[:,1] = sig.convolve(som[:,1], -filtro[:,1], mode='same')

        # band filter
        som[:,0] = filtro500Hz(som[:,0], fs)
        som[:,1] = filtro500Hz(som[:,1], fs)

        idxwindow = onset1 + window
        base = som[idxbase,:].flatten()
        mediabase = base.mean()
        desviobase = base.std()

        ndesvios = 20

        temp1 = np.where(
            np.abs(som[idxwindow,0]) > mediabase + ndesvios*desviobase
        )[0][0]

        temp2 = np.where(
            np.abs(som[idxwindow,1]) > mediabase + ndesvios*desviobase
        )[0][0]

        temp = min(temp1, temp2)
        onset = idxwindow[temp]

        hilL = sig.hilbert(som[:,0])
        hilR = sig.hilbert(som[:,1])

        for r in range(len(dur_rampa)):

            idx = onset + int((r)*(0.05 + 2*0.25)*fs) + idx2a6ms
            idx = np.round(idx).astype(int)

            phase_diff = np.angle(hilR[idx]) - np.angle(hilL[idx])

            ITD[ai,r] = ipd2itd(circ_mean(phase_diff), 500) * 1e6
            ILD[ai,r] = 20*np.log10(
                np.mean(np.abs(hilR[idx])) /
                np.mean(np.abs(hilL[idx]))
            )

            absL[ai,r] = np.mean(np.abs(hilL[idx]))
            absR[ai,r] = np.mean(np.abs(hilR[idx]))

    return np.mean(ITD,1), np.mean(ILD,1), np.mean(absL,1), np.mean(absR,1), fs


# ---------------------------------------------------------
# Synthetic stimulus generator
# ---------------------------------------------------------

def generate_synthetic(folder, azim, ITD, absL, absR, fs, manipulation):

    outdir = f"{folder}/sintetico_{manipulation}"
    os.makedirs(outdir, exist_ok=True)

    norm = max(np.max(absL), np.max(absR))
    absL /= norm
    absR /= norm

    pausa = 0.250
    dur = 0.050

    t = np.arange(0, pausa+dur+pausa, 1/fs)

    for i,a in enumerate(azim):

        itd = ITD[i] * 1e-6
        itd_phase = itd
        itd_env = itd

        ampL = absL[i]
        ampR = absR[i]

        if manipulation == "ILDzero":
            ampL = ampR = np.mean([absL[6], absR[6]])

        if manipulation == "ITDzero":
            itd = itd_phase = itd_env = 0

        if manipulation == "ITDphasezero":
            itd_phase = 0

        if manipulation == "ITDenvelopezero":
            itd_env = 0

        sigL = ampL * np.sin(2*np.pi*500*t)
        sigR = ampR * np.sin(2*np.pi*500*(t + itd_phase))

        envL = risefall_onset(t, pausa + itd_env, dur, 0.005, 0.005)
        envR = risefall_onset(t, pausa, dur, 0.005, 0.005)

        signal = np.column_stack([envL*sigL, envR*sigR])

        signal = np.tile(signal, (5,1))

        outfile = f"{outdir}/sintetico_{manipulation}_{a}.wav"
        sf.write(outfile, signal, fs)



def processa_sujeito(suj):

    azim = np.arange(-90, 91, 15)
    filtro_file = "filtro_equalizacao_hd_mic_ind_48k.wav"
    ITD, ILD, absL, absR, fs = extract_itd_ild(suj, azim, filtro_file)
    
    np.savetxt(f'{suj}/ITD_ILD_azim.txt', np.c_[ITD, ILD, azim])
    generate_synthetic(suj, azim, ITD, absL, absR, fs, "naomanipulado")
    generate_synthetic(suj, azim, ITD, absL, absR, fs, "ILDzero")


if __name__ == "__main__":
    import sys
    processa_sujeito(sys.argv[1])



