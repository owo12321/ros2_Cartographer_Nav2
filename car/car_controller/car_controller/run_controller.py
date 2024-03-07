#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO

import threading
import time


# 左轮引脚
l = [31,33,29,35]
# 右轮引脚
r = [15,11,13,12]

# 初始化引脚
def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([11,12,13,15,29,31,33,35], GPIO.OUT)

# 把左边所有引脚设为LOW
def offleft():
    GPIO.output(l, GPIO.LOW)
# 把右边所有引脚设为LOW
def offright():
    GPIO.output(r, GPIO.LOW)


flag = True # 保持线程运行的flag
dleft = 1   # 左轮方向 1前-1后
dright = 1  # 右轮方向
fleft = 0   # 左轮频率
fright = 0  # 右轮频率

# 左轮线程
def left():
    global dleft
    global fleft
    i = 1
    while flag:
        f = fleft
        offleft()
        if f==0:
            continue

        lpin = l.copy()
        if dleft == -1:
            lpin.reverse()

        GPIO.output(lpin[i], GPIO.HIGH)
        time.sleep(1/f)

        i = (i+1)%4

# 右轮线程
def right():
    global dright
    global fright
    i = 1
    while flag:
        f = fright
        offright()
        if f==0:
            continue

        rpin = r.copy()
        if dright == -1:
            rpin.reverse()

        GPIO.output(rpin[i], GPIO.HIGH)
        time.sleep(1/f)

        i = (i+1)%4


class CarController(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("%s已启动" % name)
        # 创建订阅者
        self.command_subscribe_ = self.create_subscription(Twist,"cmd_vel",self.command_callback,10)

    def command_callback(self,msg):
        self.get_logger().info('===================')
        self.get_logger().info('get massage')


        global dleft
        global fleft
        global dright
        global fright

        v = msg.linear.x
        w = msg.angular.z

        l = 0.22
        vl = v - (w*l)/2
        vr = v + (w*l)/2

        dleft=1 if vl>0 else -1
        dright=1 if vr>0 else -1

        fleft = dleft*vl / (0.06*3.1415926535897) * 200
        fright = dright*vr / (0.06*3.1415926535897) * 200

        self.get_logger().info(f'msg.angular = [{msg.angular.x, msg.angular.y, msg.angular.z}]')
        self.get_logger().info(f'msg.linear = [{msg.linear.x, msg.linear.y, msg.linear.z}]')
        self.get_logger().info(f'dl={dleft}, fl={fleft}, dr={dright}, fr={fright}')
        self.get_logger().info('===================\n')

def main(args=None):
    global flag
    
    init()
    lthred = threading.Thread(target=left)
    rthred = threading.Thread(target=right)
    lthred.start()
    rthred.start()

    rclpy.init(args=args) # 初始化rclpy
    node = CarController("run_controller")  # 新建一个节点
    try:
        rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    except KeyboardInterrupt:
        # 关闭进程，清理引脚
        flag = False
        offleft()
        offright()
        GPIO.cleanup()
        print('清理完毕')
    rclpy.shutdown() # 关闭rclpy



