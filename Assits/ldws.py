#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import Int32, String

NodeName = "LDWS"
TopicStrName = "LDWS"

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node(NodeName)

    # Create a publisher for the 'lane dep warning system' topic
    pub_ldws = rospy.Publisher(TopicStrName, Int32, queue_size=10)


    # Set the loop rate (adjust as needed)
    rate = rospy.Rate(100)  # 1 Hz
   
    while not rospy.is_shutdown():
        try:
            ldws_status = False  #this variable is used for sending to the microcontroller whether if the vehicle is deptured from the lane or not
	    #all the code (Algorithm) should be written here !
	    #Note after the algorithm is finished, change ldws_status (i.e ldws_status  = True if the vehile is dep and Flase if not)
            pub_ldws.publish(ldws_status)
            if ldws_status == False:
            	rospy.loginfo("lane depature state: False")
            else :
            	rospy.loginfo("lane depature state: True")
        except rospy.ROSException as e:
            rospy.logerr("Error waiting for message on topic ")

        # Sleep to maintain the loop rate
        rate.sleep()

