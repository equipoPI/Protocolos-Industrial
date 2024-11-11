from opcua import Client
import time
import paho.mqtt.client as mqtt

'''
Para iniciar el broker mosquito se necesita introducir el codigo:
mosquitto -c mosquitto.conf


'''

#se debe de colocal la ip del Server OPC UA al que se quiere conectar 
url = "opc.tcp://192.168.0.150:4840"

client = Client(url)

client.connect()
print("Client Connected")

client1 = mqtt.Client()
client1.connect("192.168.0.111", 1883, 60)

while True:
    Temp = client.get_node("ns=2;i=2")
    Temperature = Temp.get_value()
    print(Temperature)
    
    Press = client.get_node("ns=2;i=3")
    Pressure = Press.get_value()
    print(Pressure)
   
    TIME = client.get_node ("ns=2;i=4")
    TIME_Value = TIME.get_value()
    print(TIME_Value)

    
    client1.publish("temp", Temperature)
    client1.publish("press", Pressure)
    client1.publish("time", TIME_Value)
    
    time.sleep(1)


