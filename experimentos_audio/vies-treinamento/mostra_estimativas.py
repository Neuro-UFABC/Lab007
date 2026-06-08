import glob
import sys
import matplotlib.pylab as plt
import numpy as np
from pathlib import Path
from scipy.interpolate import interp1d
import pandas as pd


def mostra(suj):

    f, ax = plt.subplots()
    ax.plot([-90,90], [-90,90], 'k')
    ax.set_aspect('equal')
    ax.set_xlabel('Azimute real')
    ax.set_ylabel('Azimute estimado')
    ax.grid(True)

    for arq_estimativas in sorted(glob.glob(f'{suj}/estimativas_dicoico*.csv')):
        etapa = int(arq_estimativas[-5])
        print(arq_estimativas, 'etapa', etapa)

        ests = pd.read_csv(arq_estimativas)
        az_estimados = ests.groupby('verdadeiro')['estimado'].mean().to_numpy()

        if etapa == 1 or etapa == 4:
            ITD, ILD, az = np.loadtxt(f'{suj}/ITD_ILD_azim.txt').T
            itd2az = interp1d(ITD, az, fill_value="extrapolate", bounds_error=False)
            ITD_estimulos = np.arange(-720,721,120)  
            #ITD_estimulos = np.arange(-300,301,50)  # NOVA SERIE
            azim_verdadeiro = itd2az(ITD_estimulos) 
        if etapa == 2 or etapa == 3:
            azim_verdadeiro = np.arange(-90,91,15)

        ax.plot(azim_verdadeiro, az_estimados, label=etapa)

    ax.legend()
    plt.show()

if __name__ == '__main__':

    quem = sys.argv[1]
    suj = Path(quem)
    mostra(suj)
