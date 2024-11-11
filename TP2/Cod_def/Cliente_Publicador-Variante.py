
'''
mosquitto_sub -h ip_broker -t "sensors/#"

lo que hace ese comando es captar todos los topicos que esta sociados al grupo sensors, si se cambia #
por el nombre de un topico se mostrara ese solo
'''

from opcua import Client
import time
import paho.mqtt.client as mqtt

# Se debe colocar la IP del Server OPC UA al que se quiere conectar
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
   
    TIME = client.get_node("ns=2;i=4")
    TIME_Value = TIME.get_value()
    print(TIME_Value)

    # Publicar valores en los tópicos con prefijo "sensors/"
    client1.publish("sensors/temp", Temperature)
    client1.publish("sensors/press", Pressure)
    client1.publish("sensors/time", str(TIME_Value))  # Conversión a string
    
    time.sleep(1)
