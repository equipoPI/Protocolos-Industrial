
'''
Para iniciar el broker mosquito se necesita introducir el codigo:
C:\Program Files\mosquitto

mosquitto -c mosquitto.conf

mosquitto_sub -h ip_broker -t nombre_topico

mosquitto_pub -h ip_broker -t nombre_topico -m valor/dato
mosquitto_sub -h 192.168.0.111 -t "sensors/#"
'''
from opcua import Client
import time
import paho.mqtt.client as mqtt

# Función de callback para la conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente al broker MQTT")
    else:
        print("Fallo la conexión. Código de resultado:", rc)

# Se debe colocar la IP del Server OPC UA al que se quiere conectar
url = "opc.tcp://192.168.0.150:4840"

cliente_opc = Client(url)
cliente_opc.connect()
print("Cliente conectado al servidor OPC UA")

cliente_mqtt = mqtt.Client()
cliente_mqtt.on_connect = on_connect  # Asignamos la función de callback

#se debe de colocar la IP del Broker Mqtt con el cual se quiere comunicar
cliente_mqtt.connect("192.168.0.111", 1883, 60)

# Iniciar el bucle para mantener la conexión MQTT activa
cliente_mqtt.loop_start()

while True:
    # Obtener los valores de los sensores desde el servidor OPC UA y los muestra en la terminal
    temp = cliente_opc.get_node("ns=2;i=2")
    temperatura = temp.get_value()
    print("Temperatura:", temperatura)
    
    pres = cliente_opc.get_node("ns=2;i=3")
    presion = pres.get_value()
    print("Presión:", presion)
   
    tiempo = cliente_opc.get_node("ns=2;i=4")
    valor_tiempo = tiempo.get_value()
    print("Tiempo:", valor_tiempo)

    # Publicar los valores en los tópicos con el prefijo "sensores/"
    cliente_mqtt.publish("sensores/temp", temperatura)
    cliente_mqtt.publish("sensores/pres", presion)
    cliente_mqtt.publish("sensores/tiempo", str(valor_tiempo))  # Convertir valor_tiempo a string
    
    # Mostrar los valores enviados al broker MQTT en la terminal 
    print(f"Enviado al broker MQTT: Temp = {temperatura}, Pres = {presion}, Tiempo = {valor_tiempo}")
    
    time.sleep(1)

    '''Protocolos-Industrial\

        ver broker de internet y diferencias de la ip
        ver de la caida de los dispositivos que conforman la red
        '''


