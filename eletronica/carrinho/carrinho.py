import serial
import time
import serial
from math import sin, cos, radians, pi

class Carrinho:
    def __init__(self):
        #self._ser = serial.Serial('/dev/ttyACM0') # TODO: pode ser outra
        self._ser = serial.Serial('/dev/ttyUSB0') # TODO: pode ser outra
        print('Aberta serial', self._ser.name)
        time.sleep(2) # espera arduino resetar
        self.passos_mm = 40  # precisa calibrar!!!
        self.raio = 800  # precisa calibrar!!!

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ser.close()

    def habilita_motores(self):
        self._cmd('h')
        
    def desabilita_motores(self):
        self._cmd('d')
    
    def anda_grande_mm(self, mm):
        self.habilita_motores()
        passos = int(self.passos_mm * mm)
        dir = '+' if mm > 0 else '-'
        passos = int(abs(mm) * self.passos_mm)
        print(f'Vou dar {dir}{passos} passos na grande')
        self._cmd(f'py{dir}{passos}')
        self.desabilita_motores()

    def anda_peq_mm(self, mm):
        self.habilita_motores()
        passos = int(self.passos_mm * mm)
        dir = '+' if mm > 0 else '-'
        passos = int(abs(mm) * self.passos_mm)
        print(f'Vou dar {dir}{passos} passos na pequeno')
        self._cmd(f'px{dir}{passos}')
        self.desabilita_motores()


    def zera(self):
        input('Ponha manualmente na origem e aperte Enter...')
        self.azim = 90
        self.anda_grande_mm(-70)

    def anda_azim(self, azim):
        dazim = azim - self.azim
        if self.azim > 0:
            if dazim > 0:
                dirx = -1 
                diry = +1
            else:
                dirx = +1
                diry = -1
        else:
            if dazim > 0:
                dirx = +1 
                diry = +1
            else:
                dirx = -1
                diry = -1

        self.anda_grande_mm(self.raio * 
                diry * abs(sin(azim*pi/180) - sin(self.azim*pi/180)))
        self.anda_peq_mm(self.raio * 
                dirx * abs(cos(azim*pi/180) - cos(self.azim*pi/180)))

        self.azim = azim

    def sobe_mm(self, mm):
        passos = int(self.passos_mm * mm)
        print(f'Vou dar {passos} passos')
        self.sobe(passos)

    def desce_mm(self, mm):
        passos = int(self.passos_mm * mm)
        print(f'Vou dar {passos} passos')
        self.desce(passos)

    def delay(self, delay):
        print(f'Ajustando delay para {delay} ms')
        self._cmd(f'c{delay}')

    def sobe(self, passos):
        self._cmd(f'p{passos}')

    def desce(self, passos):
        self._cmd(f'p-{passos}')

    def _cmd(self, arg):
        scmd = str(arg) + '\n'
        self._ser.write(scmd.encode("utf-8"))
