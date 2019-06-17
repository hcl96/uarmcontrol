# -*- coding: utf-8 -*-
'''
Created on Tue Apr  9 11:19:24 2019

@author: xumw1
'''
import time
import serial

import numpy as np
from test_Gcode import connect_uArm, send_command, test_home


def generate_Gcode(joint_angles):
    '''
    generate Gcode from joint_angles
    '''
    G_code = []
    for ind, joint_angle in enumerate(joint_angles):
#        l = ['G2202 N{} V'.format(i) + str(round(joint_angle[i],5)) for i in range(4)]
#        tmp = ' \r\n '.join(l)
#        G_code.append(tmp)
        for i in range(4):
            G_code.append('#{} G2202 N{} V'.format(4*ind+i+1, i) + str(round(joint_angle[i],5)))

    return G_code


if __name__ == '__main__':
    T = 3
    dt = 0.02  # best we can get: 0.01 stable: 0.1
    N = int(T / dt)

    joint_angles = np.zeros((N, 5))
    for i in range(N):
        joint_angles[i, :] = np.array([90, 90 - 40/T * dt * i, 40/T * dt * i, 90, 0])

    G_code = generate_Gcode(joint_angles)

#    # set up serial port
#    '''
#    Please modifiy serial port setting based on your system
#    '''
#    arduino_data = serial.Serial('com4', baudrate=115200, timeout=3.0)
#
#    print('=====Port Opened=====')
#
#    # read first data
#    connect_uArm(arduino_data)
#
#    # test command
#    test_home(arduino_data)
#    time.sleep(3)
#
#    t0 = time.clock()
#    send_command(arduino_data, command=G_code, time_step=dt/4)
#    print('run time: ', time.clock() - t0)
#
#    # close serial port
#    arduino_data.close()
#    print('=====Port Closed=====')
