#include <SoftwareSerial.h>
//#include "dht.h"

#define rxPin 11 // Broche 11 en tant que RX, à raccorder sur TX du HC-05
#define txPin 10 // Broche 10 en tant que TX, à raccorder sur RX du HC-05

SoftwareSerial mySerial(rxPin, txPin);

//dht DHT;

// lowest and highest sensor readings:
const int sensorMin = 0;     // sensor minimum
const int sensorMax = 1024;  // sensor maximum

void setup()
{
 // define pin modes for tx, rx pins:
 pinMode(rxPin, INPUT);
 pinMode(txPin, OUTPUT);
 mySerial.begin(9600);
 Serial.begin(9600);
}

void loop()
{
  //int i = 0;
  //char someChar[32] = {0};

  //DHT.read11(A1);
    
  //Serial.print("Current humidity = ");
  //Serial.print(DHT.humidity);
  //float h=DHT.humidity;

  float h=40;
  
  //Serial.print("%  ");
  //Serial.print("temperature = ");
  //Serial.print(DHT.temperature); 
  //float t=DHT.temperature;

  float t=37;
  
  //Serial.println("C  ");
  
  // read the sensor on analog A0:
  int sensorReading = analogRead(A0);
  
  // map the sensor range (four options):
  int range = map(sensorReading, sensorMin, sensorMax, 0, 3);
  
  // range value:
    switch (range) {
    case 0:    // A fire closer than 1.5 feet away.
      mySerial.println(String(sensorReading)+"#Feu proche#"+String(range)+"#"+String(t)+"#"+String(h));
      Serial.println(String(sensorReading)+"#Feu proche#"+String(range)+"#"+String(t)+"#"+String(h));
      break;
    case 1:    // A fire between 1-3 feet away.
      mySerial.println(String(sensorReading)+"#Feu distant#"+String(range)+"#"+String(t)+"#"+String(h));
      Serial.println(String(sensorReading)+"#Feu distant#"+String(range)+"#"+String(t)+"#"+String(h));
      break;
    case 2:    // No fire detected.
      mySerial.println(String(sensorReading)+"#Pas de feu#"+String(range)+"#"+String(t)+"#"+String(h));
      Serial.println(String(sensorReading)+"#Pas de feu#"+String(range)+"#"+String(t)+"#"+String(h));
      break;
    }
  
  // when characters arrive over the serial port...
  //if(Serial.available()) {
  // do{
  // someChar[i++] = Serial.read();
  // delay(3000);
  // }while (Serial.available() > 0);
  // mySerial.println(someChar);
  // Serial.println(someChar);
  //}
  //while(mySerial.available())
  // Serial.print((char)mySerial.read());
  //}
  
  delay(1000);
}
