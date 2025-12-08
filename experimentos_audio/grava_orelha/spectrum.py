import numpy as np
from scipy.fftpack import fft
from scipy.fftpack import ifft
from scipy.signal import hann

def spectrum(x, fs):
    """
    Compute the amplitude and phase spectrum of a signal.

    Parameters:
    x  -- input signal in time domain
    fs -- sampling frequency in Hz

    Returns:
    Xamp -- amplitude spectrum (linear scale)
    Xph  -- phase spectrum in radians
    f    -- frequency vector in Hz
    """
    # Convert x to a column vector
    x = np.asarray(x).flatten()

    # Length of the signal
    N = len(x)

    # Apply a Hanning window
    win = hann(N, sym=False)
    x = x * win

    # Compute the FFT of the windowed signal
    fftx = fft(x)

    # Compute the number of unique FFT points
    NumUniquePts = int(np.ceil((N + 1) / 2.0))

    # Take only the first half of the spectrum (due to symmetry)
    fftx = fftx[:NumUniquePts]

    # Coherent amplification of the window (K)
    K = np.sum(win) / N

    # Compute the amplitude spectrum and normalize by the window's coherent amplification
    Xamp = np.abs(fftx) / (N * K)

    # Apply correction to the amplitude spectrum
    if N % 2:  # Odd N excludes Nyquist point
        Xamp[1:] = Xamp[1:] * 2
    else:  # Even N includes Nyquist point
        Xamp[1:-1] = Xamp[1:-1] * 2

    # Compute the phase spectrum in radians (default)
    Xph = np.angle(fftx)

    # Frequency vector
    f = np.linspace(0, fs / 2, NumUniquePts)

    return Xamp, Xph, f

def invert_spectrum(Xamp, Xph):
    """
    Reconstruct a time-domain signal from its amplitude and phase spectrum.

    Parameters:
    Xamp -- amplitude spectrum
    Xph  -- phase spectrum in radians

    Returns:
    x -- reconstructed time-domain signal
    """
    N = 2 * len(Xamp) - 1
    
    # Extend the phase and amplitude spectra to be symmetric
    Xph = np.concatenate((Xph, -np.flipud(Xph[1:])))
    Xamp = np.concatenate((Xamp, np.flipud(Xamp[1:])))
    
    # Apply a Hanning window
    win = hann(N, sym=False)
    K = np.sum(win) / N
    Xamp = Xamp * N * K
    
    # Correct amplitude spectrum
    Xamp[1:] = Xamp[1:] / 2
    
    # Create complex FFT
    fftx = Xamp * np.exp(1j * Xph)
    
    # Perform the inverse FFT
    x = np.real(ifft(fftx))
    
    # Normalize by the window
    x = x / win
    
    return x
