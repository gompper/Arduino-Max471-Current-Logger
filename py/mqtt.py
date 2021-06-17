import paho.mqtt.subscribe as mqtts
import paho.mqtt.client as mqttclient

topic   = "/gompbach/sensordata"
ca_file = './ca.pem'
broker  = "broker-gompbach"
port    = 8883
qos     = 2

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

mqttc = mqttclient.Client("Python_Subscription")
mqttc.on_connect = on_connect  # Define callback function for successful connection
mqttc.on_message = on_message  # Define callback function for receipt of a message
mqttc.tls_set(ca_file)
mqttc.connect(broker, port)
mqttc.subscribe(topic,qos=qos)
mqttc.loop_forever()