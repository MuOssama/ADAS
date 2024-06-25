#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import Int32, String

NodeName = "AEB"
TopicIntName = "distance_sensor_data"
TopicStrName = "AEB"

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node(NodeName)

    # Create a publisher for the 'Speed' topic
    pub_speed = rospy.Publisher(TopicStrName, Int32, queue_size=10)


    # Set the loop rate (adjust as needed)
    rate = rospy.Rate(100)  # 1 Hz

    while not rospy.is_shutdown():
        try:
            # Wait for a message on the specified topic
            int_message = rospy.wait_for_message(TopicIntName, Int32)
            rospy.loginfo("Received Distance: %d", int_message.data)
            distance = int_message.data

            if distance<70:
                brake_status = 1
                rospy.loginfo("AEB: Braking Enabled")
            else :
                brake_status = 0
                rospy.loginfo("AEB: Braking Disabled")
            pub_speed.publish(brake_status)

        except rospy.ROSException as e:
            rospy.logerr("Error waiting for message on topic ")

        # Sleep to maintain the loop rate
        rate.sleep()

