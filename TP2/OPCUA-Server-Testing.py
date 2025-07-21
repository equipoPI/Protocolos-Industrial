from opcua import Server
from random import randint
import datetime  # Asegúrate de importar datetime
import time

#para que sea ejecutable en rasberry
'''
introducir este comando con en conjunto con la instalacion del archivo "requirements.txt" para que funcione correctamente
sudo apt-get install libxml2-dev libxmlsec1-dev libffi-dev

en una de las rasberrys de prueba instalamos todo esto dentro de un entorno virtual

el entorno virtual se habilita con:
source myenv/bin/activate

'''

server = Server()

#configura el endpoint del servidor. Es el punto de conexión donde los clientes se van a comunicar
url = "opc.tcp://10.0.6.242:4840"
server.set_endpoint(url)

name = "OPCUA_TESTING"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
    Temperature = randint(10, 50)
    Pressure = randint(200, 999)
    TIME = datetime.datetime.now()

    print(Temperature, Pressure, TIME)

    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(TIME)

    time.sleep(2)