import sounddevice as sd
from scipy.io.wavfile import write, read

estimulo = 'sweep300-4k.wav' 
saida = 'conduith_azim0_sweep300-4k_mexido.wav'

sd.default.device = ['h6', 'sysdefault']
sd.default.latency = [0.1, 0.1]

taxa_wav, est_array = read(estimulo)
duracao = len(est_array)
print(f'Começando a tocar {estimulo}. Duração:{duracao}s')
print(f'Começando gravação')

gravacao = sd.playrec(est_array, taxa_wav, channels=2)
sd.wait()
print(sd.get_status())
write(saida, taxa_wav, gravacao)

print(f'Gravação concluída. Salvo arquivo {saida}.')
