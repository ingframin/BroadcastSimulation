#include <WiFi.h>
#include "esp_wifi.h"
const char* ssid = "PercEvite_P";
const char* password =  "hi64nyvy";
//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
/* Put IP Address details */
IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

WiFiClient client;
WiFiServer server(8000);
void setup() {
   Serial.begin(256000);
  Serial.setTimeout(100);
  WiFi.mode(WIFI_AP);
  
   WiFi.softAP(ssid, password, 8);
   WiFi.softAPConfig(local_ip, gateway, subnet);
   delay(100);
   server.begin();
  
  
}

void loop() {
   if (server.hasClient()){
    Serial.println("Connection accepted");
    client = server.available();
    uint8_t ReceiveBuffer[30];
    while (client.connected() && client.available()){
    int Received = client.read(ReceiveBuffer, sizeof(ReceiveBuffer));
    client.write(ReceiveBuffer, Received);
  }
   }

}
