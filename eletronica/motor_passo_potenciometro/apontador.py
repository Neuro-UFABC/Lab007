import serial
import time
import serial

class Apontador:
    def __init__(self):
        #self._ser = serial.Serial('/dev/ttyACM0') 
        self._ser = serial.Serial('/dev/ttyUSB0') # TODO: pode ser outra
        print('Aberta serial', self._ser.name)
        time.sleep(2) # espera arduino resetar

        print('Usando calibração tosca!! lembre-se de calibrar!!')
        self.pot_min = 23  
        self.pot_max = 694

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ser.close()

    def le_pot(self, ):
        ret = self._cmd('a')
        val = int(ret)
        return val
    
    def sobe(self, passos):
        self._cmd(f'p{passos}')

    def desce(self, passos):
        self._cmd(f'p-{passos}')

    def botao_apertado(self):
        bot = int(self._cmd('b'))
        return bool(bot)

    def espera_botao(self):
        bot = self._cmd('b')
        t_aperta = 0
        while t_aperta < 15:
            if self._cmd('b') != bot:
                t_aperta += 1
            else:
                t_aperta = 0
            time.sleep(0.001)


    def calibra(self):
        print('Aponte para o máximo do alto.')
        print('Depois, aperte o botão')
        self.espera_botao()
        self.pot_max = self.le_pot()

        self.espera_botao()
        print('Aponte para o máximo do baixo.')
        print('Depois, aperte o botão')
        self.espera_botao()
        self.pot_min = self.le_pot()

        return self.pot_min, self.pot_max

    def _cmd(self, arg):
        scmd = str(arg) + '\n'
        self._ser.write(scmd.encode("utf-8"))
        return self._ser.readline().strip()
