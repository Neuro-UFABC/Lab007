import numpy as np

def risefall(soundclip, sr=44100, transition=0.005, linearORraisedcosine='linear'):
    if soundclip.ndim == 1:
        soundclip = soundclip[:, np.newaxis]
    
    if isinstance(transition, (list, tuple)) and len(transition) == 2:
        transition_start, transition_end = transition
    else:
        transition_start = transition_end = transition

    if linearORraisedcosine == 'linear':
        temp = np.vstack([
            np.tile(np.linspace(0, 1, round(sr * transition_start)), (soundclip.shape[1], 1)).T,
            np.ones((soundclip.shape[0] - round(sr * transition_start) - round(sr * transition_end), soundclip.shape[1])),
            np.tile(np.linspace(1, 0, round(sr * transition_end)), (soundclip.shape[1], 1)).T
        ])
        
    elif linearORraisedcosine == 'raisedcosine':
        timevec = np.arange(1, int(round(sr * transition_start)) + 1) / sr
        rc1 = 0.5 - 0.5 * np.cos(np.pi * timevec / transition_start)

        timevec = np.arange(1, int(round(sr * transition_end)) + 1) / sr
        rc2 = 0.5 - 0.5 * np.cos(np.pi * timevec / transition_end)

        temp = np.vstack([
            np.tile(rc1, (soundclip.shape[1], 1)).T,
            np.ones((soundclip.shape[0] - int(round(sr * transition_start)) - int(round(sr * transition_end)), soundclip.shape[1])),
            np.tile(np.flip(rc2), (soundclip.shape[1], 1)).T
        ])
        
    else:
        raise ValueError("Invalid value for 'linearORraisedcosine'. Choose 'linear' or 'raisedcosine'.")

    minlength = min(len(temp), len(soundclip))
    return (soundclip[:minlength, :] * temp[:minlength, :])
