import rospy
from std_msgs.msg import String
from heart_rate_msg.msg import heart_rate  # Import the custom message
import serial
import time

def publish_heart_rate(beat_avg, beat_status):
    # Initialize the ROS node with the name 'heart_rate_publisher'
    rospy.init_node('heart_rate_publisher', anonymous=True)

    pub = rospy.Publisher('heart_rate', heart_rate, queue_size=10)

    # Create an instance of the custom message
    msg = heart_rate()

    # Populate the message fields with the data
    msg.header.stamp = rospy.Time.now()  # Current time
    msg.beat_avg = beat_avg
    msg.beat_status = beat_status

    # Publish the message
    pub.publish(msg)

    # Print the data being published
    if msg.beat_status == "WARNING":
        rospy.logwarn("Beat Average: %.2f, Beat Status: %s", msg.beat_avg, msg.beat_status)
    elif msg.beat_status == "DANGER":
        rospy.logerr("Beat Average: %.2f, Beat Status: %s", msg.beat_avg, msg.beat_status)
    else:
        rospy.loginfo("Beat Average: %.2f, Beat Status: %s", msg.beat_avg, msg.beat_status)

# Callback 함수: 토픽 메시지를 받았을 때 실행될 함수
def callback(data):
    rospy.loginfo("Received message: %s", data.data)
    
    # 아두이노로 메시지 전송
    message = data.data
    ser.write(message.encode('utf-8'))
    rospy.loginfo("Sent message to Arduino: %s", message)
    time.sleep(1/2)  # 1초 동안 대기 (원하는 대기 시간으로 수정)

def listener():
    # rospy.init_node("aircraft_status")  # 노드 초기화
    rospy.Subscriber("aircraft_status", String, callback)  # 토픽 이름을 수정

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)  # Serial port settings (change '/dev/ttyACM1' to your actual port)
    while not rospy.is_shutdown():
        line = ser.readline().decode().strip()  # Read and decode serial data
        if line:
            beat_avg, beat_status = line.split(",")  # Split CSV data
            beat_avg = float(beat_avg)  # Convert string to float

            # Publish the data as a ROS message
            publish_heart_rate(beat_avg, beat_status)
            listener()
