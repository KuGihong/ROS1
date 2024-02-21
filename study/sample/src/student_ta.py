#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
data = 0

def callback(msg):
    global data
    data = msg.data
    
rospy.init_node('student')
sub = rospy.Subscriber('memo2', Int32, callback)

while not rospy.is_shutdown():
    print(data)
