import sys
import signal
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C... exit image pub.')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class ImagePub:

  def __init__(self):

    self.publisher_ = rospy.Publisher('/video_frames', Image, queue_size=10)

    timer_period = 0.1

    self.timer = rospy.Timer(timer_period, self.timer_callback)

    self.cap = cv2.VideoCapture(0)

    self.br = CvBridge()

  def timer_callback(self):
    ret, frame = self.cap.read()

    if ret == True:
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))

    self.get_logger().info('Publishing video frame')

def main():

  rospy.init_node('image_pub', anonymous=True)

  image_pub = ImagePub()

  rospy.spin()

  image_pub.destroy_node()

  rospy.shutdown()

if __name__ == '__main__':
  main()

