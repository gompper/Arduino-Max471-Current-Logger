import paho.mqtt.client as mqttclient
import threading
import serial_read

topic       = "/gompbach/sensordata"
ca_file     = './ca.pem'
broker      = "broker-gompbach"
port        = 8883
qos         = 2
BOOTCOUNTS  = 300

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    for s in str(msg.payload).strip("'").split(): 
        if s.isdigit():
            bootCount = int(s) 
            print(bootCount)

            # Start capturing
            if bootCount == 0:
                capture_Thread=threading.Thread(target=serial_read.startCapture)
                capture_Thread.start()

            # Stop capturing
            if bootCount == BOOTCOUNTS:
                serial_read.stopCapture()
                client.unsubscribe(topic)
                client.disconnect()
                
def subscribe():
    mqttc = mqttclient.Client("Python_Subscription")
    mqttc.on_connect = on_connect  # Define callback function for successful connection
    mqttc.on_message = on_message  # Define callback function for receipt of a message
    mqttc.tls_set(ca_file)
    mqttc.connect(broker, port)
    mqttc.subscribe(topic,qos=qos)
    mqttc.loop_forever()

if __name__ == "__main__":
    
    subscribe_Thread=threading.Thread(target=subscribe)
    subscribe_Thread.start()
    subscribe_Thread.join()

    print("exiting...")
