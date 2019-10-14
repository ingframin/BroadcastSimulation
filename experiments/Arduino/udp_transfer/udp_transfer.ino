#include <WiFi.h>
#include <WiFiUdp.h>
#include "esp_wifi.h"
// WiFi network name and password:
const char * ssid = "PercEvite_P";
const char * password = "hi64nyvy";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * host = "192.168.1.137";
const int port = 8000;
char buffer[80] = {'*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*',
                   '*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*',
                   '*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*',
                   '*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'};
char incomingPacket[255];  // buffer for incoming packets
//The udp library class
WiFiUDP udp;
int incomingByte = -1;
uint8_t channel;
IPAddress local_IP(192, 168, 1, 10);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
void scan(uint8_t ch, uint8_t Ts){
  //digitalWrite(21, HIGH);
  int numSsid = WiFi.scanNetworks(false, true, true, Ts, ch);
  
  for (int j = 0; j < numSsid; j++) {
    String ssid = WiFi.SSID(j);
    if(ssid.startsWith("D")){
      Serial.print(ssid+"\t");
      Serial.print("rssi:");
      Serial.println(WiFi.RSSI(j));
    
    }
  
  }//for
 //digitalWrite(21, LOW);
}//scan()

void netCom(){
  int packetSize = udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
    int len = udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
  }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    Serial.println('>'); //Used to synchronize UART communication
      Serial.write(17);//XON
      int b = Serial.readBytesUntil('*',buffer, 80);
     Serial.write(19);//XOFF  
   //Send a packet
    udp.begin(WiFi.localIP(),port);
    udp.beginPacket(host,port);
    udp.printf(buffer);
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
  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(10);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());
  esp_wifi_set_promiscuous(true);
  channel = random(1,14); 
}

void loop() {
  netCom();
  unsigned long start = micros();
  Serial.println('S');
  scan(channel,60);//S
  unsigned long stop = micros();
  Serial.printf("s-dur: %u\r\n",stop-start);
  delay(1);

}
