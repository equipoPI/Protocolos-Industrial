/*
    ModbusUDP2.cpp - Source for Modbus UDP2 Library
    Copyright (C) 2016 wvengen
*/
#include "ModbusUDP2.h"

ModbusUDP::ModbusUDP() {
}

void ModbusUDP::config(uint8_t *mac) {
    Ethernet.begin(mac);
    _udp.begin(MODBUSIP_PORT);
}

void ModbusUDP::config(uint8_t *mac, IPAddress ip) {
    Ethernet.begin(mac, ip);
    _udp.begin(MODBUSIP_PORT);
}

void ModbusUDP::config(uint8_t *mac, IPAddress ip, IPAddress dns) {
    Ethernet.begin(mac, ip, dns);
    _udp.begin(MODBUSIP_PORT);
}

void ModbusUDP::config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway) {
    Ethernet.begin(mac, ip, dns, gateway);
    _udp.begin(MODBUSIP_PORT);
}

void ModbusUDP::config(uint8_t *mac, IPAddress ip, IPAddress dns, IPAddress gateway, IPAddress subnet) {
    Ethernet.begin(mac, ip, dns, gateway, subnet);
    _udp.begin(MODBUSIP_PORT);
}

void ModbusUDP::task() {
    _udp.parsePacket();

    if (_udp.available()) {
        _udp.read(_MBAP, 7); //MBAP length has 7 bytes size
        _len = _MBAP[4] << 8 | _MBAP[5];
        _len--;  // Do not count with last byte from MBAP

        if (_MBAP[2] !=0 || _MBAP[3] !=0) return;  //Not a MODBUSIP packet
        if (_len > MODBUSIP_MAXFRAME) return;      //Length is over MODBUSIP_MAXFRAME

        _frame = (byte*) malloc(_len);
        _udp.read(_frame, _len);

        this->receivePDU(_frame);
        if (_reply != MB_REPLY_OFF) {
            _MBAP[4] = (_len+1) >> 8;     //_len+1 for last byte from MBAP
            _MBAP[5] = (_len+1) & 0x00FF;

            _udp.beginPacket(_udp.remoteIP(), _udp.remotePort());
            _udp.write(_MBAP, 7);
            _udp.write(_frame, _len);
            _udp.endPacket();
        }

        free(_frame);
        _len = 0;
    }
}

void ModbusMasterUDP::config() {
    _master.begin(MODBUSIP_MASTER_PORT);
}

void ModbusMasterUDP::send(IPAddress ip) {
    frameMBAP(_len);
    _master.beginPacket(ip, MODBUSIP_PORT);
    _master.write(_MBAP, 7 + _len);
    _master.endPacket();
}
