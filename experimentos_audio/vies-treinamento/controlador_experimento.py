import time
import shutil
from pynput import keyboard

def banner(msg):
    larg = shutil.get_terminal_size().columns
    ban = f"{'='*len(msg)}\n{msg}\n{'='*len(msg)}"
    for l in ban.splitlines():
        print(l.center(larg))

class ControladorExperimento:

    def __init__(self):
        self.paused = False
        self.listener = keyboard.Listener(on_press=self.on_press)

    def start(self):
        self.listener.start()

    def on_press(self, key):

        if key == keyboard.Key.space and not self.paused:
            self.paused = True
            banner("Interrompido! Aperte ENTER para continuar")

        elif key == keyboard.Key.enter and self.paused:
            self.paused = False
            print("\nContinuando experimento...\n")

    def espera_se_pausado(self):
        while self.paused:
            time.sleep(0.1)
