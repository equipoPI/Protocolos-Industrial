/*
    ModbusIP.h - Header for Modbus IP Library
    Copyright (C) 2015 André Sarmento Barbosa
*/
#include <Arduino.h>
#include <Modbus.h>
#include <SPI.h>
#include <Ethernet.h>

#ifndef MODBUSIP_H
#define MODBUSIP_H

#ifndef MODBUSIP_PORT
  #define MODBUSIP_PORT          502
#endif
#ifndef MODBUSIP_MAXFRAME
  #define MODBUSIP_MAXFRAME      200
#endif

//#define TCP_KEEP_ALIVE

class ModbusIP : public Modbus {
    private:
        EthernetServer _server;
        byte _MBAP[7];

    public:
        ModbusIP();
        void config(uint8_t *mac);
        void config(uint8_t *mac, IPAddress ip);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway, IPAddress subnet);
        void task();
};

class ModbusMasterIP : public ModbusMaster {
    private:
        EthernetClient _client;
        void send(IPAddress ip);

    public:
        void config() {} /* no config required */

        inline void sendHreg(IPAddress ip, word offset, word value) {
            frameHreg(offset, value);
            send(ip);
        }

        inline void sendCoil(IPAddress ip, word offset, bool value) {
            frameCoil(offset, value);
            send(ip);
        }
};

#endif //MODBUSIP_H

