import serial
import time
import serial

class Apontador:
    def __init__(self):
        #self._ser = serial.Serial('/dev/ttyACM0') 
        self._ser = serial.Serial('/dev/ttyUSB0') # TODO: pode ser outra
        print('Aberta serial', self._ser.name)
        time.sleep(2) # espera arduino resetar

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ser.close()

    def le_pot(self, ):
        ret = self._cmd('a')
        val = int(ret.strip())
        return val
    
    def sobe(self, passos):
        self._cmd(f'p{passos}')

    def desce(self, passos):
        self._cmd(f'p-{passos}')

    def _cmd(self, arg):
        scmd = str(arg) + '\n'
        self._ser.write(scmd.encode("utf-8"))
        return self._ser.readline()
