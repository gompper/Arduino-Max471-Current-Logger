import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy.lib import load

from numpy.lib.function_base import average

def plotData(FILE,totalPlots=None):
    if totalPlots == None:
        with open(FILE,"rb") as f:
            loaded_data = np.load(f)
        plt.plot(loaded_data)
        plt.xlabel("Sample")
        plt.ylabel("Current [Ampère]")
    else:
        fig,axis = plt.subplots(totalPlots)
        for i in range(totalPlots):
            FILE = FILE[:len(FILE)-5] + str(i) + FILE[len(FILE)-4:]
            with open(FILE,"rb") as f:
                loaded_data = np.load(f)
                axis[i].plot(loaded_data)

    plt.show()

def main(arg):
    plotData(arg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Insufficient arguments, correct usage: \n\t$ python3 plot_amps.py <./path/to/numpyfile.npy>")
    else:
        main(sys.argv[1])     