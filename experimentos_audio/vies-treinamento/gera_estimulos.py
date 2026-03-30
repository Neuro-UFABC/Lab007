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


def risefall_onset(t, onset, dur, rise, fall):
    """Generate envelope with rise/fall ramps."""
    env = np.zeros_like(t)

    start = onset
    stop = onset + dur

    for i, ti in enumerate(t):
        if start <= ti <= stop:
            env[i] = 1

    # smooth with Tukey-like ramps
    ramp_up = np.logical_and(t >= start, t <= start + rise)
    ramp_down = np.logical_and(t >= stop - fall, t <= stop)

    env[ramp_up] *= (t[ramp_up] - start) / rise
    env[ramp_down] *= (stop - t[ramp_down]) / fall

    return env


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
        [0,0.001,0.002,0.003,0.004,0.005,0.006,
         0.007,0.008,0.009,0.010,0.025,0]
    )

    ITD = np.zeros((len(azim), len(dur_rampa)))
    ILD = np.zeros_like(ITD)

    absL = np.zeros_like(ITD)
    absR = np.zeros_like(ITD)

    for ai, a in enumerate(azim):

        file = f"{folder}/{folder}_variasrampas48_{a}.wav"
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

    return ITD, ILD, absL, absR, fs


# ---------------------------------------------------------
# Synthetic stimulus generator
# ---------------------------------------------------------

def generate_synthetic(folder, azim, ITD, absL, absR, fs, manipulation):

    outdir = f"sintetico_{manipulation}_{folder}"
    os.makedirs(outdir, exist_ok=True)

    abs_L = np.mean(absL[:,[0,12]], axis=1)
    abs_R = np.mean(absR[:,[0,12]], axis=1)

    norm = max(np.max(abs_L), np.max(abs_R))
    abs_L /= norm
    abs_R /= norm

    pausa = 0.250
    dur = 0.050

    t = np.arange(0, pausa+dur+pausa, 1/fs)

    for i,a in enumerate(azim):

        itd = np.mean(ITD[i,[0,12]]) * 1e-6
        itd_phase = itd
        itd_env = itd

        ampL = abs_L[i]
        ampR = abs_R[i]

        if manipulation == "ILDzero":
            ampL = ampR = np.mean([abs_L[6], abs_R[6]])

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

        outfile = f"{outdir}/sintetico_{manipulation}_{folder}_{a}.wav"
        sf.write(outfile, signal, fs)


# ---------------------------------------------------------
# Generate ITD sweep stimuli
# ---------------------------------------------------------

def generate_itd_sweep():

    fs = 48000
    itd_vec = np.arange(-720, 721, 120)

    pausa = 0.250
    dur = 0.050

    t = np.arange(0, pausa+dur+pausa, 1/fs)

    os.makedirs("sintetico_variaITD_ILDzero", exist_ok=True)

    for itd in itd_vec:

        itd_sec = itd * 1e-6

        sigL = np.sin(2*np.pi*500*t)
        sigR = np.sin(2*np.pi*500*(t + itd_sec))

        envL = risefall_onset(t, pausa + itd_sec, dur, 0.005, 0.005)
        envR = risefall_onset(t, pausa, dur, 0.005, 0.005)

        signal = np.column_stack([envL*sigL, envR*sigR])
        signal = np.tile(signal, (5,1))

        outfile = f"sintetico_variaITD_ILDzero/sintetico_ITD{itd}_ILDzero.wav"

        sf.write(outfile, signal, fs)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    folder = "Pavao2026mar1148"

    azim = np.arange(-90, 91, 15)

    filtro_file = "filtro_equalizacao_hd_mic_ind_48k.wav"

    ITD, ILD, absL, absR, fs = extract_itd_ild(folder, azim, filtro_file)

    generate_synthetic(folder, azim, ITD, absL, absR, fs, "naomanipulado")

    generate_itd_sweep()
