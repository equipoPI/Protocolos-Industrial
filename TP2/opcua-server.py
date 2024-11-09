from asyncua import Server
import asyncio
import random #esto lo vamos a reemplazar con las variables q vamos a sensar

#funcion principal asincrona para ejecutar el servidor OPC UA
async def run_opcua_server():
    server = Server()
    #configura el endpoint del servidor. Es el punto de conexión donde los clientes se van a comunicar
    server.set_endpoint("opc.tcp://192.198.0.150:4840/freeopcua/server/")
    #espacio de nombre unico del servidor para distinguirlo de otros servidores OPC UA
    uri = "http://example.org"
    idx = server.register_namespace(uri)
    #objeto device que va a contener las variables simuladas
    device = server.nodes.objects.add_object(idx, "Device")

    analog_var1 = device.add_variable(idx, "AnalogSensor1", 0.0)
    analog_var2 = device.add_variable(idx, "AnalogSensor2", 0.0)

    digital_var1 = device.add_variable(idx, "DigitalSensor1", False)
    digital_var2 = device.add_variable(idx, "DigitalSensor2", False)

    #configura las variables para que los clientes puedan escribir en ellas
    analog_var1.set_writable()
    analog_var2.set_writable()
    digital_var1.set_writable()
    digital_var2.set_writable()

    #Inicia el server y ejecuta un bucle infinito
    async with server:
        print("Servidor OPC UA corriendo")
        while True:
            #acá irían los valores sensados (por ahora usamos random)
            analog_var1.set_value(random.uniform(20.0, 30.0))
            analog_var2.set_value(random.uniform(30.0, 40.0))
            digital_var1.set_value(random.choice([True, False]))
            digital_var2.set_value(random.choice([True, False]))

            #Pausa de 1 segundo antes de la siguiente iteración para actualizar valores
            await asyncio.sleep(1)


#Llama y ejecuta la función principal de servidor asíncrono
asyncio.run(run_opcua_server())








