#include <WiFi.h>
#include <WiFiUdp.h>
// WiFi network name and password:
const char * ssid = "PercEvite_test";
const char * password = "percevite";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * host = "192.168.4.255";
const int port = 8000;

//The udp library class
WiFiUDP udp;
int incomingByte = -1;

void netCom(){
    Serial.println('=');
    while(incomingByte == -1){
      incomingByte = Serial.read();
    }
    
   //Send a packet
    udp.begin(WiFi.localIP(),port);
    udp.beginPacket(host,port);
    udp.printf("byte:%u\r\n", incomingByte);
    udp.endPacket();
    
    
     udp.flush();
     delay(20);
    
    udp.stop();
    incomingByte = -1;    
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(10);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());
  

}

void loop() {
  netCom();
  delay(1);

}
