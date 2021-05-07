import serial 
import time
import matplotlib.pyplot as plt

def ADCRaw2Amp(val,BITS,MAXVAL):
    return val*MAXVAL/(pow(2,BITS)-1)

buffer = ""
buf_arr = []
with serial.Serial('COM3', 115200, timeout=1) as ser:
    start = time.time()
    for _ in range(5000):
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
    plt.plot(buf_arr)
    plt.show()
        
