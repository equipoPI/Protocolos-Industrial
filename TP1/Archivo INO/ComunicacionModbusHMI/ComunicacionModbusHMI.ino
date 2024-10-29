#include <ModbusRtu.h>
#include <SoftwareSerial.h>    //libreria que usaremos para transmitir y recibir los datos que llegan desde el modulo bluetooth

int BT_Rx = 12;   //DO            //pines conectados al modulo bluetooth {cambiar la conexion al 10  y al 11 que son los que funcionaron en el practivo de comunicaicon de datos}
int BT_Tx = 11;   //DI

#define ID 3 //0 si lo usamos como maestro 1 a 247 si lo usamos como esclavo
#define RS485_CONTROL_PIN 4 // Pin de control para habilitar transmisión y recepción RS485

#define pinLedSalida 12
#define pinLectDigital 11
#define pinLectAnalog 1
#define pinPWM 9

Modbus slave(ID, 0, 1);
//ID
//configuración del puerto serial donde 0 corresponde a tx como 1 y rx como 0
//0 si usamos el puerto como RS232, 1 0 mayor si usamos RS485

int8_t state = 0; //variable para verificar la conexión modbus
unsigned long tempus; //para determinar el tiempo de conexión modbus

uint16_t au16data[5]; //nombre de la varriable de la tabla de registros modbus que queremos compartir

void setup() {

  configuracionIO();

  pinMode(RS485_CONTROL_PIN, OUTPUT);  // Configura el pin de control como salida
  digitalWrite(RS485_CONTROL_PIN, LOW);  // Comienza en modo recepción (LOW)

  slave.begin(9600);
  tempus = millis() + 1000;
  digitalWrite(13, HIGH );

  pinMode(pinLedSalida, OUTPUT);
  pinMode(pinLectDigital, INPUT);
  pinMode(pinPWM, OUTPUT);
  pinMode(pinLectAnalog, INPUT);

}

void loop() {

  digitalWrite(RS485_CONTROL_PIN, HIGH);  // Habilita transmisión (envía datos)
  state = slave.poll( au16data, 5 );
  digitalWrite(RS485_CONTROL_PIN, LOW);   // Habilita recepción


  if (state > 4) {
    tempus = millis() + 1000;
    digitalWrite(13, HIGH);
  }
  if (millis() > tempus) digitalWrite(13, LOW );

  MapeoIOmodbus(); //aca vamos a actualizar los datos de intercambio
}


void configuracionIO() { //pines de entrada y salida que vamos a usar del arduino
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);

  digitalWrite(2, LOW );

  analogWrite(pinPWM, 0 ); //PWM 0%
}

/*********************************************************
  Enlaza la tabla de registros con los pines
*********************************************************/
void MapeoIOmodbus() {

  // digital outputs -> au16data[0]
  // Lee los bits de la variable cero y los pone en las salidas digitales
  digitalWrite( 2, bitRead( au16data[0], 0 )); //Lee el bit 0 de la variable au16data[0] y lo pone en el pin 2 de Arduino

  // digital inputs -> au16data[1]
  // Lee las entradas digitales y las guarda en bits de la primera variable del vector
  // (es lo mismo que hacer una máscara)
  bitWrite( au16data[1], 0, digitalRead( 3 )); //Lee el pin 3 del Arduino y lo guarda en el bit 0 de la variable au16data[0]


  // Cambia el valor del PWM
  analogWrite( 4, au16data[2] ); //El valor de au16data[2] se escribe en la salida de PWM del pin 4 de Arduino. (siendo 0=0% y 255=100%)

  // Lee las entradaa analógica (ADC)
  au16data[4] = analogRead( A0 ); //El valor analógico leido en el pin A0 se guarda en au16data[4]. (siendo 0=0v y 1023=5v)
}
