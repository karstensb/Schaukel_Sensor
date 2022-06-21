#include <Arduino_LSM6DS3.h>
#include <SPI.h>
#include <WiFiNINA.h>

const char ssid[] = "vsis-raspberry-pi";
const char pass[] = "raspberryvsis-pi3";

const uint16_t port = 8080;
const char host[] = "192.168.1.148";

unsigned long prev_time;
double angle;
double prev_gyro_x;

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
     //Serial.println("Failed to initialize IMU!");
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
  prev_time = millis();
}

void loop(){
  float gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z;
  getGyro(gyro_x, gyro_y, gyro_z);

  gyro_x -= 0.4;
  angle = angle + (gyro_x+prev_gyro_x)/(double)2000 *(millis()-prev_time);
  prev_time = millis();
  prev_gyro_x = gyro_x;
  client.print(angle);
  client.print(";");
  //Serial.println(angle);

  //getAccel(accel_x, accel_y, accel_z);
  // client.print(gyro_x);
  // client.print(";");
  // client.print(gyro_y);
  // client.print(";");
  // client.print(gyro_z);
  // client.print(";");
  // client.print(accel_x);
  // client.print(";");
  // client.print(accel_y);
  // client.print(";");
  // client.print(accel_z);
  // client.print("/");
}