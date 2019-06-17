# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:11:03 2019

@author: xumw1
"""


import serial
import time
import threading
import numpy as np
from test_Gcode_generator import generate_Gcode

 
class UArm_serial_port:
    message='' 
    def __init__(self,port,buand):
        #super(SerialPort, self).__init__()
        self.port=serial.Serial(port,buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()
            print('port open')
            time.sleep(1)
    def port_open(self):
        if not self.port.isOpen():
            self.port.open()
    def port_close(self):
        self.port.close()
        
    def send_data(self, data):
        n=self.port.write((data+'\r\n').encode())
        return n
        
#    def send_command(self, command, time_step=0.1):
#        for data in command:
#            
#            #data = input("请输入要发送的数据（非中文）并同时接收数据: ")
#            n=self.port.write((data+'\r\n').encode())
#            time.sleep(time_step)
#        return n
        
    def read_data(self):
        while True:
            self.message=self.port.readline()
            print(self.message)
            
    def test_home(self):
        print('-----Home Position-----')
        command = ['G2202 N0 V90', 'G2202 N1 V90', 'G2202 N2 V0', 'G2202 N3 V90']
        # send command
        self.send_data(command[0])
 
serialPort="COM4"   #
baudRate=115200       #
 
if __name__=='__main__':
    
    mSerial=UArm_serial_port(serialPort,baudRate)
    t1=threading.Thread(target=mSerial.read_data) 
 
    t1.start()
    
    
    T = 5
    dt = 1 # best we can get: 0.1 stable in theory: 0.28 stable in practice: 0.8
    # one command for 4 motors: about 20 * 4 = 80 bytes
    # baudRate: 1152 bytes/s
    # about 14.4 command/s
    # safe dt: 0.28, for 4 commands
    N = int(T / dt)

    '''generate configs'''
    joint_angles = np.zeros((N, 5))
    for i in range(N):
        joint_angles[i, :] = np.array([90, 90 - 40/T * dt * i, 40/T * dt * i, 90, 0])

    G_code = generate_Gcode(joint_angles)
    '''generate configs'''
    
    mSerial.test_home()     # back to home pos
    time.sleep(5)
    
    for data in G_code:
        mSerial.send_data(data)
        time.sleep(dt/4)
        
#    mSerial.send_command(command=G_code)
    mSerial.port_close()