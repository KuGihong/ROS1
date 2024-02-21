import signal
import sys
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C... exit image sub.')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class ImageSub():

  def __init__(self):

    self.subscriber = rospy.Subscriber('video_frames', Image, self.listener_callback)
    self.subscriber

    self.br = CvBridge()

  def listener_callback(self, data):

    self.get_logger().info('Receiving video frame')

    current_frame = self.br.imgmsg_to_cv2(data)

    # Display image
    cv2.imshow("camera", current_frame)

    cv2.waitKey(1)

def main():

  rospy.init_node('image_sub', anonymous=True)

  image_sub = ImageSub()

  rospy.spin()

  image_sub.destroy_node()

  rospy.shutdown()

if __name__ == '__main__':
  main()

