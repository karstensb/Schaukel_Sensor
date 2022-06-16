#include <Arduino_LSM6DS3.h>
#include <SPI.h>
#include <WiFiNINA.h>

const char ssid[] = "vsis-raspberry-pi";
const char pass[] = "raspberryvsis-pi3";

const uint16_t port = 8080;
const char host[] = "192.168.1.148";

WiFiClient client;

void getGyro(float& x, float& y, float& z){
  while(!IMU.gyroscopeAvailable());
  IMU.readGyroscope(x, y, z);
}

void getAccel(float& x, float& y, float& z){
  while(!IMU.accelerationAvailable());
  IMU.readAcceleration(x, y, z);
}

void setup(){
  //Serial.begin(9600);

  if(!IMU.begin()){
    // Serial.println("Failed to initialize IMU!");
    while(1);
  }

  //Serial.println("Connecting to WiFi network...");
  while(WiFi.begin(ssid, pass) != WL_CONNECTED){
    //Serial.print("Attempting to connect to ");
    //Serial.println(ssid);
    delay(5000);
  }
  //Serial.print("Established connection to ");
  //Serial.println(ssid);

  //Serial.println("Connecting to server...");
  if(!client.connect(host, port)){
      //Serial.print("Unable to connect to server");
      while(1);
  }
  //Serial.println("Connected to server");
}

void loop(){
  float x, y, z;
  getGyro(x, y, z);
  client.print(x);
  client.print(";");
  client.print(y);
  client.print(";");
  client.print(z);
  client.print(";");
  getAccel(x, y, z);
  client.print(x);
  client.print(";");
  client.print(y);
  client.print(";");
  client.print(z);
  client.print("/");

}