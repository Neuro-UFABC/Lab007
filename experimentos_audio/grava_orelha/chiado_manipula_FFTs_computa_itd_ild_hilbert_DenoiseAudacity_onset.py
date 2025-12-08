import numpy as np
import os
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks
from scipy.interpolate import splev, splrep
from risefall_kernel import risefall_kernel
from risefall import risefall
from spectrum import spectrum, invert_spectrum
from zera_pistas import zera_pistas

Fs = 48000  # Frequência de amostragem

soundclip = np.zeros((int(Fs * 4.5), 1))
temp = risefall(2 * np.random.rand(3 * Fs, 1) - 1, Fs, 0.005, 'raisedcosine')
soundclip[int(1 * Fs):int(4 * Fs)] = 0.13 * temp
soundclip[int(0.5 * Fs)] = 1

salva_wav = 1

#diretorio_atual = r'/home/lab007/repos/Lab007/experimentos_audio/grava_orelha/ColetaSandro'
diretorio_atual = os.getcwd()
os.chdir(diretorio_atual)

input_path = input('Nome da pasta\n') #Sandro_1ago2024
pasta = [input_path]

if salva_wav == 1:
    os.makedirs(f"{pasta[0]}_proc", exist_ok=True)

#criterio_click_onset = 0.0005
criterio_click_onset = np.mean(soundclip[0:Fs])+3*np.std(soundclip[0:Fs])

# Sintetiza sons com base na gravação -- Loop sobre as pastas e arquivos
for s in range(len(pasta)):
    folder = os.path.join(pasta[s], '')  # Pasta atual
    arquivo = 'chiadolongocliqueamp90_estereo' # Nome do arquivo
    azim = np.arange(-90, 91, 15)  # Ângulos de azimute
    click_onset_idx = np.zeros((len(azim), 2), dtype=object)
    click_onset_time = np.zeros((len(azim), 2), dtype=object)
    click_onset_idx_diff = np.zeros(len(azim))
    click_onset_time_diff = np.zeros(len(azim))
        
    for a in range(len(azim)):
        filename = os.path.join(folder, f"{pasta[s]}_{arquivo}_{azim[a]}.wav")  # Nome do arquivo de áudio
        soundclip, _ = sf.read(filename) # Carrega o arquivo de áudio
        timevector = np.arange(1, len(soundclip) + 1) / Fs

        # acha os click_onsets na janela adequada
        for i in range(2):
            # Extrai um trecho do som (negativo)
            temp = -soundclip[15000:40000, i]
            temp[temp < criterio_click_onset] = 0

            # Encontra os picos
            peak_locs, _ = find_peaks(temp)
            click_onset_idx[a][i] = peak_locs[0] + 15000

            # Cria o vetor de tempo e interpolação
            timevec = timevector[(-20 + click_onset_idx[a][i]):(20 + click_onset_idx[a][i] + 1)]
            timevec_200 = np.linspace(min(timevec), max(timevec), 1 + 200 * (len(timevec) - 1))

            # Interpola o som com spline
            spline_params = splrep(timevec, -soundclip[(-20 + click_onset_idx[a][i]):(20 + click_onset_idx[a][i] + 1), i])
            temp_interp = splev(timevec_200, spline_params)

            # Aplicando o critério e encontrando os picos
            temp_interp[temp_interp < criterio_click_onset] = 0
            temp2_locs, _ = find_peaks(temp_interp)
            click_onset_time[a][i] = timevec_200[temp2_locs[0]]
    
        # Calcula a diferença entre os índices e tempos de início de clique (click_onset_idx)
        click_onset_idx_diff[a] = np.diff(click_onset_idx[a])
        click_onset_time_diff[a] = np.diff(click_onset_time[a])

        # Calcula o índice de início do som (SoundStart_idx)
        SoundStart_idx = round(np.mean(click_onset_idx[a]) + 0.5 * Fs)

        # Gera kernels
        kernel_50ms_semdelay = risefall_kernel(Fs, 1, 0.050, 0, 0.050)
        kernel_50ms_semdelay = np.column_stack((kernel_50ms_semdelay, kernel_50ms_semdelay))

        kernelL = risefall_kernel(Fs, 1, 0.050, 0, 0.050)
        kernelR = risefall_kernel(Fs, 1, 0.050, -click_onset_time_diff[a], 0.050)
        kernel_50ms_comdelay = np.column_stack((kernelL, kernelR))

        kernelL = risefall_kernel(Fs, 1, 0.005, 0, 0.050)
        kernelR = risefall_kernel(Fs, 1, 0.005, -click_onset_time_diff[a], 0.050)
        kernel_5ms_comdelay = np.column_stack((kernelL, kernelR))

        #GRAVAÇÃO
        soundclip_GRAV = risefall(soundclip[3523:3523 + int(1.5 * Fs)], sr=Fs, transition=0, linearORraisedcosine='raisedcosine')
        
        #if salva_wav == 1:
            #filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_GRAV_{azim[a]}.wav")
            #sf.write(filename_proc, soundclip_GRAV, Fs)

        start_idx = int(SoundStart_idx + Fs)
        end_idx = int(start_idx + 1.5 * Fs)
        soundclip_cut = soundclip[start_idx:end_idx, :]

        amplfftL, phasefftL, freq_fft = spectrum(soundclip_cut[:, 0], Fs)
        amplfftR, phasefftR, _ = spectrum(soundclip_cut[:, 1], Fs)


        #AMBOS ZERADOS
        soundclip_ITD0ILD0 = zera_pistas(amplfftL, amplfftR, phasefftL, phasefftR, azim[a], "both")
        soundclip_ITD0ILD0 = soundclip_ITD0ILD0[np.arange(Fs) + int(0.25 * Fs), :]

        # Ambos 0 slow onset com delay
        soundclip_ITD0ILD0slowonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_comdelay.shape[1])), kernel_50ms_comdelay * soundclip_ITD0ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0ILD0slowonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0ILD0slowonsetdelay, Fs)
           
        # Ambos 0 slow onset sem delay
        soundclip_ITD0ILD0slowonsetsemdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_semdelay.shape[1])), kernel_50ms_semdelay * soundclip_ITD0ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0ILD0slowonsetsemdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0ILD0slowonsetsemdelay, Fs)
            
        # Ambos 0 fast onset
        soundclip_ITD0ILD0fastonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_5ms_comdelay.shape[1])), kernel_5ms_comdelay * soundclip_ITD0ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0ILD0fastonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0ILD0fastonsetdelay, Fs)
        
        #ITD ZERADO
        soundclip_ITD0 = zera_pistas(amplfftL, amplfftR, phasefftL, phasefftR, azim[a], "ITD")
        soundclip_ITD0 = soundclip_ITD0[np.arange(Fs) + int(0.25 * Fs), :]
        
        # ITD0 slow onset com delay
        soundclip_ITD0slowonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_comdelay.shape[1])), kernel_50ms_comdelay * soundclip_ITD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0slowonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0slowonsetdelay, Fs)
            
        # ITD0 slow onset sem delay
        soundclip_ITD0slowonsetsemdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_semdelay.shape[1])), kernel_50ms_semdelay * soundclip_ITD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0slowonsetsemdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0slowonsetsemdelay, Fs)

        # ITD0 fast onset com delay
        soundclip_ITD0fastonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_5ms_comdelay.shape[1])), kernel_5ms_comdelay * soundclip_ITD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ITD0fastonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ITD0fastonsetdelay, Fs)
            
        #ILD ZERADO
        soundclip_ILD0 = zera_pistas(amplfftL, amplfftR, phasefftL, phasefftR, azim[a], "ILD")
        soundclip_ILD0 = soundclip_ILD0[np.arange(Fs) + int(0.25 * Fs), :]
        
        # ILD0 slow onset com delay
        soundclip_ILD0slowonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_comdelay.shape[1])), kernel_50ms_comdelay * soundclip_ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ILD0slowonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ILD0slowonsetdelay, Fs)
            
        # ILD0 slow onset sem delay
        soundclip_ILD0slowonsetsemdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_semdelay.shape[1])), kernel_50ms_semdelay * soundclip_ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ILD0slowonsetsemdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ILD0slowonsetsemdelay, Fs)

        # ILD0 fast onset com delay
        soundclip_ILD0fastonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_5ms_comdelay.shape[1])), kernel_5ms_comdelay * soundclip_ILD0))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ILD0fastonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ILD0fastonsetdelay, Fs)
        
        #CONTROLE (ORIG)
        soundclip_ORIG = zera_pistas(amplfftL, amplfftR, phasefftL, phasefftR, azim[a], "none")
        soundclip_ORIG = soundclip_ORIG[np.arange(Fs) + int(0.25 * Fs), :]
        
        # ORIG slow onset com delay
        soundclip_ORIGslowonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_comdelay.shape[1])), kernel_50ms_comdelay * soundclip_ORIG))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ORIGslowonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ORIGslowonsetdelay, Fs)
            
        # ORIG slow onset sem delay
        soundclip_ORIGslowonsetsemdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_50ms_semdelay.shape[1])), kernel_50ms_semdelay * soundclip_ORIG))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ORIGslowonsetsemdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ORIGslowonsetsemdelay, Fs)

        # ORIG fast onset com delay
        soundclip_ORIGfastonsetdelay = np.vstack((np.zeros((int(0.5 * Fs), kernel_5ms_comdelay.shape[1])), kernel_5ms_comdelay * soundclip_ORIG))
        if salva_wav == 1:
            filename_proc = os.path.join(f"{pasta[s]}_proc", f"{pasta[s]}_{arquivo}_ORIGfastonsetdelay_{azim[a]}.wav")
            sf.write(filename_proc, soundclip_ORIGfastonsetdelay, Fs)
