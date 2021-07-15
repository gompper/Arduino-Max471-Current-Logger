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
        
        print("Start capturing...")
        while(RUN):
            # read one byte
            oneByte = ser.read(1)
            
            # test if received byte is line break
            if oneByte == b"\r":    
                try:
                    buf_int = int(buffer)
                    # print(buf_int)
                    pass
                except ValueError:
                    try:
                        message = str(buffer)
                        if(message == '\nB'):
                            timeStart = time.time()
                        if(message == '\nE'):
                            timeEnd = time.time()
                            # skip 1st set, cause it's maybe incomplete
                            if DATASETS > 0:
                                data.append(data_temp)
                                deltaTime = timeEnd-timeStart
                                samples = len(data_temp)
                                samplerate = samples/deltaTime
                                period = 1/samplerate
                                print("No:",DATASETS-1,"\tTime:",round(deltaTime,5),"s\tSamples:",samples,"\tSampleRate:",round(samplerate,2),"SPS\t\tPeriod:",period,"s")
                            DATASETS += 1
                            data_temp = []
                    except:
                        continue
                    buffer = ""
                    continue
                
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
       
        
        print("Stopped capturing.")
        

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
    while(DATASETS<maxDATASETS+1):
        time.sleep(1)
    stopCapture()
    captureT.join()
    pa.plotData(FILEPATH + FILENAME + '_0' + FILEEXTENSION,DATASETS-1)

if __name__ == "__main__":
    main( **dict(arg.split('=') for arg in sys.argv[1:]) )
