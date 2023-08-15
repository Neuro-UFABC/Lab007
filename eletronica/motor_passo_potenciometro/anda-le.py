import time
from audio007.apontador import Apontador

import matplotlib.pyplot as plt
import numpy as np

pot = []

pmin = 20
pmax = 590


with Apontador() as a:
    for i in range(100):
        a.desce(1)
        x = a.le_pot()
        pot.append(x)
        print(x)
        time.sleep(0.5) 

plt.plot(pot, 'o')
plt.show()
