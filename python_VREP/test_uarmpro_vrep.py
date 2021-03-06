# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 11:05:31 2019

@author: xumw1
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:08:04 2019

@author: xumw1
"""

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import vrep
import sys
import numpy as np
import math
import time
import pprint

PI = math.pi

class Uarm():
    def __init__(self, clientID):
        '''
        get handles
        set initial state
        '''
        self.clientID = clientID
        self.jointHandles = [-1,-1,-1,-1]
        #self.collisionHandles = [-1,-1]
        #self.state = [False,False]
        
        jointInd = [0,1,2,3]
        jointName = ['uarm_motor' + str(i+1) for i in range(4)]
        self.jointDict = dict(zip(jointInd, jointName))
        
        # joint handle
        for i in range(4):
            res, self.jointHandles[i] = vrep.simxGetObjectHandle(clientID, self.jointDict[i] ,vrep.simx_opmode_blocking)
            if res!=0:
                print('Failed to find: {}'.format(self.jointDict[i]))
        
        # collision handle
#        for i in range(2):
#            self.returnCode,self.collisionHandles[i] = vrep.simxGetCollisionHandle(clientID,'Collision'+str(i+1),vrep.simx_opmode_blocking)
        print('handles get')
        print(self.jointHandles)
        
        # initialize
        for i in range(4):
            vrep.simxGetJointPosition(self.clientID, self.jointHandles[i],  vrep.simx_opmode_streaming)
        print('initialzied')
        
    
    def get_joint_position(self, ignoreError=False):
        jointPos = np.zeros(4)
        for i in range(4):
            res, jointPos[i] = vrep.simxGetJointPosition(self.clientID, self.jointHandles[i],  vrep.simx_opmode_buffer)
            if res!=0 and not ignoreError:
                print('Failed to get joint position: {}'.format(self.jointDict[i]))
                
        return jointPos
    
    def set_joint_position(self, target, ignoreError=False):
        '''
        set joint position to target position
        '''
        vrep.simxPauseCommunication(clientID,True)
        for i in range(4):
            res = vrep.simxSetJointTargetPosition(clientID,self.jointHandles[i],target[i],vrep.simx_opmode_oneshot)
            if res!=0 and not ignoreError:
                print('Failed to set joint position: {}'.format(self.jointDict[i]))
                print(res)
        vrep.simxPauseCommunication(clientID,False)
        
        return None
    
    
        
if __name__ == '__main__':
    vrep.simxFinish(-1) # just in case, close all opened connections
    clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
    
    if clientID !=- 1:
        print ('Connected to remote API server')
        # start simulation
        vrep.simxSynchronous(clientID,True);
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
        print('In synchronous mode')
    else:
        print ('Failed connecting to remote API server')
        sys.exit('Could not connect')
      
  
    N = 30
    targetPos = np.zeros((N,4))
    
    for i in range(N):
        targetPos[i,0] = 90 + i * PI / 180
        targetPos[i,1] = 90 - i * PI / 180
        targetPos[i,2] = i * PI / 180
#        targetPos[i,2] = -i * PI / 180
        
    pprint.pprint(targetPos)
    
    uarm_1 = Uarm(clientID)
    
    t1 = time.clock()
    for i in range(N):
        uarm_1.set_joint_position(targetPos[i,:])
        time.sleep(0.1)
        
    print('run time: ', time.clock() - t1)
    
#    targetPos = np.array([0, 0, 0, 0])
#    uarm_1.set_joint_position(targetPos)
#    time.sleep(1)
#    vrep.simxSynchronousTrigger(clientID)
#    vrep.simxGetPingTime(clientID)
#    jointPos = uarm_1.get_joint_position()
#    print(jointPos)
#    
#    time.sleep(1)
#    '''
#    Set position and check collision
#    '''

#    targetPos = np.array([0,0,0,0])
#    uarm_1.set_joint_position(targetPos)

#        
#    # end simulation
#    time.sleep(1)
#    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)