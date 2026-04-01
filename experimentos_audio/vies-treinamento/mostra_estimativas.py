import pandas as pd
import glob
import matplotlib.pylab as plt
import numpy as np
from pathlib import Path
from scipy.interpolate import interp1d


def mostra_estimativas(suj):

    arq_ests = glob.glob(f'{suj}/*.csv')[0]
    ests = pd.read_csv(arq_ests)
    ITD, ILD, az = np.loadtxt(f'{suj}/ITD_ILD_azim.txt').T
    mu_estimados = ests.groupby('# verdadeiro')[' estimado'].mean().to_numpy()

   
    azim = np.arange(-90, 91, 15)
    
    itd2az = interp1d(ITD, az, fill_value="extrapolate", bounds_error=False)

    ITDests = np.arange(-720,721,120)

    f, ax = plt.subplots()
    ax.plot(itd2az(ITDests),az)
    ax.plot([-90,90], [-90,90])
    ax.set_aspect('equal')
    ax.set_xlabel('Azimute real')
    ax.set_ylabel('Azimute estimado')
    ax.grid(True)
    plt.show()

if __name__ == '__main__':

    suj = Path('xxx')
    mostra_estimativas(suj)
