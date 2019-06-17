# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:34:13 2019

@author: xumw1
"""
import csv
import time
import numpy as np
import pandas as pd

from UArm_SDK import UArm_SDK

class UArm_traj(UArm_SDK):
    
    def __init__(self):
        super().__init__()
        
    def get_csv_row(self, filename):
    # read csv file using generator
        with open(filename) as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                yield row
                
    def get_csv_full(self, filename):
        c = pd.read_csv(filename, header=None)
        return c.to_numpy()
                
    def control_uarm_via_traj(self, filename, dt):
        gripper_temp = 0
        
        mat = self.get_csv_full(filename)
        if mat[:,9].mean() <= 1:
            # convert meter to mm
            mat[:, 9:12] *= 1000
        for item in mat:
#        for item in self.get_csv_row(filename):
            # 9 10 11 12: px py pz gripper
#            px, py, pz, gripper = float(item[9]), float(item[10]), float(item[11]), float(item[12])
            px, py, pz, gripper = item[9], item[10], item[11], item[12]
            print('px {} py {} pz {} gripper {}'.format(px, py, pz, gripper))
            # move robot
            e = self.swift.set_position(x=px, y=py, z=pz, speed=100000, wait=True)
            print(e)
            if gripper_temp == 0 and gripper == 1:
                # enable suction cup
#                time.sleep(5)
                self.swift.set_pump(on=True, wait=False)
                print('pump on')
                gripper_temp = 1
            if gripper_temp == 1 and gripper == 0:
                # disable suction cup
                self.swift.set_pump(on=False, wait=False)
                print('pump off')
                gripper_temp = 0
           
            time.sleep(dt)
        
        
if __name__ == '__main__':
    UArm = UArm_traj()
    
#    filename = 'milestone2_out_traj.csv'
#    filename = 'test_traj.csv'
    filename = 'trajectory.csv'
    dt = 0.02
    
#    time.sleep(10)
    UArm.control_uarm_via_traj(filename, dt)
    
    del UArm