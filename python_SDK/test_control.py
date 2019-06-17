# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:26:14 2019

@author: xumw1
"""
import time
import numpy as np
from UArm_SDK_FK import UArm_SDK

UArm = UArm_SDK()

position_start = np.array([0.25, 0, 0.05])
UArm.control_uarm_via_traj(position_start, 0, 0, 0.5)
UArm.control_uarm_via_traj(position_start, 0, 1, 0.5)
time.sleep(1)
position_end = np.array([0.2, 0, 0.15])
UArm.control_uarm_via_traj(position_end, 0, 1, 0.5)
time.sleep(2)
position_start = np.array([0.25, 0, 0.05])
UArm.control_uarm_via_traj(position_start, 0, 1, 0.5)
UArm.control_uarm_via_traj(position_start, 0, 0, 0.5)

del UArm