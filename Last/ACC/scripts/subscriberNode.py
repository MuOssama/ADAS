#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import Int32, String
from decimal import Decimal, getcontext

getcontext().prec = 20
NodeName = "ACC"
TopicIntName = "distance_sensor_data"
TopicStrName = "Speed"

# Set initial values
prevT = Decimal(time.time())  # Initial time
prevD = 0  # Initial distance
prevVr = 0  # Initial velocity
Speed = 0
cnt = 0
i = -1
aveDistance = [0,0,0,0,0]

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
            distance = Decimal(int_message.data)
            if distance > 500:
                distance=500
            cnt = cnt+1
            aveDistance.insert(5,distance)
            if cnt >= 5:
                n=0
                #arranging array 
                for j in range(0,5):  
                    aveDistance[j] = aveDistance[j+1]
                for k in range(0,5):  
                    rospy.loginfo("Reading %d: %d",k+1, aveDistance[k] )
                    if aveDistance[k] == 0:
                        n =n+1
                if n==5:
                    n=4
                rospy.loginfo("Filtered data: %d", n )
                distance = (aveDistance[0]+aveDistance[1]+aveDistance[2]+aveDistance[3]+aveDistance[4])/(5-n)
                # Update time
                currT = Decimal(time.time()*1000)
                dT = currT - prevT  # time difference in seconds
                rospy.loginfo("Current time: %d",  Decimal(currT) )
                rospy.loginfo("Previous time: %d", Decimal(prevT) )

                rospy.loginfo("Detla time dt: %d", dT )

                # Calculate velocity
                Vr = Decimal(100*(distance - prevD) / dT)
                rospy.loginfo("Current Distance reading: %d", distance )
                rospy.loginfo("Previous Distance reading: %d", prevD )

                # Check for large changes in velocity
                
               # if abs(Vr - prevVr) > abs(Vr):
                #    Vr = 18
                 
                # Calculate speed by accumulating velocity
                Speed = Speed + Vr

                # Update previous values
                prevT = Decimal(currT)
                prevD = distance
                prevVr = Vr

                # Log and publish the calculated speed
                rospy.loginfo("Calculated VR: %f", Vr)
               # rospy.loginfo("Calculated Speed: %f", Speed)
                rospy.loginfo("Calculated average distance: %f", distance)
                
                pub_speed.publish(Vr*7)

        except rospy.ROSException as e:
            rospy.logerr("Error waiting for message on topic ")

        # Sleep to maintain the loop rate
        rate.sleep()

