
from opcua import Server
import datetime
import time
from MaestroMODBUS import Registro1, Registro2, Registro3, Registro4, Registro5, Registro6, Registro7, Registro8

# IMPORTANTE:
# Este script debe ejecutarse *después* de haber leído los registros MODBUS
# y haber asignado sus valores a variables como Registro1, Registro2, etc.

# Asegurate de que las siguientes variables existan:
# Registro1 a Registro8
# Si este script está en otro archivo, debés importarlas o compartirlas

# Configuración del servidor OPC UA
server = Server()

# Endpoint: Dirección donde el servidor OPC estará disponible
url = "opc.tcp://192.168.0.150:4840"
server.set_endpoint(url)

# Namespace: espacio de nombres personalizado para tus variables
name = "Servidor_OPCUA_Modbus"
addspace = server.register_namespace(name)

# Nodo raíz de objetos del servidor
node = server.get_objects_node()

# Crear objeto "Parametros" que contendrá las variables
Parametros = node.add_object(addspace, "Parametros_Modbus")

# Crear variables y hacerlas editables desde el servidor
Reg1 = Parametros.add_variable(addspace, "Registro1_PWM_LED1", 0)
Reg2 = Parametros.add_variable(addspace, "Registro2_PWM_LED2", 0)
Reg3 = Parametros.add_variable(addspace, "Registro3_Digital1", 0)
Reg4 = Parametros.add_variable(addspace, "Registro4_Luz", 0)
Reg5 = Parametros.add_variable(addspace, "Registro5_Pote", 0)
Reg6 = Parametros.add_variable(addspace, "Registro6_Reserva", 0)
Reg7 = Parametros.add_variable(addspace, "Registro7_NC", 0)
Reg8 = Parametros.add_variable(addspace, "Registro8_NC", 0)

# Otras variables útiles
Hora = Parametros.add_variable(addspace, "Hora", datetime.datetime.now())
Hora.set_writable()

# Hacer todas las variables escribibles
for var in [Reg1, Reg2, Reg3, Reg4, Reg5, Reg6, Reg7, Reg8]:
    var.set_writable()

# Iniciar el servidor
server.start()
print(f"✅ Servidor OPC UA iniciado en {url}")

try:
    while True:
        # Simular que estos valores ya fueron actualizados desde la lectura Modbus
        # Asegurate de que las variables Registro1 a Registro8 existan en el entorno

        # Asignar los valores actuales al servidor OPC UA
        Reg1.set_value(Registro1)
        Reg2.set_value(Registro2)
        Reg3.set_value(Registro3)
        Reg4.set_value(Registro4)
        Reg5.set_value(Registro5)
        Reg6.set_value(Registro6)
        Reg7.set_value(Registro7)
        Reg8.set_value(Registro8)

        Hora.set_value(datetime.datetime.now())

        # Mostrar en consola para monitoreo
        print(f"[{datetime.datetime.now()}] Publicando:")
        print(f"  PWM LED1: {Registro1} | PWM LED2: {Registro2}")
        print(f"  Digital1: {Registro3} | Luz: {Registro4}")
        print(f"  Pote: {Registro5} | Reserva: {Registro6}")
        print(f"  NC1: {Registro7} | NC2: {Registro8}")
        print()

        time.sleep(2)  # Actualizar cada 2 segundos

except KeyboardInterrupt:
    print("⛔ Servidor detenido por el usuario.")

finally:
    server.stop()
