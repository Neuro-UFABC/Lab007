import serial
import time
import serial

class Carrinho:
    def __init__(self):
        self._ser = serial.Serial('/dev/ttyACM0') # TODO: pode ser outra
        print('Aberta serial', self._ser.name)
        time.sleep(2) # espera arduino resetar

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ser.close()

    def sobe(self, passos):
        self._cmd(passos)

    def desce(self, passos):
        self._cmd(f'-{passos}')

    def _cmd(self, arg):
        scmd = str(arg) + '\n'
        self._ser.write(scmd.encode("utf-8"))