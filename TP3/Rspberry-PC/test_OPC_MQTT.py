

# Este script conecta un cliente OPC UA y un cliente MQTT para publicar y recibir datos entre ambos.
# Los datos publicados por MQTT pueden ser visualizados en una interfaz web (HTML) y controlados desde allí.
# El script también recibe comandos desde la web para controlar salidas digitales y analógicas.


# Importa el cliente OPC UA para conectarse al servidor
# Importa el cliente OPC UA para conectarse al servidor
from opcua import Client

# Importa módulo para demoras en el loop principal
import time
# Importa cliente MQTT para comunicación con el broker
import paho.mqtt.client as mqtt

# ----------------- Configuracion -----------------


# Dirección IP del servidor OPC UA (Raspberry Pi o PC)
opcua_url = "opc.tcp://192.168.0.150:4840"  # Cambia la IP si tu servidor OPC UA está en otra máquina

# Dirección IP del broker MQTT y puerto
mqtt_broker_ip = "192.168.0.112"  # Cambia esta IP por la del broker MQTT accesible desde ambas PCs
mqtt_broker_port = 1883  # Puerto por defecto de MQTT para Python (TCP)

# NOTA IMPORTANTE:
# El HTML debe conectarse a ws://<ip_broker>:9001 (WebSocket),
# este script debe seguir usando 1883 (TCP) a menos que uses una librería MQTT para WebSocket en Python.

# ----------------- Conexion OPC UA -----------------


# Crea una instancia del cliente OPC UA y se conecta al servidor
client_opcua = Client(opcua_url)
client_opcua.connect()
print("? Conectado al servidor OPC UA")

# ----------------- Conexion MQTT -----------------


# --- Callback para recibir comandos desde el HTML vía MQTT ---
import json
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"[MQTT] Mensaje recibido en {topic}: {payload}")
        data = json.loads(payload)

        # Procesa comandos para salidas digitales
        if topic.startswith("topicos/control/digital/"):
            salida = topic.split("/")[-1]
            valor = bool(data.get("value", False))
            # Mapear salida 1 -> Digital1, salida 2 -> Digital2
            if salida == "1":
                nodo = nodos.get("Digital1")
            elif salida == "2":
                nodo = nodos.get("Digital2")
            else:
                nodo = None
            if nodo:
                nodo.set_value(valor)
                print(f"[OPC UA] Salida digital {salida} actualizada a {valor}")

        # Procesa comandos para salidas analógicas
        elif topic.startswith("topicos/control/analog/"):
            salida = topic.split("/")[-1]
            valor = int(data.get("value", 0))
            # Mapear salida 1 -> PWM_LED1, salida 2 -> PWM_LED2
            if salida == "1":
                nodo = nodos.get("PWM_LED1")
            elif salida == "2":
                nodo = nodos.get("PWM_LED2")
            else:
                nodo = None
            if nodo:
                nodo.set_value(valor)
                print(f"[OPC UA] Salida analógica {salida} actualizada a {valor}")
    except Exception as e:
        print(f"[ERROR] Procesando mensaje MQTT: {e}")


# Crea una instancia del cliente MQTT y configura el callback para recibir mensajes
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Suscribirse a los tópicos de control para recibir comandos desde la web
client_mqtt.subscribe("topicos/control/digital/+")
client_mqtt.subscribe("topicos/control/analog/+")

print(f"? Conectado al broker MQTT en {mqtt_broker_ip}:{mqtt_broker_port}")

# ----------------- Obtencion de nodos OPC UA -----------------


# Diccionario de nodos OPC UA: cada clave es el nombre simbólico de la variable
# y el valor es el nodo OPC UA correspondiente. Los NodeId deben coincidir con los del servidor OPC UA.
nodos = {
    "PWM_LED1": client_opcua.get_node("ns=2;i=2"),   # Salida analógica 1 (PWM)
    "PWM_LED2": client_opcua.get_node("ns=2;i=3"),   # Salida analógica 2 (PWM)
    "Digital1": client_opcua.get_node("ns=2;i=4"),   # Salida digital 1
    "Luz":      client_opcua.get_node("ns=2;i=5"),   # Sensor de luz
    "Pote":     client_opcua.get_node("ns=2;i=6"),   # Potenciómetro
    "Digital2": client_opcua.get_node("ns=2;i=7"),   # Salida digital 2
    "NC1":      client_opcua.get_node("ns=2;i=8"),   # Entrada digital 1
    "NC2":      client_opcua.get_node("ns=2;i=9"),   # Entrada digital 2
    "Hora":     client_opcua.get_node("ns=2;i=10")   # Hora actual
}


# ----------------- Loop principal -----------------
# En este loop se publican los datos de sensores y entradas digitales a MQTT,
# y se procesan los comandos recibidos desde la web para actualizar los nodos OPC UA.
try:
    while True:
        print("?? Publicando datos...")

        # Publicar sensores analógicos (Luz y Pote) en MQTT
        for i, sensor in enumerate(["Luz", "Pote"], start=1):
            valor = nodos[sensor].get_value()
            print(f"  Sensor {i} ({sensor}): {valor}")
            payload = json.dumps({"value": valor, "unit": "V"})
            client_mqtt.publish(f"topicos/sensors/{i}", payload)

        # Publicar entradas digitales (NC1 y NC2) en MQTT
        for i, entrada in enumerate(["NC1", "NC2"], start=1):
            valor = nodos[entrada].get_value()
            print(f"  Entrada Digital {i} ({entrada}): {valor}")
            payload = json.dumps({"value": bool(valor)})
            client_mqtt.publish(f"topicos/inputs/{i}", payload)

        # Publicar estado de MODbus (status/modbus) en MQTT
        modbus_status = True  # Suponemos que si el script está corriendo, MODbus está conectado
        status_payload = json.dumps({"connected": modbus_status})
        client_mqtt.publish("topicos/status/modbus", status_payload)

        # Publicar estado de OPC UA (status/opc) en MQTT
        opc_status = True  # Suponemos que si el script está corriendo, OPC está conectado
        status_payload = json.dumps({"connected": opc_status})
        client_mqtt.publish("topicos/status/opc", status_payload)

        # Procesar mensajes entrantes (comandos de control)
        client_mqtt.loop(timeout=0.1)

        print()  # Línea en blanco para separar publicaciones
        time.sleep(2)  # Espera 2 segundos antes de la próxima lectura/publicación

# Si el usuario presiona Ctrl+C, se sale del loop principal
except KeyboardInterrupt:
    print("\n? Cliente detenido por el usuario.")

# ----------------- Finalización -----------------
# Al finalizar, se cierra la conexión con el servidor OPC UA de forma segura
finally:
    client_opcua.disconnect()
    print("?? Desconectado del servidor OPC UA")