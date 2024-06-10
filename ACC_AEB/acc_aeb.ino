#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

std_msgs::Float32 distance_msg;
float distances[5] = {0.0, 0.0, 0.0, 0.0, 0.0};
float xt = 0.0;
int acc = 0;

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
    
    // Update the acc variable
    if (xt > 50) {
        acc = 1;
    } else {
        acc = 0;
    }
}

ros::Subscriber<std_msgs::Float32> sub("distance_topic", distanceCallback);

void setup() {
    nh.initNode();
    nh.subscribe(sub);
}

void loop() {
    nh.spinOnce();
    delay(200);  // Delay to match the 0.2 second interval of the sender
}
