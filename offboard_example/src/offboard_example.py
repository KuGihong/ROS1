#!/usr/bin/env python3

import numpy as np
import rospy
import time
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped


class OffboardRos:
    def __init__(self):
        self.pub_local_pose = 1
        self.pose = [0.0, 0.0, 0.0]
        self.quat = [0.0, 0.0, 0.0, 0.0]
        
        self.command = PoseStamped()
        self.command.pose.position.x = 10.0
        self.command.pose.position.y = 0.0
        self.command.pose.position.z = 0.0

    def callback_pose(self, data):
        self.pose[0] = data.pose.pose.position.x
        self.pose[1] = data.pose.pose.position.y
        self.pose[2] = data.pose.pose.position.z

        self.quat[0] = data.pose.pose.orientation.x
        self.quat[1] = data.pose.pose.orientation.y
        self.quat[2] = data.pose.pose.orientation.z
        self.quat[3] = data.pose.pose.orientation.w
        

    def main(self):
    
        self.sub_pose = rospy.Subscriber("/mavros/global_position/local", Odometry, self.callback_pose, queue_size=2)
        self.pub_command = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=2)
        
        rate = rospy.Rate(30)
        
        br1 = tf.TransformBroadcaster()
        print("start offboar example")
        while not rospy.is_shutdown():

            br1.sendTransform(self.pose, self.quat, rospy.Time.now(), "px4", "world")
            self.pub_command.publish(self.command)
            
            rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('offboard_example', anonymous=True)
        OFF = OffboardRos()
        OFF.main()
    except rospy.ROSInterruptException:
        pass
