# Script para integrar servidor OPC UA y maestro MODBUS RTU.
# Permite controlar y monitorear variables entre Python y Arduino usando OPC UA y MODBUS.
# Para ejecutarlo: python3 /home/lautaro/Proyects/Protocolos-Industrial/TP3/Arduino-Raspberry/M_MODBUS_S_OPCUA.py

from opcua import Server
import datetime
import time
import serial
import struct
import json

# ======================================================
# ========== CONFIG. SERVIDOR OPC UA INTEGRADO =========
# ======================================================


# ========== CONFIGURACIÓN DEL SERVIDOR OPC UA ==========
# Se crea el servidor OPC UA y se definen las variables que serán compartidas con el cliente Python y Arduino.
server = Server()

# Endpoint: Dirección donde el servidor OPC estará disponible
url = "opc.tcp://192.168.0.150:4840"  # Cambia la IP si tu servidor está en otra máquina
server.set_endpoint(url)

# Namespace: espacio de nombres personalizado para tus variables
name = "Servidor_OPCUA_Modbus"
addspace = server.register_namespace(name)

# Nodo raíz de objetos del servidor
node = server.get_objects_node()

# Crear objeto "Parametros" que contendrá las variables compartidas
Parametros = node.add_object(addspace, "Parametros_Modbus")

# Crear variables y hacerlas editables desde el servidor OPC UA
Reg1 = Parametros.add_variable(addspace, "Registro1_PWM_LED1", 0)  # PWM LED 1
Reg2 = Parametros.add_variable(addspace, "Registro2_PWM_LED2", 0)  # PWM LED 2
Reg3 = Parametros.add_variable(addspace, "Registro3_Digital1", 0)  # Salida digital 1
Reg4 = Parametros.add_variable(addspace, "Registro4_Luz", 0)       # Sensor de luz
Reg5 = Parametros.add_variable(addspace, "Registro5_Pote", 0)      # Potenciómetro
Reg6 = Parametros.add_variable(addspace, "Registro6_Digital2", 0)  # Salida digital 2
Reg7 = Parametros.add_variable(addspace, "Registro7_NC1", 0)       # Entrada digital 1
Reg8 = Parametros.add_variable(addspace, "Registro8_NC2", 0)       # Entrada digital 2

# Variable para guardar la hora de la última actualización
Hora = Parametros.add_variable(addspace, "Hora", datetime.datetime.now())
Hora.set_writable()

# Variable para guardar la hora de la última actualización
EMOD = Parametros.add_variable(addspace, "EMOD", datetime.datetime.now())
Hora.set_writable()

# Hacer todas las variables principales escribibles desde el cliente OPC UA
for var in [Reg1, Reg2, Reg3, Reg4, Reg5, Reg6, Reg7, Reg8]:
    var.set_writable()


# Iniciar el servidor OPC UA
server.start()
print(f"✅ Servidor OPC UA iniciado en {url}")

# ================================================
# ========== CONFIG. MAESTRO MODBUS RTU ==========
# ================================================


# -------- CONFIGURACIÓN GENERAL MODBUS --------

# Variables globales para almacenar las lecturas de los registros MODBUS
# Se conservan los valores anteriores si ocurre un error de lectura
Registro1 = 0  # PWM LED 1
Registro2 = 0  # PWM LED 2
Registro3 = 0  # Entrada Digital 1
Registro4 = 0  # Sensor de luz analógico
Registro5 = 0  # Potenciómetro
Registro6 = 0  # Entrada Digital 2
Registro7 = 0  # Sensor de presión 1
Registro8 = 0  # Sensor de presión 2


# -------- FUNCIÓN PARA CALCULAR CRC16 (MODBUS) --------
# Calcula el CRC16 para verificar la integridad de las tramas MODBUS
def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            lsb = crc & 0x0001
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc


# -------- Configuración del Puerto Serial --------
# Configura el puerto serial para comunicar con Arduino por MODBUS RTU
puerto = '/dev/ttyACM0'  # Cambia si usás otro puerto (ver con ls /dev/tty*)
baudrate = 9600
ser = serial.Serial(puerto, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=1)
modbus_conectado = True
time.sleep(3)  # Espera a que se estabilice la conexión tras abrir el puerto


# -------- Leer un registro MODBUS (con reintentos si falla la comunicación o CRC) --------
# Lee el valor de un registro MODBUS y verifica la respuesta y el CRC
def leer_entrada(registro):
    slave_addr = 0x03  # Dirección del esclavo MODBUS
    function = 0x03    # Código de función: lectura de holding register
    start_addr = registro
    quantity = 0x0001  # Solo se lee 1 registro

    # Construcción de la trama de solicitud MODBUS
    frame = bytearray()
    frame.append(slave_addr)
    frame.append(function)
    frame += start_addr.to_bytes(2, byteorder='big')
    frame += quantity.to_bytes(2, byteorder='big')

    crc = calc_crc(frame)
    frame += crc.to_bytes(2, byteorder='little')  # CRC en orden little-endian

    print(f"\n📤 Trama enviada (lectura reg {registro}):")
    for i, b in enumerate(frame):
        print(f"  Byte {i}: {format(b, '08b')}")

    intento = 0
    max_intentos = 5

    while intento < max_intentos:
        ser.reset_input_buffer()
        ser.write(frame)
        time.sleep(0.1)

        respuesta = ser.read(7)  # Esperamos 7 bytes (respuesta esperada)

        if len(respuesta) < 7:
            print(f"⚠️  Respuesta incompleta ({len(respuesta)} bytes): {[format(b, '08b') for b in respuesta]}")
            intento += 1
            continue

        print(f"📥 Respuesta recibida (lectura reg {registro}):")
        for i, b in enumerate(respuesta):
            print(f"  Byte {i}: {format(b, '08b')}")

        # Verificar dirección y función de la respuesta
        if respuesta[0] != slave_addr or respuesta[1] != function:
            print("⚠️  Cabecera incorrecta. Reintentando...")
            intento += 1
            continue

        # Verificación de CRC de la respuesta
        crc_recibido = int.from_bytes(respuesta[-2:], byteorder='little')
        crc_calculado = calc_crc(respuesta[:-2])

        print(f"🔐 CRC recibido:  {format(crc_recibido, '016b')}")
        print(f"🔐 CRC calculado: {format(crc_calculado, '016b')}")

        if crc_recibido == crc_calculado:
            valor = int.from_bytes(respuesta[3:5], byteorder='big')
            print(f"✅ Valor leído (reg {registro}): {valor}  (binario: {format(valor, '016b')})")
            return valor
        else:
            print("❌ CRC incorrecto. Reintentando...")
            intento += 1
            time.sleep(0.2)

    print("❌ Error: No se pudo leer correctamente tras varios intentos.")
    return None  # Devuelve None si no se obtuvo una lectura válida


# -------- Función para escribir en cualquier registro MODBUS --------
# Escribe un valor en cualquier registro MODBUS especificado
def escribir_valor_modbus(registro, valor):
    slave_addr = 0x03
    function = 0x06  # Código de función: escritura en registro único
    reg_addr = registro

    frame = bytearray()
    frame.append(slave_addr)
    frame.append(function)
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += valor.to_bytes(2, byteorder='big')

    crc = calc_crc(frame)
    frame += crc.to_bytes(2, byteorder='little')

    print(f"\n📤 Trama enviada (escritura reg {registro}):")
    for i, b in enumerate(frame):
        print(f"  Byte {i}: {format(b, '08b')}")

    intento = 0
    max_intentos = 5

    while intento < max_intentos:
        ser.reset_input_buffer()
        ser.write(frame)
        time.sleep(0.1)

        respuesta = ser.read(8)

        if len(respuesta) < 8:
            print(f"⚠️  Respuesta incompleta ({len(respuesta)} bytes): {[format(b, '08b') for b in respuesta]}")
            intento += 1
            continue

        print("📥 Respuesta recibida (escritura):")
        for i, b in enumerate(respuesta):
            print(f"  Byte {i}: {format(b, '08b')}")

        # Verificar dirección y función de la respuesta
        if respuesta[0] != slave_addr or respuesta[1] != function:
            print("⚠️  Cabecera incorrecta. Reintentando...")
            intento += 1
            continue

        # Verificación de CRC de la respuesta
        crc_recibido = int.from_bytes(respuesta[-2:], byteorder='little')
        crc_calculado = calc_crc(respuesta[:-2])

        print(f"🔐 CRC recibido:  {format(crc_recibido, '016b')}")
        print(f"🔐 CRC calculado: {format(crc_calculado, '016b')}")

        if crc_recibido == crc_calculado:
            print("✅ Comando de escritura confirmado por esclavo.")
            return
        else:
            print("❌ CRC incorrecto en respuesta de escritura. Reintentando...")
            intento += 1
            time.sleep(0.2)

    print("❌ Error: No se pudo confirmar la escritura tras varios intentos.")


# -------- LOOP PRINCIPAL --------
# En este loop se sincronizan los datos entre OPC UA y MODBUS:
# 1. Se reciben comandos desde OPC UA y se escriben en los registros MODBUS (PWM y digitales)
# 2. Se leen sensores desde MODBUS y se actualizan los nodos OPC UA para monitoreo web
# MQTT para publicar estado de MODBUS

try:
    while True:
        modbus_conectado = True
        try:
            # 1. Recibir comandos desde OPC UA y escribirlos en MODBUS (PWM y Digitales)
            pwm_led1 = Reg1.get_value()
            pwm_led2 = Reg2.get_value()
            digital1 = Reg3.get_value()
            digital2 = Reg6.get_value()

            # Escribir PWM_LED1 (registro 1)
            escribir_valor_modbus(1, int(pwm_led1))
            # Escribir PWM_LED2 (registro 2)
            escribir_valor_modbus(2, int(pwm_led2))
            # Escribir Digital1 (registro 3)
            escribir_valor_modbus(3, int(digital1))
            # Escribir Digital2 (registro 6)
            escribir_valor_modbus(6, int(digital2))

            # 2. Leer sensores y salidas digitales desde MODBUS y actualizar OPC UA
            r3 = leer_entrada(3);  Registro3 = r3 if r3 is not None else Registro3  # Salida digital 1
            r4 = leer_entrada(4);  Registro4 = r4 if r4 is not None else Registro4  # Luz
            r5 = leer_entrada(5);  Registro5 = r5 if r5 is not None else Registro5  # Pote
            r6 = leer_entrada(6);  Registro6 = r6 if r6 is not None else Registro6  # Salida digital 2
            r7 = leer_entrada(7);  Registro7 = r7 if r7 is not None else Registro7  # NC1
            r8 = leer_entrada(8);  Registro8 = r8 if r8 is not None else Registro8  # NC2

            Reg3.set_value(Registro3)  # Salida digital 1
            Reg4.set_value(Registro4)  # Luz
            Reg5.set_value(Registro5)  # Pote
            Reg6.set_value(Registro6)  # Salida digital 2
            Reg7.set_value(Registro7)  # NC1
            Reg8.set_value(Registro8)  # NC2
            # Actualizar la hora de la última actualización 
            hora_OPCUA = datetime.datetime.now()
            Hora.set_value(hora_OPCUA)
            print(f"  Hora enviada por OPC UA: {hora_OPCUA}")
            # Estado de coneccion de comunicacion MODBUS
            EMOD.set_value(modbus_conectado)

            # Mostrar en consola para monitoreo
            print(f"[{datetime.datetime.now()}] Actualizando OPC UA:")
            print(f"  PWM LED1: {pwm_led1} | PWM LED2: {pwm_led2}")
            print(f"  Digital1: {digital1} | Digital2: {digital2}")
            print(f"  Luz: {Registro4} | Pote: {Registro5}")
            print(f"  NC1: {Registro7} | NC2: {Registro8}")
            print()
            time.sleep(2)

        except serial.serialutil.SerialException as se:
            print(f"[ERROR] SerialException: {se}")
            modbus_conectado = False
            # Intentar reconectar el puerto serie cada 5 segundos
            while not modbus_conectado:
                print("Intentando reconectar el puerto serie...")
                try:
                    ser.close()
                except:
                    pass
                try:
                    ser = serial.Serial(puerto, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=1)
                    time.sleep(3)
                    print("¡Puerto serie reconectado!")
                    modbus_conectado = True
                except Exception as e:
                    print(f"No se pudo reconectar: {e}")
                    time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Finalizando programa por interrupción del usuario.")
    print("⛔ Servidor detenido por el usuario.")
    ser.close()

finally:
    server.stop()
