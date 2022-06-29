#include <Arduino_LSM6DS3.h>
#include <WiFiNINA.h>

#define LED (13)

const char ssid[] = "vsis-raspberry-pi";
const char pass[] = "raspberryvsis-pi3";
const char host[] = "192.168.1.148";

// const char ssid[] = "vsis-raspberry-pi2";
// const char pass[] = "raspberryvsis-pi3";
// const char host[] = "192.168.0.148";

const uint16_t port = 8080;

unsigned long prev_time;
double angle;
double prev_angle = 0;
double prev_gyro_x;
double idle_time;

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
    for(int i=0; i<10;++i){
      digitalWrite(LED, HIGH);
      delay(100);
      digitalWrite(LED, LOW);
      delay(100);
    }
  }
  digitalWrite(LED, HIGH);

  if(!client.connect(host, port)){
      while(1){
      digitalWrite(LED, HIGH);
      delay(100);
      digitalWrite(LED, LOW);
      delay(1000);
    }
  }
  prev_time = millis();
}

void loop(){
  float gyro_x, gyro_y, gyro_z;
  getGyro(gyro_x, gyro_y, gyro_z);

  gyro_x -= 0.34;
  angle = angle + (gyro_x+prev_gyro_x)/(double)2000 *(millis()-prev_time);
  if(abs(prev_angle-angle) < 0.05){
    angle = prev_angle;
    idle_time += millis()-prev_time;
    if(idle_time > 5000){
      angle = 0;
      gyro_x = 0;
      idle_time = 0;
      client.print("R");
      delay(1000);
    }
  }else{
    idle_time = 0;
  }
  
  prev_time = millis();
  prev_angle = angle;
  prev_gyro_x = gyro_x;
  client.print(angle);
  client.print(";");
}