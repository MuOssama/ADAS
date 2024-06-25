#!/usr/bin/env python

import rospy
import time
from sensor_msgs.msg import LaserScan

# Initialize variables
xt_old = 0  # Previous distance reading
dt = 0.1  # Time interval in seconds (100 ms)
readings = []  # List to store the lidar readings

def edgeDetecting(readings):
    # Dummy implementation for edgeDetecting function
    # Replace with actual edge detection logic
    return readings, sum(readings) / len(readings) if readings else 0

def lidar_callback(data):
    global readings
    readings = data.ranges
    for reading in readings:
        print(reading)

def main():
    global xt_old

    # Initialize ROS node
    rospy.init_node('velocity_calculator', anonymous=True)

    # Subscribe to the lidar topic
    rospy.Subscriber('/scan', LaserScan, lidar_callback)

    # Set loop rate to match the desired time interval
    rate = rospy.Rate(10)  # 10 Hz (100 ms)

    while not rospy.is_shutdown():
        xt_new = edgeDetecting(readings)[1]  # Get the new distance reading
        
        # Calculate the velocity
        vt = (xt_new - xt_old) / dt
        
        # Print the velocity
        rospy.loginfo(f"Velocity: {vt} units/s")
        
        # Update the old distance reading
        xt_old = xt_new
        
        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
