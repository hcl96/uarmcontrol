# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:21:16 2019

@author: xumw1
"""
import time
import numpy as np
import csv

from uarm.wrapper import SwiftAPI
PI = 3.14159


class UArm_SDK(object):
    def __init__(self):
        '''
        connect to UArm
        '''
        self.swift = SwiftAPI()
        
        self.swift.connect()
        self.swift.get_power_status()
        print(self.swift.get_device_info())
        
        self.swift.reset(wait=True)   # back to home position
        print('init complete')

    def __del__(self):
        '''
        disconnect UArm
        '''
        self.swift.disconnect()
        print('uarm disconnected')


    def set_servo_angle(self, joint_angles, dt):
        '''
        set servo angle via SDK
        input:
            joint_angles, 5-vector: [theta1, theta2, theta3, theta4, pump state]
            dt, time step
        '''
        
        wait = True

        self.swift.set_servo_angle(
            servo_id=0, angle=joint_angles[0] + 90, speed=5000, wait=wait)
        time.sleep(dt / 4)
        self.swift.set_servo_angle(
            servo_id=1, angle=joint_angles[1], speed=5000, wait=wait)
        time.sleep(dt / 4)
        self.swift.set_servo_angle(
            servo_id=2, angle=joint_angles[2] - joint_angles[1], speed=5000, wait=wait)
        time.sleep(dt / 4)
        self.swift.set_servo_angle(
            servo_id=3, angle=180 - joint_angles[3], speed=5000, wait=wait)
        time.sleep(dt / 4)
        if joint_angles[4] > 0:
            self.swift.set_pump(on=True)
        elif joint_angles[4] == 0:
            self.swift.set_pump(on=False)
        else:
            print("ERROR")


if __name__ == '__main__':
    UArm = UArm_SDK()

    # read csv file
    results = []
    with open("config_mat.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)
    # update csv from radians to degrees
    
    results = np.array(results)
    print("RESULTS", results)
    
    # convert rad to deg
    results[:,:-1] = np.multiply(results[:,:-1], (180/PI))
    print("RESULTS", results)

    # run
    for i in results:
        print("INPUTING", i)
        UArm.set_servo_angle(i, 0.05)
        
    del UArm


