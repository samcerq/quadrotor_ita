#!/usr/bin/env python

from std_msgs.msg import Float64MultiArray 
from geometry_msgs.msg import Twist,Vector3
import termios, fcntl, sys, os
import rospy

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

rospy.init_node('keyboard')
msg = Twist()
lin_vel = Vector3()
ang_vel = Vector3()
ang_vel.x = 0
ang_vel.y = 0
ang_vel.z = 0
msg.linear = lin_vel
msg.angular = ang_vel
try:
    while not rospy.is_shutdown():
        try:
            c = sys.stdin.read(1)
            if c=='w':
                lin_vel.x = 0.5
                lin_vel.y = 0
                lin_vel.z = 0
            elif c=='s':
                lin_vel.x = -0.5
                lin_vel.y = 0
                lin_vel.z = 0
            elif c=='d':
                lin_vel.x = 0
                lin_vel.y = 0.5
                lin_vel.z = 0
            elif c=='a':
                lin_vel.x = 0
                lin_vel.y = -0.5
                lin_vel.z = 0
            elif c==' ':
                lin_vel.x = 0
                lin_vel.y = 0
                lin_vel.z = 0.5
            elif c=='b':
                lin_vel.x = 0
                lin_vel.y = 0
                lin_vel.z = -0.5
            else:
                lin_vel.x = 0
                lin_vel.y = 0
                lin_vel.z = 0
            while c!='':
                c = sys.stdin.read(1)
        except IOError: pass
        pub.publish(msg)
        rospy.sleep(0.1)
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
