#include "ESP8266WiFi.h"
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

HTTPClient http;
WiFiClient client;

#define builtInLED 2

const char* ssid = "TP-LINK_7DD6";  //Enter SSID
const char* password = "12345678";   //Enter Password
String address_rfid = "http://192.168.0.101/TourIT/web_server/php/rfid_connector.php";
String address_batt = "http://192.168.0.101/TourIT/web_server/php/battery_connector.php";

void setup(void) {
  pinMode(builtInLED, OUTPUT);
  Serial.begin(115200);
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(builtInLED, HIGH);
    delay(250);
    digitalWrite(builtInLED, LOW);
    delay(250);
    Serial.println("***");
  }
  Serial.println("");
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());  // Print the IP address

  http.begin(client, address_rfid);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.POST("input=");  // Send an initial POST request to the server to set up the data variable
  http.end();

  http.begin(client, address_batt);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.POST("input=");  // Send an initial POST request to the server to set up the data variable
  http.end();
}

void call_http(String& value, String& address);

void loop() {
  String recv;
  if (Serial.available() > 0) {
    recv = Serial.readStringUntil('\n');
    recv.trim();
    int separate = recv.indexOf(",");
    String recv_rfid = recv.substring(0, separate);   
    String recv_batt = recv.substring(separate + 1);  
    recv_rfid.trim();
    recv_batt.trim();
    if (recv_rfid != "") {
      call_http(recv_rfid, address_rfid);
    }

    if (recv_batt != "") {
      call_http(recv_batt, address_batt);
    }
  }
}

void call_http(String& value, String& address) {
  http.begin(client, address);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int httpCode = http.POST("input=" + value);
  if (httpCode > 0) {
    Serial.printf("HTTP status code: %d\n", httpCode);
    String response = http.getString();
    Serial.println(response);
    digitalWrite(builtInLED, LOW);
  } else {
    Serial.println("HTTP request failed");
    digitalWrite(builtInLED, HIGH);
    delay(500);
  }
  http.end();
  value.clear();
}