#!/usr/bin/env python2
import rospy

if __name__ == '__main__':
    rospy.init_node("Mu")
    rospy.loginfo("message")
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo("hello")
        rate.sleep()