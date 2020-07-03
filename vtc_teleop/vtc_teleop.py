#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
import tty, termios
import select, sys

MAX_LIN_VEL = 0.583 #burgerと同じ
MAX_ANG_VEL = 2.84

LIN_VEL_STEP_SIZE = 0.05
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control robot!
----------------------------------
Moving around:
        w
   a    s    d
        x
w/x : increase/decrease linear velocity ( ~ 0.583)
a/d : increase/decrease angular velocity ( ~ 2.84)
space key, s : force stop
CTRL-C to quit
"""

e = """
Communications Failed
"""
def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def checkLinearLimitVelocity(vel):
    if vel < -MAX_LIN_VEL:
        vel = -MAX_LIN_VEL
    elif vel > MAX_LIN_VEL:
        vel = MAX_LIN_VEL
    else:
        vel = vel
    
    return vel

def checkAngularLimitVelocity(vel):
    if vel < -MAX_ANG_VEL:
        vel = -MAX_ANG_VEL
    elif vel > MAX_ANG_VEL:
        vel = MAX_ANG_VEL
    else:
        vel = vel
    
    return vel

def getkey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin],[],[], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = termios.tcgetattr(sys.stdin)

rospy.init_node('vtc_teleop_node',anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

status = 0
target_linear_vel   = 0.0
target_angular_vel  = 0.0
control_linear_vel  = 0.0
control_angular_vel = 0.0

try: 
    print(msg)
    while(1):
        key = getkey()
        if key == 'w' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
        elif key == 'x' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
        elif key == 'a' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
        elif key == 'd' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
        elif key == ' ' or key == 's' :
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
        else:
                if (key == '\x03'):
                    break
            
        if status == 20:
                print(msg)
                status = 0
            
        twist = Twist()

        control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
        twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

        control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

        pub.publish(twist)

except:
    print(e)

finally:
    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    pub.publish(twist)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)