import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy.lib import load

from numpy.lib.function_base import average

def plotData(FILE):
    with open(FILE,"rb") as f:
        loaded_data = np.load(f)
    amps_average = np.sum(loaded_data) / loaded_data.size
    print("average ampere consumption:",amps_average)

    plt.plot(loaded_data)
    plt.xlabel("Sample [1*64]")
    plt.ylabel("Current [Ampère]")
    plt.show()

def main(arg):
    plotData(arg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Insufficient arguments, correct usage: \n\t$ python3 plot_amps.py <./path/to/numpyfile.npy>")
    else:
        main(sys.argv[1])     