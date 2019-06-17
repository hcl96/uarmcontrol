# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:21:16 2019

@author: xumw1
"""
import time
import numpy as np

from uarm.wrapper import SwiftAPI

swift = SwiftAPI()

swift.connect()
swift.get_power_status()
print(swift.get_device_info())


T = 2
dt = 0.01 # best we can get: 0.01

N = int(T / dt)

#swift.set_servo_angle(servo_id=0, angle=90)
##time.sleep(3)
#swift.set_servo_angle(servo_id=1, angle=90)
##time.sleep(3)
#swift.set_servo_angle(servo_id=2, angle=0)
##time.sleep(3)
#swift.set_servo_angle(servo_id=3, angle=90)
swift.reset()
time.sleep(3)

swift.set_speed_factor(2)


'''generate configs'''
joint_angles = np.zeros((N, 5))
for i in range(N):
    joint_angles[i, :] = np.array([90, 90 - 90/T * dt * i, 90/T * dt * i, 90, 0])
        
    
# step motor step?
    
for i in range(N):
    swift.set_servo_angle(servo_id=0, angle=joint_angles[i,0])
#    time.sleep(dt/4)
    swift.set_servo_angle(servo_id=1, angle=joint_angles[i,1])
#    time.sleep(dt/4)
    swift.set_servo_angle(servo_id=2, angle=joint_angles[i,2])
#    time.sleep(dt/4)
    swift.set_servo_angle(servo_id=3, angle=joint_angles[i,3])
#    time.sleep(dt/4)
time.sleep(1)
swift.disconnect()