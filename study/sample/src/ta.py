#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

data = 0
value = 0

def callback(msg):
    global data, value
    data = msg.data
    value = data*100
    
rospy.init_node('ta')
sub = rospy.Subscriber('memo1', Int32, callback)
pub = rospy.Publisher('memo2', Int32, queue_size=10)

while not rospy.is_shutdown():
    rospy.wait_for_message('memo1', Int32)
    pub.publish(value)
    
