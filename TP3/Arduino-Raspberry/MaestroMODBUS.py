import serial
import time
import struct

# -------- CRC16 (MODBUS) --------
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

# -------- Comunicación Serial --------
puerto = '/dev/ttyUSB0'  # O usa 'ttyACM0' si es necesario
baudrate = 9600

ser = serial.Serial(puerto, baudrate=baudrate, timeout=1)
time.sleep(2)  # Espera para que se estabilice la conexión

# -------- Enviar petición de lectura (función 0x03) --------
def leer_entrada():
    slave_addr = 0x01
    function = 0x03
    start_addr = 0x0000
    quantity = 0x0001

    frame = bytearray()
    frame.append(slave_addr)
    frame.append(function)
    frame += start_addr.to_bytes(2, byteorder='big')
    frame += quantity.to_bytes(2, byteorder='big')
    
    crc = calc_crc(frame)
    frame += crc.to_bytes(2, byteorder='little')

    ser.write(frame)
    respuesta = ser.read(7)  # Espera 7 bytes: addr + func + byte_count + 2 datos + 2 crc

    if len(respuesta) >= 7:
        crc_recibido = int.from_bytes(respuesta[-2:], byteorder='little')
        crc_calc = calc_crc(respuesta[:-2])
        if crc_recibido == crc_calc:
            valor = int.from_bytes(respuesta[3:5], byteorder='big')
            print(f"Valor leído desde A0: {valor}")
        else:
            print("CRC incorrecto")
    else:
        print("Sin respuesta o incompleta")

# -------- Enviar comando de escritura (función 0x06) --------
def encender_led(encender=True):
    slave_addr = 0x01
    function = 0x06
    reg_addr = 0x0001
    value = 0x0001 if encender else 0x0000

    frame = bytearray()
    frame.append(slave_addr)
    frame.append(function)
    frame += reg_addr.to_bytes(2, byteorder='big')
    frame += value.to_bytes(2, byteorder='big')
    
    crc = calc_crc(frame)
    frame += crc.to_bytes(2, byteorder='little')

    ser.write(frame)
    respuesta = ser.read(8)

    if len(respuesta) >= 8:
        crc_recibido = int.from_bytes(respuesta[-2:], byteorder='little')
        crc_calc = calc_crc(respuesta[:-2])
        if crc_recibido == crc_calc:
            print("Comando de escritura enviado correctamente.")
        else:
            print("CRC incorrecto en respuesta de escritura")
    else:
        print("Sin respuesta de escritura")

# -------- Main Loop --------
try:
    while True:
        leer_entrada()
        time.sleep(2)
        encender_led(encender=True)
        time.sleep(2)
        encender_led(encender=False)
        time.sleep(2)

except KeyboardInterrupt:
    print("Finalizando programa")
    ser.close()
