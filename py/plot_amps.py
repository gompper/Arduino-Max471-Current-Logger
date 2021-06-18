import matplotlib.pyplot as plt
import numpy as np
import sys

def plotData(FILE):
    with open(FILE,"rb") as f:
        loaded_data = np.load(f)
    plt.plot(loaded_data)
    plt.xlabel("Sample*64")
    plt.ylabel("Ampère")
    plt.show()

def main(arg):
    plotData(arg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Insufficient arguments, correct usage: \n\t$ python3 plot_amps.py <./path/to/numpyfile.npy>")
    else:
        main(sys.argv[1])     