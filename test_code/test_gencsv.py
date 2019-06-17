# -*- coding: utf-8 -*-
"""
Created on Tue May  7 20:04:58 2019

@author: xumw1
"""

import numpy as np

test_pos = np.zeros((200, 13))

# make sure X >= 130
for i, pos in enumerate(test_pos):
    pos[9:12] = np.array([130 + 0.5*i, 0.5*i, 100 - 0.2*i])
    
test_pos[120:160, -1] = np.ones((40))
np.savetxt('../python_SDK/test_traj.csv', test_pos, delimiter=",")    