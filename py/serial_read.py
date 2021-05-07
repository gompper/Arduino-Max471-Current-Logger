import serial 
import time
import numpy as np
import datetime
import plot_amps

FILENAME = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now())
FILEPATH = './data/'
FILEEXTENSION = ".npy"
FILE = FILEPATH + FILENAME + FILEEXTENSION

def ADCRaw2Amp(val,BITS,MAXVAL):
    return val*MAXVAL/(pow(2,BITS)-1)

def saveData(data):
    f = open(FILE,"wb")
    np.save(f,data)
    f.close()

buffer = ""
buf_arr = []
with serial.Serial('COM3', 115200, timeout=1) as ser:
    start = time.time()
    for _ in range(1000):
        oneByte = ser.read(1)
        if oneByte == b"\r":    
            try:
                buf_int = int(buffer)
                pass
            except ValueError:
                buffer = ""
                continue
            buf_converted = ADCRaw2Amp(buf_int,10,5)
            buf_arr.append(buf_converted)
            buffer = ""
        else:
            try:
                buffer += oneByte.decode("utf-8") 
            except UnicodeDecodeError:
                buffer = ""
                continue
    end = time.time()
    print(round((len(buf_arr)/(end-start))*64,2), "sample/s")
    buf_np = np.asarray(buf_arr)
    saveData(buf_np)
    plot_amps.plotData(FILE)
        
