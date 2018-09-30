#include <Arduino.h>

/*
 NodeMcu-Client-Aussentemperatur

 Temperatur wird über angeschlossenen Sensor DS18B20 ausgelesen und per
 Url an einen Server uebertragen.
 Als Server (also Empfaenger) kann ebenfalls ein NodeMcu-Board verwendet werden.
 Ein Beispiel-Empfaenger empfehlen wir das Script "NodeMCU-Server-TFT-Temperatur" auf unser
 Projektseite. Dieses gibt die empfangene Temperatur als auch lokale Temperatur auf einem
 QVGA-Farbdisplay aus.
 Die Temperatur wird nur alle 15 Minuten übertragen um Energie zu sparen und Batterie
 Betrieb zu ermöglichen. Zwischendurch legt sich das Board schlafen.

 Temperatursensor DS18B20 an Pin D2

 Bezugsquelle Temperatursensor: Reichelt / Conrad / Amazon - http://amzn.to/2i3WlRX
 Bezugsquelle NodeMCU Board: http://amzn.to/2iRkZGi
 Notwendige Lib:
 https://github.com/milesburton/Arduino-Temperature-Control-Library

 Programm erprobt ab Arduino IDE 1.6.13
 Projektbeschreibung und weitere Beispiele unter https://www.mikrocontroller-elektronik.de/
*/

#include <ESP8266WiFi.h>
#include <I2CSoilMoistureSensor.h>
#include <Wire.h>

const char* ssid = "WLAN"; //Hier SSID eures WLAN Netzes eintragen
const char* password = ""; //Hier euer Passwort des WLAN Netzes eintragen

const char* host = "192.168.178.75"; //Server der die temperatur empfangen soll
                                   //(er sollte feste IP haben)
const char* script = "/sensor/temperatur/"; //URL/Verzeichnis das wir gewaehlt haben

const char* passwort = "passwortxyz"; //Passwort, derzeit ungenutzt
const char* idnr = "1"; //Hier kann man dem Sensor eine beliebe ID zuteilen (derzeit ungenutzt)

#define LED D0 //Interne Led auf dem NodeMCU Board LED_BUILTIN

I2CSoilMoistureSensor sensor;

void setup() {
 Wire.begin();
 Wire.setClockStretchLimit(2500);  
 
 Serial.begin(9600);
 delay(10);

 Serial.println();
 Serial.println();
 
 sensor.begin(); // reset sensor
 delay(1000); // give some time to boot up
 Serial.print("I2C Soil Moisture Sensor Address: ");
 Serial.println(sensor.getAddress(),HEX);
 Serial.print("Sensor Firmware version: ");
 Serial.println(sensor.getVersion(),HEX);
 Serial.println();

   Serial.print("Change address to 0x21 ...");
  if (sensor.setAddress(0x21,true)) // set Sensor Address to 0x21 and reset
    Serial.println("... DONE");
  else
    Serial.println("... ERROR");
  Serial.println();

 delay(1000); // give some time to boot up
 Serial.print("I2C Soil Moisture Sensor Address: ");
 Serial.println(sensor.getAddress(),HEX);
 Serial.print("Sensor Firmware version: ");
 Serial.println(sensor.getVersion(),HEX);
 Serial.println();

 Serial.print("Verbinde mich mit Netz: ");
 Serial.println(ssid);

 WiFi.begin(ssid, password);

 
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 }

 Serial.println("");
 Serial.println("WiFi Verbindung aufgebaut");
 Serial.print("Eigene IP des ESP-Modul: ");
 Serial.println(WiFi.localIP());
}



//In unserem Beispiel wird die loop Schleife eigentlich nur einmal durchlaufen
void loop() {

 while (sensor.isBusy()) delay(50); // available since FW 2.3
 char temperaturStr[6];
 float temperatur = sensor.getTemperature()/(float)10;
 dtostrf(temperatur, 2, 0, temperaturStr);
 Serial.print("Temperatur: ");
 Serial.println(temperaturStr);

 char humStr[6];
 float hum = sensor.getCapacitance();
 dtostrf(hum, 2, 0, humStr);
 Serial.print("Bodenfeuchte: ");
 Serial.println(humStr);

 sensor.sleep(); // available since FW 2.3


 int versuche=1;
 WiFiClient client;
 const int httpPort = 80;
 int erg;
 do
 {
   Serial.print("Verbindungsaufbau zu Server ");
   Serial.println(host);

   erg =client.connect(host, httpPort);
   if (!erg) {
     versuche++;
     Serial.println("Verbindungsaufbau nicht moeglich!!!");
     if (versuche>3){
       Serial.println("Klappt nicht, ich versuche es spaeter noch mal!");
       client.stop();
       WiFi.disconnect();
       ESP.deepSleep( 10*60000000); //Etwas später neu probieren, solange schlafen
     }
   }
   delay(1000);
 } while (erg!=1);

 String url = script; //Url wird zusammengebaut
 url += "?pw=";
 url += passwort;
 url += "&idnr=";
 url += idnr;
 url += "&temp=";
 url += temperaturStr;
 url += "&hum=";
 url += humStr;

 Serial.print("Folgende URL wird aufgerufen: ");
 Serial.println(host + url);

 client.print(String("GET ") + url + " HTTP/1.1\r\n" +
 "Host: " + host + "\r\n" +
 "Connection: close\r\n\r\n");
 unsigned long timeout = millis();
 while (client.available() == 0) {
   if (millis() - timeout > 5000) {
      Serial.println("Timeout!");
      Serial.println("Uebergabe klappt nicht, ich versuche es spaeter noch mal!");
      client.stop();
      WiFi.disconnect();
      ESP.deepSleep( 60*1000000); //Etwas später 60 Sekunden neu probieren,solange schlafen
   }
 }

 Serial.print("Rueckgabe vom Server:\n");
 while(client.available()){
   String line = client.readStringUntil('\r');
   Serial.print(line);
 }

 client.stop();
 WiFi.disconnect();
 Serial.println("\nVerbindung beendet");

 Serial.print("Schlafe jetzt ...");
 ESP.deepSleep( 15*60000000); //Angabe in Minuten - hier 15
}

