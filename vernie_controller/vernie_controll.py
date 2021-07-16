import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs import Twist

import hashlib
import os
import re
import subprocess
import time

from pylgbst import *
from pylgbst.hub import MoveHub

forward = FORWARD = right = RIGHT = 1
backward = BACKWARD = left = LEFT = -1
straight = STRAIGHT = 0

VERNIE_TO_MOTOR_DEGREES = 2.6
VERNIE_SINGLE_MOVE = 430


class Vernie(MoveHub):
    def __init__(self):
        super(Vernie, self).__init__()

        print("Initializing Vernie")

        while True:
            required_devices = (self.vision_sensor, self.motor_external)
            if None not in required_devices:
                break
            log.debug("Waiting for required devices to appear: %s", required_devices)
            time.sleep(1)

        self._head_position = 0
        self.motor_external.subscribe(self._external_motor_data)

        self._reset_head()
#        self.say("ready")
        time.sleep(1)

#    def say(self, phrase):
#        if phrase in SPEECH_LANG_MAP[self.language]:
#            phrase = SPEECH_LANG_MAP[self.language][phrase]
#        say(phrase)

    def _external_motor_data(self, data):
        log.debug("External motor position: %s", data)
        self._head_position = data

    def _reset_head(self):
        self.motor_external.timed(1, -0.2)
        self.head(RIGHT, angle=45)

    def head(self, direction=RIGHT, angle=25, speed=0.1):
        if direction == STRAIGHT:
            angle = -self._head_position
            direction = 1

        self.motor_external.angled(direction * angle, speed)

    def turn(self, direction, degrees=90, speed=0.3):
        self.head(STRAIGHT, speed=0.5)
        self.head(direction, 35, 1)
        self.motor_AB.angled(int(VERNIE_TO_MOTOR_DEGREES * degrees), speed * direction, -speed * direction)
        self.head(STRAIGHT, speed=0.5)

    def move(self, direction, distance=1, speed=0.2):
        self.head(STRAIGHT, speed=0.5)
        self.motor_AB.angled(distance * VERNIE_SINGLE_MOVE, speed * direction, speed * direction)

    def shot(self):
        self.motor_external.timed(0.5)
        self.head(STRAIGHT)
        self.head(STRAIGHT)

class VernieController(Node):

    def __init__(self):
        super().__init__('vernie_controller_node')

        self.received_twist = Twist
        self.received_connection_status = False
        self.connection_subscription = self.create_subscription(
            Bool,
            'connection',
            self.connection_listener,
            10)
        self.connection_subscription  # prevent unused variable warning

        self.twist_subscription = self.create_subscription(
            Twist,
            'twist',
            self.twist_listener,
            10)
        self.twist_subscription  # prevent unused variable warning


    def connection_listener(self, msg):
        self.received_connection_status = msg.data

    def twist_listener(self, msg):
        self.received_twist = msg

def main(args=None):
   
  # print("test hello")

  # robot = Vernie()

  # print("robot initialized")

  # robot.turn(LEFT, 90)
  # robot.turn(RIGHT, 90)

   #print("turned?")

    rclpy.init(args=args)

    vernie_controller_node = VernieController()

    rclpy.spin(vernie_controller_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()