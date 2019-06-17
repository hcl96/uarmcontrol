# -*- coding: utf-8 -*-
'''
Created on Thu Apr  4 14:24:25 2019

@author: xumw1
'''

import serial
import time


def connect_uArm(arduino_data):
    print('=====Connecting to uArm=====')
    t0 = time.clock()
    while True:
        count = arduino_data.inWaiting()
        if count != 0:
            rcv = arduino_data.read(count)
            print(str(rcv, 'utf-8'))

        if time.clock() - t0 > 5:
            break
    print('=====Connected to uArm=====')


def send_command(arduino_data, command, time_step=0.1):
    # send command
    #    for i in range(len(command)):
    #        print('time stamp: ', time.clock())
    #        arduino_data.write((command[i] + '\r\n').encode())
    #        print('data sent: \n', command[i])
    #        time.sleep(time_step)
    for data in command:
#        print('time stamp: ', time.clock())
        arduino_data.write((data + '\r\n').encode())
#        print('data sent: \n', data)
        time.sleep(time_step)
    return None


def test_G0():
    print('-----Testing G0-----')
    # prepare command
    command = [
        'G0 X250 Y0 Z130 F10000',
        'G0 X240 Y10 Z140 F10000',
        'G0 X230 Y20 Z150 F10000',
    ]
    # send command
    send_command(command)
    return None


def test_G2202():
    print('-----Testing G2202-----')
    # prepare command
    command = [
        'G2202 N0 V90',
        'G2202 N0 V95',
        'G2202 N0 V100',
        'G2202 N0 V105',
        'G2202 N0 V110',
        'G2202 N0 V115',
        'G2202 N0 V120',
        'G2202 N0 V125',
    ]
    # send command
    send_command(arduino_data, command, time_step=0.5)
    return None


def test_M2231():
    print('-----Testing M2231-----')
    command = ['M2231 V1', 'M2231 V0']
    # send command
    send_command(arduino_data, command, time_step=5)
    return None


def test_home(arduino_data):
    print('-----Home Position-----')
    command = ['G2202 N0 V90', 'G2202 N1 V90', 'G2202 N2 V0', 'G2202 N3 V90']
    # send command
    send_command(arduino_data, command, time_step=0.5)
    return None


def test_line():
    print('-----Testing Line-----')
    command = [
        'G2202 N1 V90 \r\n G2202 N2 V0', 'G2202 N1 V95 \r\n G2202 N2 V5',
        'G2202 N1 V100 \r\n G2202 N2 V10', 'G2202 N1 V105 \r\n G2202 N2 V15',
        'G2202 N1 V110 \r\n G2202 N2 V20'
    ]
    #    command = ['G2202 N1 V90',
    #               'G2202 N2 V0',
    #               'G2202 N1 V85',
    #               'G2202 N2 V5',
    #               'G2202 N1 V80',
    #               'G2202 N2 V10',
    #               'G2202 N1 V75',
    #               'G2202 N2 V15',
    #               'G2202 N1 V70',
    #               #'G2202 N2 V70'
    #               ]
    # send command
    t1 = time.clock()
    send_command(arduino_data, command, time_step=0.5)
    print('time: ', time.clock() - t1)
    return None


if __name__ == '__main__':
    # set up serial port
    '''
    Please modifiy serial port setting based on your system
    '''
    arduino_data = serial.Serial('com4', baudrate=115200, timeout=3.0)

    print('=====Port Opened=====')

    # read first data
    connect_uArm(arduino_data)

    # test command
    test_home()
    #    test_G0()
    #    time.sleep(1)
    #    test_G2202()
    #    time.sleep(1)
    #    test_M2231()
    #    time.sleep(1)
    time.sleep(3)
    test_line()

    # close serial port
    arduino_data.close()
    print('=====Port Closed=====')