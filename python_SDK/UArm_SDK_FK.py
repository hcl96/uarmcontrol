# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:21:16 2019

@author: xumw1
"""
import time
import numpy as np
import csv

import modern_robotics as mr
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

        self.gripper_temp = 0       # keep track of gripper state

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
            joint_angles, 5-vector: [theta1, theta2, theta3, theta4, pump state] in degrees
            dt, time step
        '''

        wait = True

        self.swift.set_servo_angle(
            servo_id=0, angle=joint_angles[0] + 90, speed=5000, wait=wait)
        time.sleep(dt/4)
        self.swift.set_servo_angle(
            servo_id=1, angle=joint_angles[1], speed=5000, wait=wait)
        time.sleep(dt/4)
        self.swift.set_servo_angle(
            servo_id=2, angle=joint_angles[2] - joint_angles[1], speed=5000, wait=wait)
        time.sleep(dt/4)
        self.swift.set_servo_angle(
            servo_id=3, angle=180 - joint_angles[3], speed=5000, wait=wait)
        time.sleep(dt/4)
        if joint_angles[4] > 0:
            self.swift.set_pump(on=True)
        elif joint_angles[4] == 0:
            self.swift.set_pump(on=False)
        else:
            print("ERROR")

    def control_uarm_via_traj(self, position, wrist_angle, pump_state, dt):
        '''
        set end effector position, wrist angle and pump state via SDK
        input:
            position, 3-vector: [px, py, pz]
            wrist_angle: wrist angle in rad
            pump_state: bool, 0 - off, 1 - on
        '''   
        px, py, pz = position[0], position[1], position[2]
        # conver m to mm
        px *= 1000
        py *= 1000
        pz *= 1000

        # change end effector position
        e = self.swift.set_position(x=px, y=py, z=pz, speed=100000, wait=True)
        print(e)

        # change wrist angle
        self.swift.set_wrist(90 - wrist_angle * 180 / PI)

        if self.gripper_temp == 0 and pump_state == 1:
            # enable suction cup
            self.swift.set_pump(on=True, wait=True)
            print('pump on')
            self.gripper_temp = 1
        if self.gripper_temp == 1 and pump_state == 0:
            # disable suction cup
            self.swift.set_pump(on=False, wait=True)
            print('pump off')
            self.gripper_temp = 0

        time.sleep(dt)


def convert_FK(results):
    '''
    convert joint angles to end effector position
    '''
    H0 = 0.0723
    H1 = 0.0333
    L1 = 0.0132
    L2 = 0.14207
    L3 = 0.1585
    L4 = 0.0566
    H5 = 0.0751

    # M: The home configuration of the end-effector
    M = np.array([[1, 0, 0, L1 + L2 + L3 + L4],
                  [0, 1, 0, 0],
                  [0, 0, 1, H0 + H1 - H5],
                  [0, 0, 0, 1]])
    Slist = np.array([[0, 0, 1, 0, 0, 0],
                      [0, -1, 0, H0 + H1, 0, -L1],
                      [0, 1, 0, -H0 - H1, 0, L1 + L2],
                      [0, -1, 0, H0 + H1, 0, - L1 - L2 - L3],
                      [0, 0, 1, 0, -L1 - L2 - L3 - L4, 0]]).T

    results_FK = results.copy()
    for i in range(results_FK.shape[0]):
        thetalist = np.hstack(
            (results[i, :3], (results[i, 2] - results[i, 1]), results[i, 4]))
        mat = mr.FKinSpace(M, Slist, thetalist)
        position = mat[:3, 3]
        results_FK[i, :3] = position

    return results_FK


if __name__ == '__main__':
    UArm = UArm_SDK()

    # read csv file
    results = []
    with open("config_mat.csv") as csvfile:
        # change contents to floats
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:  # each row is a list
            results.append(row)

    results = np.array(results)
    print("RESULTS", results)

    # convert joint angles to end-effector position to avoid jitterness
    results_FK = convert_FK(results)
    print("RESULTS_FK", results_FK)

    # run
    for cmd in results_FK:
        UArm.control_uarm_via_traj(cmd[:3], cmd[3], cmd[4], 0.005)

    del UArm
