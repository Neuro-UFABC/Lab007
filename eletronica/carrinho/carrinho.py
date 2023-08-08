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
        self.azim = -90
        self.modo = 'azimute'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ser.close()

    def habilita_motores(self):
        self._cmd('h')
        
    def desabilita_motores(self):
        self._cmd('d')

    def anda_mm(self, eixo, mm):
        if eixo not in ('grande', 'pequeno'):
            print("anda_mm recebe como primeiro parâmetro 'grande' ou 'pequeno'")
            return

        if self.modo == 'azimute':
            self.habilita_motores()

        passos = int(self.passos_mm * mm)
        dir = '+' if mm > 0 else '-'
        passos = int(abs(mm) * self.passos_mm)
        print(f'Vou dar {dir}{passos} passos no eixo {eixo}')

        xy = 'x' if eixo == 'pequeno' else 'y'
        self._cmd(f'p{xy}{dir}{passos}')

        if self.modo == 'azimute':
            self.desabilita_motores()

    def zera(self):
        input('Ponha manualmente na origem e aperte Enter...')
        self.azim = -90
        self.anda_mm('grande', +70)
        

    def anda_azim(self, azim):

        def r(azim):
            # referencial do experimento para radianos usuais
            return -(azim - 90) * pi / 180

        th0 = r(self.azim)
        th1 = r(azim)

        dgrande = self.raio * (cos(th1) - cos(th0))
        dpeq = self.raio * (sin(th1) - sin(th0))

        self.anda_mm('grande', dgrande)
        self.anda_mm('pequeno', dpeq)

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
