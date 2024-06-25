#include <ros.h>
#include <std_msgs/Float32.h>
#include <Arduino.h>
ros::NodeHandle nh;
std_msgs::Float32 speed_msg;
std_msgs::Float32 distance_msg;
float distances[5] = {0.0, 0.0, 0.0, 0.0, 0.0};
float xt = 0.0;
int acc = 0;
int forwardPin = 10;

void distanceCallback(const std_msgs::Float32& msg) {
    // Update the distances array like a stack
    for (int i = 0; i < 4; i++) {
        distances[i] = distances[i + 1];
    }
    distances[4] = msg.data;
    
    // Calculate the average
    float sum = 0.0;
    for (int i = 0; i < 5; i++) {
        sum += distances[i];
    }
    xt = sum / 5.0;
    speed_msg.data = xt;
    // Update the acc variable
    if (xt > 50) {
        acc = 1;
        digitalWrite(forwardPin,HIGH);
    } else {
        digitalWrite(forwardPin,LOW);
    }

}

ros::Subscriber<std_msgs::Float32> sub("AccAeb", &distanceCallback);
ros::Publisher speed_pub("Speed", &speed_msg);

void setup() {
    nh.initNode();
     nh.advertise(speed_pub);
    nh.subscribe(sub);
    pinMode(forwardPin,OUTPUT);
 
    
}

void loop() {

    speed_pub.publish(&speed_msg);
    nh.spinOnce();
    delay(200);  // Delay to match the 0.2 second interval of the sender
}
