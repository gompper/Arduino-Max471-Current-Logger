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

def saveDataToFile(data):
    f = open(FILE,"wb")
    np.save(f,data)
    f.close()

def capture():
    buffer = ""
    buf_arr = []
    with serial.Serial('COM6', 115200, timeout=1) as ser:
        start = time.time()
        while(len(buf_arr)<1000):
            # read one byte
            oneByte = ser.read(1)
            
            # test if received byte is line break
            if oneByte == b"\r":    
                try:
                    buf_int = int(buffer)
                    pass
                except ValueError:
                    buffer = ""
                    continue
                
                # convert raw data to ampère
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
        
        # calculate samples/second (averaging over 64 samples is done on arduino)
        SamplesPerSecond = (len(buf_arr)/(end-start))*64
        print(round(SamplesPerSecond,2), "sample/s")

        buf_np = np.asarray(buf_arr)
        saveDataToFile(buf_np)
        plot_amps.plotData(FILE)
        
if __name__ == "__main__":
    capture()