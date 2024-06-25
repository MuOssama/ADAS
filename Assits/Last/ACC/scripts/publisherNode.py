#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32, String
import time

NodeName = "test"
TopicIntName = "IntData"
TopicStrName = "StrData"

def publisher_node():
    dataInt = 0
    dataStr = "hello" 
    # Initialize the ROS node
    rospy.init_node(NodeName, anonymous=True)

    # Create a publisher for the 'random_numbers' topic
    pub_numbers = rospy.Publisher(TopicIntName, Int32, queue_size=10)

    # Create a publisher for the 'random_strings' topic
    pub_strings = rospy.Publisher(TopicStrName, String, queue_size=10)

    # Set the loop rate (adjust as needed)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        dataInt += 1
        rospy.loginfo(dataInt)
        pub_numbers.publish(dataInt)

   
        rospy.loginfo(dataStr)

        pub_strings.publish(dataStr)

        # Sleep to achieve the desired loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher_node()
    except rospy.ROSInterruptException:
        pass