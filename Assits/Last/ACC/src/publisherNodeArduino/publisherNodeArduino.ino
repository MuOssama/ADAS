#include <ros.h>
#include <std_msgs/Int32.h>
#include <Arduino.h>
ros::NodeHandle nh;
int Speed = 0;
int RPWM = 5;
int LPWM = 23;
#define R 0
#define L 1
int IN1 = 18;
int IN2 = 19;
int IN3 = 21;
int IN4 = 22;
const int trigPin = 32;
const int echoPin = 33;
long duration;
double distance;
void speedCallback(const std_msgs::Int32 &msg) {
  Speed = msg.data;
  //digitalWrite(2,LOW);
  if(Speed >150)
  Speed =150;
}
void AEBCallback(const std_msgs::Int32 &msg) {
  if( msg.data==1){
  stopBot();  }
  else if(msg.data==0){
      digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
    }
  //digitalWrite(2,LOW);

}
void LDWSCallback(const std_msgs::Int32 &msg) {
  int LDWS_state = msg.data;
  if(LDWS_state == HIGH){
  digitalWrite(2,LOW);
  //buzzer will be fired
  }
}
std_msgs::Int32 distance_sensor_msg;
ros::Publisher distance_sensor_pub("distance_sensor_data", &distance_sensor_msg);
ros::Subscriber<std_msgs::Int32> speed_sub("Speed", speedCallback);
ros::Subscriber<std_msgs::Int32> AEB_sub("AEB", AEBCallback);
ros::Subscriber<std_msgs::Int32> LDWS_sub("LDWS", LDWSCallback);




void setup() {
  nh.initNode();
  nh.advertise(distance_sensor_pub);
  nh.subscribe(speed_sub);
  nh.subscribe(AEB_sub);
  nh.subscribe(LDWS_sub);
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(2, OUTPUT);
  ledcSetup(R, 5000, 8);
  ledcAttachPin(RPWM, R);
  ledcSetup(L, 5000, 8);
  ledcAttachPin(LPWM, L);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void handleBluetoothSignal(char signal) {
  switch (signal) {
    case '0': Speed = 100; break;
    case '1': Speed = 110; break;
    case '2': Speed = 120; break;
    case '3': Speed = 130; break;
    case '4': Speed = 140; break;
    case '5': Speed = 150; break;
    case '6': Speed = 180; break;
    case '7': Speed = 200; break;
    case '8': Speed = 220; break;
    case '9': Speed = 240; break;
    case 'q': Speed = 255; break;
    case 'F': driveForward(); break;
    case 'B': driveBackward(); break;
    case 'L': driveLeft(); break;
    case 'R': driveRight(); break;
    case 'S': stopBot(); break;
    case 'A': handleAcc(); break;
  }
}

void driveForward() {
  ledcWrite(R, Speed);
  ledcWrite(L, Speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void driveBackward() {
  ledcWrite(R, Speed);
  ledcWrite(L, Speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void driveLeft() {
  ledcWrite(R, Speed);
  ledcWrite(L, Speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void driveRight() {
  ledcWrite(R, Speed);
  ledcWrite(L, Speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void stopBot() {
  ledcWrite(R, Speed);
  ledcWrite(L, Speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void handleAcc() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;
    /*if(distance > 50)
      distance = 50;*/
    driveForward();

}
void loop() {
    digitalWrite(2,HIGH);

  // Read sensor data (modify this part based on your sensor)
  handleAcc();
  // Publish sensor data to ROS
  distance_sensor_msg.data = distance*10;
  distance_sensor_pub.publish(&distance_sensor_msg);
  
  nh.spinOnce();
  delay(25);  // Adjust the delay based on your sensor update rate
}
