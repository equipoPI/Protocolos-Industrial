
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
mqtt_broker_ip = "192.168.0.112"  # Cambia esta IP por la del broker MQTT accesible desde ambas PCs
mqtt_broker_port = 1883  # Puerto por defecto de MQTT para Python (TCP)

# NOTA: El HTML debe conectarse a ws://<ip_broker>:9001 (WebSocket),
# este script debe seguir usando 1883 (TCP) a menos que uses una librería MQTT para WebSocket en Python.

# ----------------- Conexion OPC UA -----------------

# Crea una instancia del cliente OPC UA y se conecta al servidor
client_opcua = Client(opcua_url)
client_opcua.connect()
print("? Conectado al servidor OPC UA")

# ----------------- Conexion MQTT -----------------

# Crea una instancia del cliente MQTT y se conecta al broker

# --- Callback para recibir comandos desde el HTML ---
import json
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"[MQTT] Mensaje recibido en {topic}: {payload}")
        data = json.loads(payload)

        # Salidas digitales
        if topic.startswith("topicos/control/digital/"):
            salida = topic.split("/")[-1]
            valor = bool(data.get("value", False))
            # Mapear salida 1 -> PWM_LED1, salida 2 -> PWM_LED2 (ajusta según tu OPC UA)
            if salida == "1":
                nodo = nodos.get("PWM_LED1")
            elif salida == "2":
                nodo = nodos.get("PWM_LED2")
            else:
                nodo = None
            if nodo:
                nodo.set_value(valor)
                print(f"[OPC UA] Salida digital {salida} actualizada a {valor}")

        # Salidas analógicas
        elif topic.startswith("topicos/control/analog/"):
            salida = topic.split("/")[-1]
            valor = int(data.get("value", 0))
            # Mapear salida 1 -> Pote, salida 2 -> Luz (ajusta según tu OPC UA)
            if salida == "1":
                nodo = nodos.get("Pote")
            elif salida == "2":
                nodo = nodos.get("Luz")
            else:
                nodo = None
            if nodo:
                nodo.set_value(valor)
                print(f"[OPC UA] Salida analógica {salida} actualizada a {valor}")
    except Exception as e:
        print(f"[ERROR] Procesando mensaje MQTT: {e}")

client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Suscribirse a los tópicos de control
client_mqtt.subscribe("topicos/control/digital/+")
client_mqtt.subscribe("topicos/control/analog/+")

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

        # Publicar sensores analógicos (PWM_LED1 y PWM_LED2)
        for i, sensor in enumerate(["PWM_LED1", "PWM_LED2"], start=1):
            valor = nodos[sensor].get_value()
            print(f"  Sensor {i} ({sensor}): {valor}")
            payload = json.dumps({"value": valor, "unit": "V"})
            client_mqtt.publish(f"topicos/sensors/{i}", payload)

        # Publicar entradas digitales (Digital1 y Digital2)
        for i, entrada in enumerate(["Digital1", "Digital2"], start=1):
            valor = nodos[entrada].get_value()
            print(f"  Entrada Digital {i} ({entrada}): {valor}")
            payload = json.dumps({"value": bool(valor)})
            client_mqtt.publish(f"topicos/inputs/{i}", payload)

        # Publicar estado de MODbus (status/modbus)
        modbus_status = True  # Suponemos que si el script está corriendo, MODbus está conectado
        status_payload = json.dumps({"connected": modbus_status})
        client_mqtt.publish("topicos/status/modbus", status_payload)

        # Publicar estado de OPC (status/opc)
        opc_status = True  # Suponemos que si el script está corriendo, OPC está conectado
        status_payload = json.dumps({"connected": opc_status})
        client_mqtt.publish("topicos/status/opc", status_payload)

        # Procesar mensajes entrantes (comandos)
        client_mqtt.loop(timeout=0.1)

        print()  # Línea en blanco para separar publicaciones
        time.sleep(2)  # Espera 2 segundos antes de la próxima lectura/publicación

# Si el usuario presiona Ctrl+C, se sale del loop
except KeyboardInterrupt:
    print("\n? Cliente detenido por el usuario.")

# ----------------- Finalizacion -----------------

finally:
    # Cierra la conexion con el servidor OPC UA de forma segura
    client_opcua.disconnect()
    print("?? Desconectado del servidor OPC UA")