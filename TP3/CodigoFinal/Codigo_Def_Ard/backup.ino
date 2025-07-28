//// Definición de Pines
//#define REPin 4   // Pin para habilitar la recepción
//#define LED1 9
//#define LED2 10
//#define Digital 20
//#define Luz A0
//#define Pote A1
//
//
//// Definición de variables tramas de recepción
//const int arraySize = 8;  // Tamaño del array para almacenar los datos
//byte receivedData[arraySize];  // Array para almacenar los datos en formato binario
//int receivedDataDecimal[arraySize];  // Array para almacenar los datos en decimal
//int currentIndex = 0;  // Índice actual dentro del array
//
//// Variables tramas de respuesta
//const int arraySizeResponse = 7;  // Tamaño del array para almacenar los datos
//const int sizeWrite = 8;
//byte responseData[arraySizeResponse];  // Array para almacenar los datos en formato binario
//int responseDataDecimal[arraySizeResponse];  // Array para almacenar los datos en decimal
//int respCurrentIndex = 0;  // Índice actual dentro del array
//byte responseDataW[sizeWrite];
//
//// Unificación de registros
//const int arrayLong = 5;
//unsigned int reciveDataDecimalUnifi[arrayLong];
//
//// Variables de registros
//int valorPWMOUT1 = 50;        // Registro 1
//int valorPWMOUT2 = 50;         // Registro 2
//int valorDigital = 0;          // Registro 3
//int lecturaLUZ = 925;          // Registro 4
//int lecturaPote = 300;         // Registro 5
//byte activarSalida = 1;        // Registro 6
//
//unsigned int envioID = 0;
//unsigned int envioFunc = 0;
//unsigned int envioCantBits = 0;
//unsigned int valorEnv = 0;
//unsigned int CRCcalculado = 0;
//bool crcMatch = false;  // Variable para verificar si el CRC coincide
//
//void setup() {
//  Serial.begin(9600);  // Inicializar el monitor serial a 9600 bps
//  Serial1.begin(9600); // Inicializar Serial1 con paridad par
//
//  pinMode(REPin, OUTPUT);      // Configurar el pin RE como salida
//  digitalWrite(REPin, LOW);    // Habilitar la recepción
//
//  pinMode(LED1, OUTPUT);
//  pinMode(LED2, OUTPUT);
//  pinMode(Digital, INPUT);
//  pinMode(Luz, INPUT);
//  pinMode(Pote, INPUT);
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
//  // Verificar que se hayan recibido al menos 8 datos antes de combinar
//  if (currentIndex == 0) {  // Verificar que el array está lleno
//    reciveDataDecimalUnifi[0] = receivedData[0];  // Guardar ID
//    reciveDataDecimalUnifi[1] = receivedData[1];  // Guardar Func
//    reciveDataDecimalUnifi[2] = (receivedData[2] << 8) | receivedData[3]; // Combinar posición 2 y 3
//    reciveDataDecimalUnifi[3] = (receivedData[4] << 8) | receivedData[5]; // Combinar posición 4 y 5
//    reciveDataDecimalUnifi[4] = (receivedData[7] << 8) | receivedData[6]; // Combinar posición 6 y 7
//
//    // Mostrar los valores combinados
//    Serial.println("Datos combinados:");
//    Serial.print("ID: ");
//    Serial.println(reciveDataDecimalUnifi[0]);
//    Serial.print("Func: ");
//    Serial.println(reciveDataDecimalUnifi[1]);
//    Serial.print("Reg: ");
//    Serial.println(reciveDataDecimalUnifi[2]);
//    Serial.print("Cant: ");
//    Serial.println(reciveDataDecimalUnifi[3]);
//    Serial.print("CRC Recibido: ");
//    Serial.println(reciveDataDecimalUnifi[4]);
//
//    // Calcular el CRC de los primeros 6 bytes recibidos
//    unsigned int CRCcalculado = calcularCRC(receivedData, 6);
//    Serial.print("CRC Calculado: ");
//    Serial.println(CRCcalculado);
//
//    // Verificar si el CRC calculado coincide con el CRC recibido
//    crcMatch = (CRCcalculado == reciveDataDecimalUnifi[4]);
//
//    // Mostrar el estado del CRC
//    Serial.print("CRC match: ");
//    Serial.println(crcMatch ? "Sí" : "No");
//
//    Serial.print("Luz: ");
//    Serial.println(lecturaLUZ);
//
//    Serial.print("ActSal: ");
//    Serial.println(activarSalida);
//
//    Serial.print("Pote: ");
//    Serial.println(lecturaPote);
//
//    Serial.print("ValDig: ");
//    Serial.println(valorDigital);
//
//    if (crcMatch && reciveDataDecimalUnifi[0] == 3) {
//      Serial.println("CRC correcto, proceder con lectura/escritura.");
//
//      if (reciveDataDecimalUnifi[1] == 3) {  // Función 03
//        Serial.println("Función 03 reconocida");
//
//        envioID = 3;
//        envioFunc = 3;
//        envioCantBits = 2;
//
//        switch (reciveDataDecimalUnifi[2]) {
//          case 1:
//            valorEnv = valorPWMOUT1;
//            break;
//          case 2:
//            valorEnv = valorPWMOUT2;
//            break;
//          case 3:
//            valorEnv = valorDigital;
//            break;
//          case 4:
//            valorEnv = lecturaLUZ;
//            break;
//          case 5:
//            valorEnv = lecturaPote;
//            break;
//          case 6:
//            valorEnv = activarSalida;
//            break;
//        }
//
//        responseData[0] = envioID;
//        responseData[1] = envioFunc;
//        responseData[2] = envioCantBits;
//
//        // Obtener los 8 bits más significativos (high byte)
//        responseData[3] = (valorEnv >> 8) & 0xFF;
//
//        // Obtener los 8 bits menos significativos (low byte)
//        responseData[4] = valorEnv & 0xFF;
//
//        // Calcular el CRC de la respuesta
//        CRCcalculado = calcularCRC(responseData, arraySizeResponse - 2);
//
//        // Guardar el CRC en las posiciones 5 y 6
//        responseData[6] = (CRCcalculado >> 8) & 0xFF;
//        responseData[5] = CRCcalculado & 0xFF;
//
//        digitalWrite(REPin, HIGH);
//        // Enviar la respuesta completa por Serial1
//        Serial.println("En proceso de envío...");
//        Serial1.write(responseData, arraySizeResponse);
//        delay(500);
//        digitalWrite(REPin, LOW);
//        Serial.println("Datos enviados.");
//
//      }
//
//      if (reciveDataDecimalUnifi[1] == 6) {
//        // Manejo para función 06 (Escritura de registros)
//        Serial.println("Función 06 reconocida");
//
//        envioID = 3;
//        envioFunc = 6;
//
//        switch (reciveDataDecimalUnifi[2]) {
//          case 1:
//            valorPWMOUT1 = reciveDataDecimalUnifi[3];
//            valorEnv = valorPWMOUT1;
//            break;
//          case 2:
//            valorPWMOUT2 = reciveDataDecimalUnifi[3];
//            valorEnv = valorPWMOUT2;
//            break;
//          case 3:
//            Serial.print("none");
//            break;
//          case 4:
//            Serial.print("none");
//            break;
//          case 5:
//            Serial.print("none");
//            break;
//          case 6:
//            activarSalida = reciveDataDecimalUnifi[3];
//            valorEnv = activarSalida;
//            break;
//        }
//
//        responseDataW[0] = envioID;
//        responseDataW[1] = envioFunc;
//
//        // Obtener los 8 bits más significativos (high byte)
//        responseDataW[2] = (reciveDataDecimalUnifi[2] >> 8) & 0xFF;
//
//        // Obtener los 8 bits menos significativos (low byte)
//        responseDataW[3] = reciveDataDecimalUnifi[2] & 0xFF;
//
//        // Obtener los 8 bits más significativos (high byte)
//        responseDataW[4] = (valorEnv >> 8) & 0xFF;
//
//        // Obtener los 8 bits menos significativos (low byte)
//        responseDataW[5] = valorEnv & 0xFF;
//
//        // Calcular el CRC de la respuesta
//        CRCcalculado = calcularCRC(responseDataW, sizeWrite - 2);
//
//        // Guardar el CRC en las posiciones 5 y 6
//        responseDataW[7] = (CRCcalculado >> 8) & 0xFF;
//        responseDataW[6] = CRCcalculado & 0xFF;
//
//        digitalWrite(REPin, HIGH);
//        // Enviar la respuesta completa por Serial1
//        Serial.println("En proceso de envío...");
//        Serial1.write(responseDataW, sizeWrite);
//        delay(500);
//        digitalWrite(REPin, LOW);
//        Serial.println("Datos enviados.");
//      }
//
//      receivedData[0] = 0;
//      receivedData[1] = 0;
//      receivedData[2] = 0;
//      receivedData[3] = 0;
//      receivedData[4] = 0;
//      receivedData[5] = 0;
//      receivedData[6] = 0;
//      receivedData[7] = 0;
//
//    } else {
//      Serial.println("Error en el CRC o ID no válido.");
//    }
//  }
//
//  // Agregar un pequeño retardo para no saturar el monitor serial
//  delay(100);
//  lecturaLUZ = analogRead(Luz);
//  lecturaPote = analogRead(Pote);
//  valorDigital = digitalRead(Digital);
//
//  if (activarSalida >= 1) {
//    analogWrite(LED1, valorPWMOUT1);
//    analogWrite(LED2, valorPWMOUT2);
//  }
//
//  if (activarSalida == 0) {
//    analogWrite(LED1, 0);
//    analogWrite(LED2, 0);
//  }
//
//}
//
//// Función para calcular CRC de 16 bits
//unsigned int calcularCRC(byte *array, int length) {
//  unsigned int crc = 0xFFFF;  // Valor inicial del CRC
//  for (int pos = 0; pos < length; pos++) {
//    crc ^= (unsigned int)array[pos];  // XOR con el byte actual
//    for (int i = 8; i != 0; i--) {    // Procesar cada bit del byte
//      if ((crc & 0x0001) != 0) {      // Si el bit menos significativo es 1
//        crc >>= 1;                    // Desplazar hacia la derecha
//        crc ^= 0xA001;                // XOR con el polinomio
//      } else {
//        crc >>= 1;                    // Solo desplazar si no hay 1
//      }
//    }
//  }
//  return crc;  // Retornar el CRC calculado
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
