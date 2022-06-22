#include <Arduino_LSM6DS3.h>
#include <WiFiNINA.h>

#define LED (13)

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
  pinMode(LED, OUTPUT);

  if(!IMU.begin()){
    while(1){
      digitalWrite(LED, HIGH);
      delay(1000);
      digitalWrite(LED, LOW);
      delay(100);
    }
  }

  while(WiFi.begin(ssid, pass) != WL_CONNECTED){
    for(int i=0; i<25;++i){
      digitalWrite(LED, HIGH);
      delay(100);
      digitalWrite(LED, LOW);
      delay(100);
    }
  }

  if(!client.connect(host, port)){
      while(1){
      digitalWrite(LED, HIGH);
      delay(100);
      digitalWrite(LED, LOW);
      delay(1000);
    }
  }
  digitalWrite(LED, HIGH);
  prev_time = millis();
}

void loop(){
  float gyro_x, gyro_y, gyro_z;
  getGyro(gyro_x, gyro_y, gyro_z);

  gyro_x -= 0.4;
  angle = angle + (gyro_x+prev_gyro_x)/(double)2000 *(millis()-prev_time);
  prev_time = millis();
  prev_gyro_x = gyro_x;
  client.print(angle);
  client.print(";");
}