import numpy as np
from spectrum import invert_spectrum
def zera_pistas(amplfftL, amplfftR, phasefftL, phasefftR, azim, correction_type):
    """
    Aplica correção de ITD, ILD ou ambos aos espectros dos canais esquerdo e direito.
    
    Parameters:
    amplfftL (np.ndarray): Amplitude do espectro do canal esquerdo.
    amplfftR (np.ndarray): Amplitude do espectro do canal direito.
    phasefftL (np.ndarray): Fase do espectro do canal esquerdo.
    phasefftR (np.ndarray): Fase do espectro do canal direito.
    azim (float): Ângulo de azimute.
    correction_type (str): Tipo de correção ('ILD', 'ITD', 'both').

    Returns:
    np.ndarray: Matriz com os canais corrigidos.
    """
    # Inicializa os canais
    left_channel = np.array([])
    right_channel = np.array([])

    if correction_type == 'ILD':
        # Correção ILD: zera a diferença de nível
        avg_amplfft = 0.5 * (amplfftL + amplfftR)
        left_channel = invert_spectrum(avg_amplfft, phasefftL)
        right_channel = invert_spectrum(avg_amplfft, phasefftR)

    elif correction_type == 'ITD':
        # Correção ITD: zera a diferença de tempo
        if azim < 0:
            # Azimute negativo
            left_channel = invert_spectrum(amplfftL, phasefftL)
            right_channel = invert_spectrum(amplfftR, phasefftL)
        else:
            # Azimute positivo ou zero
            left_channel = invert_spectrum(amplfftL, phasefftR)
            right_channel = invert_spectrum(amplfftR, phasefftR)

    elif correction_type == 'both':
        # Correção de ITD e ILD
        avg_amplfft = 0.5 * (amplfftL + amplfftR)
        if azim < 0:
            left_channel = invert_spectrum(avg_amplfft, phasefftL)
            right_channel = invert_spectrum(avg_amplfft, phasefftL)
        else:
            left_channel = invert_spectrum(avg_amplfft, phasefftR)
            right_channel = invert_spectrum(avg_amplfft, phasefftR)
    
    elif correction_type == 'none':
        left_channel = invert_spectrum(amplfftL, phasefftL)
        right_channel = invert_spectrum(amplfftR, phasefftR)

    else:
        raise ValueError('Tipo de correção desconhecido.')

    # Cria uma matriz com os dois canais
    soundclip = np.column_stack((left_channel, right_channel))
    return soundclip
