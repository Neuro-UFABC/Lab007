import audio_utils as au

print(au.sd.default.device)
au.sd.default.device = ['h6', 'ALC888 Analog']
au.toca_grava('estimulo.wav', 'lixo.wav')

