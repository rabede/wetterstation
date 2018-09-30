/*
 NodeMCU-Server-TFT-Temperatur

 NodeMCU fungiert als Server und empfängt Temperatur per URL
 Temperaturwerte (z.B. Außentemperatur) wird auf angeschlossenem
 QVGA-Display ausgegeben,

 Parameteruebergabe-Syntax:
 http://192.168.2.75/sensor/temperatur/?pw=passwortxyz&idnr=1&wert=20

 Verwendetes Display: 2.2 Zoll Serial TFT-Farbdisplay; SPI; Auflösung 240x320 Pixel
 Bezugsquellen Display:
 Amazon - http://amzn.to/2iNmaXx / Amazon - http://amzn.to/2j1VIXK

 Temperatur wird über angeschlossenen Sensor DS18B20 ausgelesen und auf dem Display angezeigt
 Temperatursensor DS18B20 an Pin D2
 Bezugsquelle Temperatursensor: Reichelt / Conrad / Amazon - http://amzn.to/2i3WlRX

 Notwendig ist die angepasste Display-Lib: https://github.com/glennirwin/Adafruit_ILI9340

 Programm erprobt ab Arduino IDE 1.6.13
 Projektbeschreibung und weitere Beispiele unter https://www.mikrocontroller-elektronik.de/
 */

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

float merketemp = 0;
float merkehum = 0;

const char* ssid = "WLAN"; //Ihr Wlan,Netz SSID eintragen
const char* pass = ""; //Ihr Wlan,Netz Passwort eintragen
IPAddress ip(192, 168, 178, 75); //Feste IP des neuen Servers, frei wählbar
IPAddress gateway(192, 168, 178, 1); //Gatway (IP Router eintragen)
IPAddress subnet(255, 255, 255, 0); //Subnet Maske eintragen

ESP8266WebServer server(80);

void handleRoot() {
  //Temperatur auch bei Url-Aufruf zurückgeben
  String message =
      "*** Ueberwachungs Server - Beispiel von www.mikrocontroller-elektronik.de ***\n";
  String tempstr = String(merketemp, 2);
  message += "Temperatur : " + tempstr + "\n";
  tempstr = String(merkehum, 2);
  message += "Bodenfeuchte: " + tempstr + "\n";
  server.send(200, "text/plain", message);
}

void handleTemperatur() {
  //printUrlArg(); //fuer Debugz Zwecke

  String stemp = server.arg("temp");
  float temperatur = stemp.toFloat();
  if (merketemp != temperatur) {
    merketemp = temperatur;
  }

  String shum = server.arg("hum");
  float hum = shum.toFloat();
  if (merkehum != hum) {
    merkehum = hum;
  }

  //Temperatur auch bei Url-Aufruf zurückgeben
  String message =
      "*** Ueberwachungs Server - Beispiel von www.mikrocontroller-elektronik.de ***\n";
  String tempstr = String(merketemp, 2);
  message += "Temperatur : " + tempstr + "\n";
  tempstr = String(merkehum, 2);
  message += "Bodenfeuchte: " + tempstr + "\n";
  server.send(200, "text/plain", message);
}

void printUrlArg() {
  //Alle Parameter seriell ausgeben
  String message = "";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(200, "text/plain", message);
  Serial.println(message);
}

void setup() {

  Serial.begin(115200);
  Serial.println(" \r\nINIT \r\n");

  WiFi.begin(ssid, pass);
  WiFi.config(ip, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Verbunden mit ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/sensor/temperatur/", handleTemperatur);
  server.begin();

  Serial.println("HTTP Server wurde gestartet!");
}

void loop(void) {
  server.handleClient();

  delay(500);

}

