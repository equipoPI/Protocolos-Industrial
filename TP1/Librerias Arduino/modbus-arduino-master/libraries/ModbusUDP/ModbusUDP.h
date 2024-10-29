/*
    ModbusUDP.h - Header for Modbus UDP Library
    Copyright (C) 2016 wvengen
    Copyright (C) 2015 André Sarmento Barbosa
*/
#include <Arduino.h>
#include <Modbus.h>
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

#ifndef MODBUSUDP_H
#define MODBUSUDP_H

#ifndef MODBUSIP_PORT
  #define MODBUSIP_PORT          502
#endif
#ifndef MODBUSIP_MASTER_PORT
  #define MODBUSIP_MASTER_PORT 10502
#endif
#ifndef MODBUSIP_MAXFRAME
  #define MODBUSIP_MAXFRAME      200
#endif

class ModbusUDP : public Modbus {
    private:
        EthernetUDP _udp;
        byte _MBAP[7];

    public:
        ModbusUDP();
        void config(uint8_t *mac);
        void config(uint8_t *mac, IPAddress ip);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway);
        void config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway, IPAddress subnet);
        void task();
};

class ModbusMasterUDP : public ModbusMaster {
    private:
        EthernetUDP _master;
        void send(IPAddress ip);

    public:
        void config();

        inline void sendHreg(IPAddress ip, word offset, word value) {
            frameHreg(offset, value);
            send(ip);
        }

        inline void sendCoil(IPAddress ip, word offset, bool value) {
            frameCoil(offset, value);
            send(ip);
        }
};

#endif /* MODBUSUDP_H */

