#!/usr/bin/python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def talker():

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        cmd = Twist()
        cmd.linear.x = 1.5
        cmd.angular.z = 1.0
        pub.publish(cmd)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
