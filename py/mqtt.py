import threading

############ MQTT ############
import paho.mqtt.client as mqttclient

############ ARDUINO ############
import serial 
import time
import numpy as np
import datetime
import plot_amps

############ MQTT ############
topic   = "/gompbach/sensordata"
ca_file = './ca.pem'
broker  = "broker-gompbach"
port    = 8883
qos     = 2
RUN     = True

############ ARDUINO ############
FILENAME = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now())
FILEPATH = './data/'
FILEEXTENSION = ".npy"
FILE = FILEPATH + FILENAME + FILEEXTENSION

############ MQTT ############

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    global RUN
    for s in str(msg.payload).strip("'").split(): 
        if s.isdigit():
            bootCount = int(s) 
            print(bootCount)
            if bootCount == 0:
                cap=threading.Thread(target=capture)
                cap.start()
            if bootCount == 2:
                RUN = False
                
    # print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

def subscribe():
    mqttc = mqttclient.Client("Python_Subscription")
    mqttc.on_connect = on_connect  # Define callback function for successful connection
    mqttc.on_message = on_message  # Define callback function for receipt of a message
    mqttc.tls_set(ca_file)
    mqttc.connect(broker, port)
    mqttc.subscribe(topic,qos=qos)
    mqttc.loop_forever()

############ ARDUINO ############

def ADCRaw2Amp(val,BITS,MAXVAL):
    return val*MAXVAL/(pow(2,BITS)-1)

def saveDataToFile(data):
    f = open(FILE,"wb")
    np.save(f,data)
    f.close()

def capture():
    global RUN
    buffer = ""
    buf_arr = []
    print("start capturing...")
    with serial.Serial('COM6', 115200, timeout=1) as ser:
        start = time.time()
        while(RUN):
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
        
        print("stopped capturing...")

        # calculate samples/second (averaging over 64 samples is done on arduino)
        SamplesPerSecond = (len(buf_arr)/(end-start))*64
        print(round(SamplesPerSecond,2), "sample/s")

        buf_np = np.asarray(buf_arr)
        saveDataToFile(buf_np)
        plot_amps.plotData(FILE)

if __name__ == "__main__":
    sub=threading.Thread(target=subscribe)

    sub.start()