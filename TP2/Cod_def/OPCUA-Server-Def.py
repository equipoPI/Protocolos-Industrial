from opcua import Server
from random import randint
import datetime  
import time

#para que sea ejecutable en rasberry
'''
sudo apt-get install libxml2-dev libxmlsec1-dev libffi-dev
'''

server = Server()

#configura el endpoint del servidor. Es el punto de conexión donde los clientes se van a comunicar
url = "opc.tcp://192.168.0.150:4840"
server.set_endpoint(url)

name = "OPCUA_TESTING"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

#variables de los sensores 
Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
    #genera valores aleatorios para los sensores
    Temperature = randint(10, 50)
    Pressure = randint(200, 999)
    #obtiene el valor temporal del momento
    TIME = datetime.datetime.now()

    print(Temperature, Pressure, TIME)

    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(TIME)

    time.sleep(2)