import paho.mqtt.client as mqtt
from asyncua import Client
import asyncio

# Variables para la configuración de la Raspberry Pi y el broker MQTT
raspberry_pi_ip = "192.168.56.2"  # Cambia esto a la IP de tu Raspberry Pi
mqtt_broker_ip = raspberry_pi_ip  # Puedes usar la misma IP o cambiarla si es necesario
port = 1883
topic_analog1 = "sensors/analog1"
topic_analog2 = "sensors/analog2"
topic_digital1 = "sensors/digital1"
topic_digital2 = "sensors/digital2"

# Inicializar el cliente MQTT
mqtt_client = mqtt.Client(client_id="OPCUA_to_MQTT", clean_session=True)

# Conectar al broker MQTT
mqtt_client.connect(mqtt_broker_ip, port)

async def opcua_client():
    url = f"opc.tcp://{raspberry_pi_ip}:4840/freeopcua/server/"  # Usar la variable para la IP
    client = Client(url)

    try:
        await client.connect()
        print("Conectado al servidor OPC UA")

        root = client.get_root_node()
        analog_var1 = root.get_child(["0:Objects", "2:Device", "2:AnalogSensor1"])
        analog_var2 = root.get_child(["0:Objects", "2:Device", "2:AnalogSensor2"])
        digital_var1 = root.get_child(["0:Objects", "2:Device", "2:DigitalSensor1"])
        digital_var2 = root.get_child(["0:Objects", "2:Device", "2:DigitalSensor2"])

        while True:
            analog_value1 = await analog_var1.read_value()
            analog_value2 = await analog_var2.read_value()
            digital_value1 = await digital_var1.read_value()
            digital_value2 = await digital_var2.read_value()

            mqtt_client.publish(topic_analog1, analog_value1)
            mqtt_client.publish(topic_analog2, analog_value2)
            mqtt_client.publish(topic_digital1, int(digital_value1))
            mqtt_client.publish(topic_digital2, int(digital_value2))

            print(f"Publicado en MQTT: Analog1={analog_value1}, Analog2={analog_value2}")
            print(f"Publicado en MQTT: Digital1={digital_value1}, Digital2={digital_value2}")
            await asyncio.sleep(1)

    finally:
        await client.disconnect()
        mqtt_client.disconnect()

# Ejecutar el cliente OPC UA
asyncio.run(opcua_client())
