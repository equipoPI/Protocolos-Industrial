# Protocolos-Industrial

Este repositorio contiene los trabajos y desarrollos prácticos de la materia Protocolos de Comunicación Industrial.

## Estructura de carpetas

- **Act1/**: Material y entregables de la Actividad Nº1 (manuales, informes, PDFs).
- **TP1/**: Práctico 1 sobre MODBUS. Incluye:
  - Documentación y guías de referencia (PDFs).
  - Ejemplos de código Arduino y macros para pantallas Weintek.
  - Carpeta `Librerias Arduino/` con librerías MODBUS para Arduino.
- **TP2/**: Práctico 2 sobre OPC UA y MQTT. Incluye:
  - Scripts Python para clientes y servidores OPC UA y MQTT.
  - Ejemplos de comunicación y pruebas.
  - Documentos explicativos y PDFs.
- **TP3/**: Práctico integrador MODBUS-OPC-UA-MQTT. Incluye:
  - Carpeta `CodigoFinal/` con los scripts principales:
    - `S_MODBUS_OPCUA.py`: Servidor OPC UA que integra y sincroniza datos con Arduino vía MODBUS RTU.
    - `S_OPC_MQTT.py`: Cliente OPC UA que publica y recibe datos por MQTT, permitiendo monitoreo y control desde la web.
    - `interface.html`: Interfaz web para monitoreo y control en tiempo real usando MQTT/WebSocket.
  - Ejemplos de código para Arduino y Raspberry Pi.
  - Documentos de informe y PDFs.

## Funcionalidades principales

- **Integración de protocolos industriales:**
  - MODBUS RTU (Arduino ↔ Python)
  - OPC UA (Servidor Python ↔ Cliente Python)
  - MQTT (Python ↔ Broker EMQX ↔ Web)
- **Monitoreo y control remoto:**
  - Visualización de sensores y estados digitales/analógicos desde la web.
  - Envío de comandos desde la web hacia el sistema físico.
- **Ejemplos y documentación:**
  - Archivos PDF y DOCX con guías, informes y referencias técnicas.
  - Ejemplos de código para cada protocolo y plataforma.

## Ejemplo de flujo de datos

1. Arduino adquiere datos y responde por MODBUS RTU.
2. Python (S_MODBUS_OPCUA.py) sincroniza variables con Arduino y expone datos vía OPC UA.
3. Python (S_OPC_MQTT.py) publica los datos en MQTT y recibe comandos desde la web.
4. La web (interface.html) muestra los datos y permite controlar el sistema en tiempo real.

## Requisitos

- Python 3.x
- Librerías: `opcua`, `paho-mqtt`, etc.
- Broker MQTT público: [broker.emqx.io](https://www.emqx.com/en/online-mqtt)
- Arduino con librería MODBUS

---
Para más detalles, consulta los informes y la documentación en cada carpeta.