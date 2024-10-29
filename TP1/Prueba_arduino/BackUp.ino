//const int maxReadings = 17; // Número máximo de caracteres en la trama ASCII
//char readings[maxReadings]; // Arreglo para almacenar la trama recibida
//int index = 0;
//
//void activar() {
//  pinMode(4, OUTPUT);
//  pinMode(4, LOW);
//}
//
////void setup() {
////  Serial.begin(115200);        // Inicializar el monitor serial a 9600 bps
////  Serial1.begin(9600, SERIAL_8E1); // Inicializar Serial1 (para RS485) con paridad par
////  activar();
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (RS485)
//  if (Serial1.available()) {
//    char incomingByte = Serial1.read(); // Leer un byte
//    Serial.print("Lo que llega");
//    Serial.println(incomingByte);
//
//    // Almacenar el byte en el arreglo si no está lleno
//    if (index < maxReadings) {
//      readings[index] = incomingByte; // Guardar el byte en el arreglo
//      index++;
//    }
//
//    // Si se han leído 17 bytes (trama completa), procesarla
//    if (index >= maxReadings) {
//      Serial.print("Trama Modbus ASCII Recibida: ");
//      for (int i = 0; i < maxReadings; i++) {
//        Serial.print(readings[i]); // Mostrar cada carácter recibido
//      }
//      Serial.println();
//
//      // Convertir la trama ASCII a hexadecimales
//      processReceivedData();
//
//      // Reiniciar el índice para la siguiente serie de lecturas
//      index = 0;
//    }
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//void processReceivedData() {
//  if (readings[0] == ':' && index == maxReadings) {
//    // Suponiendo que la trama tiene el formato correcto
//    Serial.println("Procesando la trama Modbus...");
//
//    // Convertir caracteres ASCII a valores hexadecimales
//    for (int i = 1; i < maxReadings - 2; i += 2) {
//      unsigned char high = readings[i];
//      unsigned char low = readings[i + 1];
//      unsigned char value = asciiToHex(high, low);
//
//      // Imprimir el valor convertido
//      Serial.print("Byte ");
//      Serial.print(i / 2); // Número de byte
//      Serial.print(": ");
//      Serial.println(value, HEX); // Mostrar en formato hexadecimal
//    }
//  }
//}
//
//unsigned char asciiToHex(char high, char low) {
//  return (hexCharToValue(high) << 4) | hexCharToValue(low);
//}
//
//unsigned char hexCharToValue(char c) {
//  if (c >= '0' && c <= '9') {
//    return c - '0'; // Convertir caracteres '0'-'9' a 0-9
//  }
//  if (c >= 'A' && c <= 'F') {
//    return c - 'A' + 10; // Convertir caracteres 'A'-'F' a 10-15
//  }
//  if (c >= 'a' && c <= 'f') {
//    return c - 'a' + 10; // Convertir caracteres 'a'-'f' a 10-15
//  }
//  return 0; // Si no es un carácter hexadecimal válido
//}




//const int REPin = 4;  // Pin para habilitar la recepción
//const int maxReadings = 4; // Número máximo de lecturas
//char readings[maxReadings]; // Arreglo para almacenar las lecturas
//int index = 0;             // Índice para el arreglo actual
//
//void setup() {
//  Serial.begin(9600);          // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600, SERIAL_8E1); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  Serial.println("Esperando datos..."); // Mensaje de depuración
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (MAX485)
//  while (Serial1.available()) {  // Si hay datos disponibles
//    char incomingByte = Serial1.read(); // Leer un byte
//
//    // Almacenar el byte en el arreglo si no está lleno
//    if (index < maxReadings) {
//      readings[index] = incomingByte; // Guardar el byte en el arreglo
//      index++;                        // Incrementar el índice
//    }
//
//    // Si se han leído 4 datos, mostrar el arreglo
//    if (index >= maxReadings) {
//      Serial.print("Valores recibidos en binario: ");
//      for (int i = 0; i < maxReadings; i++) {
//        // Convertir el byte a su representación binaria y mostrarlo
//        Serial.print("Byte ");
//        Serial.print(i + 1);
//        Serial.print(": ");
//        Serial.println(byteToBinary(readings[i])); // Mostrar en binario
//      }
//      index = 0; // Reiniciar el índice para la siguiente serie de lecturas
//    }
//  }
//
//  // Si no hay datos, mostrar un mensaje
//  if (Serial1.available() == 0) {
//    Serial.println("No hay datos disponibles.");
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//// Función para convertir un byte a su representación binaria
//String byteToBinary(byte b) {
//  String binary = "";
//  for (int i = 7; i >= 0; i--) {
//    binary += ((b >> i) & 1) ? "1" : "0"; // Desplazar y comprobar cada bit
//  }
//  return binary;
//}


//
//const int REPin = 4;  // Pin para habilitar la recepción
//
//void setup() {
//  Serial.begin(9600);          // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  Serial.println("Esperando datos..."); // Mensaje de depuración
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (MAX485)
//  while (Serial1.available()) {  // Si hay datos disponibles
//    char incomingByte = Serial1.read(); // Leer un byte
//
//    // Mostrar el byte en formato binario de 16 bits
//    Serial.print("Valor recibido en binario: ");
//    Serial.println(byteToBinary16(incomingByte)); // Mostrar en binario
//  }
//
//  // Si no hay datos, mostrar un mensaje
//  if (Serial1.available() == 0) {
//    Serial.println("No hay datos disponibles.");
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//// Función para convertir un byte a su representación binaria de 16 bits
//String byteToBinary16(byte b) {
//  String binary = "00000000"; // Inicializar con 16 bits en 0
//  for (int i = 7; i >= 0; i--) {
//    binary += ((b >> i) & 1) ? "1" : "0"; // Desplazar y comprobar cada bit
//  }
//  return binary; // Retornar el valor en binario
//}
//




//const int REPin = 4;  // Pin para habilitar la recepción
//
//void setup() {
//  Serial.begin(9600);          // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  Serial.println("Esperando datos..."); // Mensaje de depuración
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (MAX485)
//  while (Serial1.available()) {  // Si hay datos disponibles
//    char incomingByte = Serial1.read(); // Leer un byte
//
//    // Mostrar el byte en formato binario de 8 bits invertido
//    Serial.print("Valor recibido en binario invertido: ");
//    Serial.println(byteToBinary8(incomingByte)); // Mostrar en binario
//  }
//
//  // Si no hay datos, mostrar un mensaje
//  if (Serial1.available() == 0) {
//    Serial.println("No hay datos disponibles.");
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//// Función para convertir un byte a su representación binaria de 8 bits invertida
//String byteToBinary8(byte b) {
//  String binary = ""; // Inicializar como cadena vacía
//  for (int i = 7; i >= 0; i--) {
//    // Invertir el bit: cambiar 0 por 1 y 1 por 0
//    binary += ((b >> i) & 1) ? "0" : "1"; // Desplazar y comprobar cada bit
//  }
//  return binary; // Retornar el valor en binario invertido
//}


//const int REPin = 4;   // Pin para habilitar la recepción
//const int arraySize = 8;  // Tamaño del array para almacenar los datos
//byte receivedData[arraySize];  // Array para almacenar los datos en formato binario
//int receivedDataDecimal[arraySize];  // Array para almacenar los datos en decimal
//int currentIndex = 0;  // Índice actual dentro del array
//
//void setup() {
//  Serial.begin(9600);  // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  Serial.println("Esperando datos...");  // Mensaje de depuración
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (MAX485)
//  while (Serial1.available()) {  // Si hay datos disponibles
//    char incomingByte = Serial1.read(); // Leer un byte
//
//    // Mostrar el byte en formato binario de 8 bits
//    Serial.print("Valor recibido en binario: ");
//    Serial.println(byteToBinary8(incomingByte)); // Mostrar en binario
//
//    // Mostrar el byte en formato decimal
//    Serial.print("Valor recibido en decimal: ");
//    Serial.println(incomingByte);  // Mostrar en decimal
//
//    // Guardar el byte en el array en la posición cíclica
//    receivedData[currentIndex] = incomingByte;  // Guardar el dato en binario
//    receivedDataDecimal[currentIndex] = incomingByte;  // Guardar el dato en decimal
//
//    // Incrementar el índice de forma cíclica
//    currentIndex = (currentIndex + 1) % arraySize;
//  }
//
//  // Si no hay datos, mostrar un mensaje
//  if (Serial1.available() == 0) {
//    Serial.println("No hay datos disponibles.");
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//// Función para convertir un byte a su representación binaria de 8 bits
//String byteToBinary8(byte b) {
//  String binary = ""; // Inicializar con una cadena vacía
//  for (int i = 7; i >= 0; i--) {
//    binary += ((b >> i) & 1) ? "1" : "0"; // Desplazar y comprobar cada bit
//  }
//  return binary;  // Retornar el valor en binario
//}


////definicion de Pines
//const int REPin = 4;   // Pin para habilitar la recepción
//
////definicion variables tramas recepcion
//const int arraySize = 8;  // Tamaño del array para almacenar los datos
//byte receivedData[arraySize];  // Array para almacenar los datos en formato binario
//int receivedDataDecimal[arraySize];  // Array para almacenar los datos en decimal
//int currentIndex = 0;  // Índice actual dentro del array
//
////variables variables tramas respuesta
//const int arraySizeResponse = 7;  // Tamaño del array para almacenar los datos
//byte responseData[arraySizeResponse];  // Array para almacenar los datos en formato binario
//int responseDataDecimal[arraySizeResponse];  // Array para almacenar los datos en decimal
//int respCurrentIndex = 0;  // Índice actual dentro del array
//
////unificacion de registros
//const int arrayLong = 5;
//unsigned int reciveDataDecimalUnifi[arrayLong];
//
////variables de registros
//int valorPWMOUT = 125;
//int valorDigital = 0;
//int encendidoLed = 0;
//int lecturaPWMIN = 925;
//
//void setup() {
//  Serial.begin(9600);  // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  Serial.println("Esperando datos...");  // Mensaje de depuración
//}
//
//void loop() {
//  // Leer datos del puerto serie Serial1 (MAX485)
//  while (Serial1.available()) {  // Si hay datos disponibles
//    byte incomingByte = Serial1.read(); // Leer un byte como valor numérico
//
//    // Mostrar el byte en formato binario de 8 bits
//    Serial.print("Valor recibido en binario: ");
//    Serial.println(byteToBinary8(incomingByte)); // Mostrar en binario
//
//    // Convertir el byte a decimal y mostrarlo
//    int decimalValue = (int)incomingByte;  // Convertir el byte a decimal
//    Serial.print("Valor recibido en decimal: ");
//    Serial.println(decimalValue);  // Mostrar en decimal
//
//    // Guardar el byte en el array en la posición cíclica
//    receivedData[currentIndex] = incomingByte;  // Guardar el dato en binario
//    receivedDataDecimal[currentIndex] = decimalValue;  // Guardar el dato en decimal
//
//    // Incrementar el índice de forma cíclica
//    currentIndex = (currentIndex + 1) % arraySize;
//  }
//
//  // Si no hay datos, mostrar un mensaje
//  if (Serial1.available() == 0) {
//    Serial.println("No hay datos disponibles.");
//  }
//
//  // Si ya tenemos datos en las posiciones 6 y 7, combinamos sus valores
//  if (currentIndex >= 7) {
//    reciveDataDecimalUnifi[0] = receivedData[0];
//    reciveDataDecimalUnifi[1] = receivedData[1];
//    reciveDataDecimalUnifi[2] = (receivedData[2] << 8) | receivedData[3]; // Combinar posición 2 y 3;;
//    reciveDataDecimalUnifi[3] = (receivedData[4] << 8) | receivedData[5]; // Combinar posición 4 y 5;;
//    reciveDataDecimalUnifi[4] = (receivedData[6] << 8) | receivedData[7]; // Combinar posición 6 y 7;
//
//    Serial.print("  ID:");
//    Serial.println(reciveDataDecimalUnifi[0]);
//    Serial.print("Func:");
//    Serial.println(reciveDataDecimalUnifi[1]);
//    Serial.print(" Reg:");
//    Serial.println(reciveDataDecimalUnifi[2]);
//    Serial.print("Cant:");
//    Serial.println(reciveDataDecimalUnifi[3]);
//    Serial.print(" CRC:");
//    Serial.println(reciveDataDecimalUnifi[4]);
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//}
//
//// Función para convertir un byte a su representación binaria de 8 bits
//String byteToBinary8(byte b) {
//  String binary = ""; // Inicializar con una cadena vacía
//  for (int i = 7; i >= 0; i--) {
//    binary += ((b >> i) & 1) ? "1" : "0"; // Desplazar y comprobar cada bit
//  }
//  return binary;  // Retornar el valor en binario
//}
//
