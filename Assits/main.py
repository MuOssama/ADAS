#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from assists import *

# Initialize a list to store the index and reading pairs
index_reading_pairs = []
# Initialize variables
xt_old = 0.0  # Previous distance reading
dt = 10.0  # Time interval, 1 Hz as the lidar spins at 10 hz 
rate = None
vt = 0.0

def callback(data):
    global index_reading_pairs
    global xt_old
    global dt
    global rate
    global vt
    xt_new = 0.0
    index_reading_pairs = []  # Reset the list to store the new set of readings

    # Iterate through each range reading and store the index and reading pair
    for index, reading in enumerate(data.ranges):
        index_reading_pairs.append([index, reading])

    # Calculate the relative velocity
    xt_new = edgeDetecting(index_reading_pairs)[1]  # Get the new distance reading
    vt = (xt_new - xt_old) / (1/dt)  # Calculate the velocity
    xt_old = xt_new  # Update the old distance reading
    
    # Print the velocity
    #rospy.loginfo(vt)

    # Publish the distance status

    pub_numbers.publish(xt_new*100)  # ACC accelerate


    rate.sleep()  # taking calculations at dt hz

def subsNode():
    global rate
    global pub_numbers

    # Initialize the publisher 
    TopicIntName = "AccAeb"
    pub_numbers = rospy.Publisher(TopicIntName, Float32, queue_size=10)

    # Set the rate
    rate = rospy.Rate(dt)  # taking calculations at dt hz

    # Create a subscriber
    rospy.Subscriber("/scan", LaserScan, callback)  # Subscribe to the /scan topic

    rospy.spin()  # Keep the node running

if __name__ == '__main__':
    rospy.init_node('rplidar_listener', anonymous=True)  # Initialize the node
    try:
        subsNode()
    except rospy.ROSInterruptException:
        pass

