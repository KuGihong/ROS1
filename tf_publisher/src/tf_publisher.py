#!/usr/bin/env python3

import numpy as np
import rospy
import time
import tf
import turtlesim.msg


class TFBroadcastRos:
    def __init__(self):
        self.pub_local_pose = 1
        self.turtle1_x = 0.0
        self.turtle1_y = 0.0
        self.turtle1_th = 0.0

        self.turtle2_x = 0.0
        self.turtle2_y = 0.0
        self.turtle2_th = 0.0

    def callback_turtle_1(self, msg):
        self.turtle1_x = msg.x
        self.turtle1_y = msg.y
        self.turtle1_th = msg.theta

    def callback_turtle_2(self, msg):
        self.turtle2_x = msg.x
        self.turtle2_y = msg.y
        self.turtle2_th = msg.theta

    def main(self):
        rospy.Subscriber('/turtle1/pose', turtlesim.msg.Pose, self.callback_turtle_1)
        rospy.Subscriber('/turtle2/pose', turtlesim.msg.Pose, self.callback_turtle_2)
        rate = rospy.Rate(30)
        br1 = tf.TransformBroadcaster()
        br2 = tf.TransformBroadcaster()

        while not rospy.is_shutdown():

            print("processing ...")
            pose = (self.turtle1_x, self.turtle1_y, 0)
            angle = tf.transformations.quaternion_from_euler(0, 0, self.turtle1_th)
            br1.sendTransform(pose, angle, rospy.Time.now(), "turtle1", "world")

            pose = (self.turtle2_x, self.turtle2_y, 0)
            angle = tf.transformations.quaternion_from_euler(0, 0, self.turtle2_th)
            br2.sendTransform(pose, angle, rospy.Time.now(), "turtle2", "world")
            #pose = (0.0, 0.0, 0.55)
            #angle = tf.transformations.quaternion_from_euler(0, 0, 0)
            #br2.sendTransform(pose, angle, rospy.Time.now(), "horizontal_lasr_link", "px4")
			
            rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('tf_publisher', anonymous=True)
        TFB = TFBroadcastRos()
        TFB.main()
    except rospy.ROSInterruptException:
        pass
