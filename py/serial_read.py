import serial 
import time
import numpy as np
import datetime
import threading
import sys
import plot_amps as pa

# Config: Serial 
COMPORT         = 'COM7'
BAUDRATE        = 115200

# Config: Output File
FILENAME        = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now())
FILEPATH        = './data/'
FILEEXTENSION   = ".npy"

DATASETS        = 0
RUN             = True

def ADCRaw2Amp(val,BITS,MAXVAL):
    return val*MAXVAL/(pow(2,BITS)-1)

def saveDataToFile(data,number):
    file = FILEPATH + FILENAME + '_' + number + FILEEXTENSION
    f = open(file,"wb")
    np.save(f,data)
    f.close()

def startCapture():
    global DATASETS 
    buffer = ""
    data = []
    data_temp = []
    with serial.Serial(COMPORT, BAUDRATE, timeout=1) as ser:
        timeStart = time.time()
        print("Start capturing...")
        while(RUN):
            # read one byte
            oneByte = ser.read(1)
            
            # test if received byte is line break
            if oneByte == b"\r":    
                try:
                    buf_int = int(buffer)
                    # pass
                except ValueError:
                    try:
                        start = str(buffer)
                        print(start)
                        if DATASETS > 0:
                            data.append(data_temp)
                        DATASETS += 1
                        data_temp = []
                    except:
                        continue
                    buffer = ""
                    continue
                
                # print(str(buf_int))
                # convert raw data to ampère
                buf_converted = ADCRaw2Amp(buf_int,10,5)
                data_temp.append(buf_converted)
                buffer = ""
            else:
                try:
                    buffer += oneByte.decode("utf-8") 
                except UnicodeDecodeError:
                    buffer = ""
                    continue
        timeEnd = time.time()
        
        print("Stopped capturing.")
        print("Total time elapsed:",round(timeEnd-timeStart,2)," seconds.")

        for i in range(len(data)):
            number = str(i)
            data_np = np.asarray(data[i])
            saveDataToFile(data_np,number)
        
def stopCapture():
    global RUN
    RUN = False

def main(**kwargs):
    global COMPORT
    for k,v in kwargs.items():
        if k == 'p':
            COMPORT = v
        if k == 'sets':
            maxDATASETS = int(v)
    captureT = threading.Thread(target=startCapture)
    captureT.start()
    while(DATASETS<maxDATASETS):
        time.sleep(10)
    stopCapture()
    captureT.join()
    pa.plotData(FILEPATH + FILENAME + '_0' + FILEEXTENSION,DATASETS-1)

if __name__ == "__main__":
    main( **dict(arg.split('=') for arg in sys.argv[1:]) )
