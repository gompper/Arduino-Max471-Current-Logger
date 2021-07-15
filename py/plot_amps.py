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
    else:
        fig,axis = plt.subplots(totalPlots)
        mean_list = []
        for i in range(totalPlots):
            FILE_temp = FILE[:len(FILE)-5] + str(i) + FILE[len(FILE)-4:]
            with open(FILE_temp,"rb") as f:
                loaded_data = np.load(f)
                axis[i].plot(loaded_data)
                mean_list.append(loaded_data.mean())
    mean_list_np = np.asarray(mean_list)
    print("mean current:",mean_list_np.mean())
    plt.xlabel("Sample")
    plt.ylabel("Current [Ampère]")
    plt.show()

def main(arg,totalPlots=None):
    plotData(arg,int(totalPlots))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Insufficient arguments, correct usage: \n\t$ python3 plot_amps.py <./path/to/numpyfile.npy>")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
