import rclpy
from rclpy.node import Node
from google.cloud import texttospeech
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import datetime


class VernieSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        #self.subscription = self.create_subscription(
        #    String,
        #    'speech',
        #    self.listener_callback,
        #    10)
        #self.subscription  # prevent unused variable warning

        self.time_last_press = datetime.datetime.now()
        self.speech_text_index = 0
        self.speech_publisher = self.create_publisher(String,'speech',0)
        self.twist_publisher = self.create_publisher(Twist,'twist',10)
        self.twist_publisher
        self.joy_subscriber = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.joy_subscriber  # prevent unused variable warning



    def joy_callback(self, msg):

        joy_sideways = msg.axes[0]
        joy_forward_backward = msg.axes[1]

        twist_msg = Twist()
        twist_msg.linear.x = joy_forward_backward
        twist_msg.angular.z = joy_sideways

        self.twist_publisher.publish(twist_msg)

       # self.get_logger().info('sideways value: "%s"' % joy_sideways)
       # self.get_logger().info('forward value: "%s"' % joy_forward_backward)
       # self.get_logger().info('joy msg: "%s"' % msg)

        button_a = msg.buttons[0]
        if button_a == 1:
            self.button_a_press()
            self.get_logger().info('joy msg: "%s"' % "button A pressed")

    def button_a_press(self):

        speech_text = ["hei mit navn er Lisi. Mine beste venner er Liv og Siri - de bare elsker jeg å leker med!",
                       "oi oi, hør om min dag på skolen. Jeg spurte læren min hvorfor jeg må lære engelsk på skolen. Hun svarte fordi halve verden snakken engelsk. Jeg svarte, jammen er det ikke nok da?",
                       "min første dag på skolen var ganske morsom! Læren min fortalte oss at om vi skulle på do skulle jeg bare rekke opp hånden. Jeg spurte, hjelper det da?"]

        self.speech_text_index
        speech_msg = String()
        speech_msg.data = speech_text[self.speech_text_index]

        print("speech index", self.speech_text_index)
        print("speech text", speech_text[self.speech_text_index])
        print("speech text length", len(speech_text))




        time_since_last_press = datetime.datetime.now() - self.time_last_press

        if time_since_last_press.microseconds > 200000:
            self.time_last_press = datetime.datetime.now()
            self.speech_text_index += 1
            if self.speech_text_index >= len(speech_text):
                self.speech_text_index = 0
            self.speech_publisher.publish(speech_msg)





def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = VernieSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()