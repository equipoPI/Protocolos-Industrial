
'''
mosquitto_sub -h ip_broker -t "sensors/#"

lo que hace ese comando es captar todos los topicos que esta sociados al grupo sensors, si se cambia #
por el nombre de un topico se mostrara ese solo
'''

# Importa el cliente OPC UA para conectarse al servidor
from opcua import Client
# Importa modulo para demoras en el loop
import time
# Importa cliente MQTT
import paho.mqtt.client as mqtt

# ----------------- Configuracion -----------------

# Direccion IP del servidor OPC UA (Raspberry Pi o PC)
opcua_url = "opc.tcp://192.168.0.150:4840"

# Direccion IP del broker MQTT y puerto
mqtt_broker_ip = "192.168.0.112"
mqtt_broker_port = 1883  # Puerto por defecto de MQTT

# ----------------- Conexion OPC UA -----------------

# Crea una instancia del cliente OPC UA y se conecta al servidor
client_opcua = Client(opcua_url)
client_opcua.connect()
print("? Conectado al servidor OPC UA")

# ----------------- Conexion MQTT -----------------

# Crea una instancia del cliente MQTT y se conecta al broker
client_mqtt = mqtt.Client()
client_mqtt.connect(mqtt_broker_ip, mqtt_broker_port, 60)
print(f"? Conectado al broker MQTT en {mqtt_broker_ip}:{mqtt_broker_port}")

# ----------------- Obtencion de nodos OPC UA -----------------

# Define un diccionario donde cada clave es un nombre simbolico de la variable
# y el valor es el nodo OPC UA al que corresponde
# Los NodeId deben coincidir con los del servidor OPC UA que hayas definido
nodos = {
    "PWM_LED1": client_opcua.get_node("ns=2;i=2"),
    "PWM_LED2": client_opcua.get_node("ns=2;i=3"),
    "Digital1": client_opcua.get_node("ns=2;i=4"),
    "Luz":      client_opcua.get_node("ns=2;i=5"),
    "Pote":     client_opcua.get_node("ns=2;i=6"),
    "Digital2":  client_opcua.get_node("ns=2;i=7"),
    "NC1":      client_opcua.get_node("ns=2;i=8"),
    "NC2":      client_opcua.get_node("ns=2;i=9"),
    "Hora":     client_opcua.get_node("ns=2;i=10")
}

# ----------------- Loop principal -----------------

try:
    while True:
        print("?? Publicando datos...")

        # Recorre cada variable del servidor OPC UA
        for nombre, nodo in nodos.items():
            valor = nodo.get_value()  # Obtiene su valor actual
            print(f"  {nombre}: {valor}")  # Lo muestra en consola

            # Publica el valor en un topico MQTT con formato: topicos/nombre_variable
            # Ejemplo: topicos/pwm_led1
            client_mqtt.publish(f"topicos/{nombre.lower()}", str(valor))

        print()  # Lonea en blanco para separar publicaciones
        time.sleep(2)  # Espera 2 segundos antes de la proxima lectura/publicacion

# Si el usuario presiona Ctrl+C, se sale del loop
except KeyboardInterrupt:
    print("\n? Cliente detenido por el usuario.")

# ----------------- Finalizacion -----------------

finally:
    # Cierra la conexion con el servidor OPC UA de forma segura
    client_opcua.disconnect()
    print("?? Desconectado del servidor OPC UA")

