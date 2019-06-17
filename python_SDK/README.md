# Control UArm via Python SDK

## Get Started
Before running the codes, please download and install uArm-Python-SDK following the instruction:
https://github.com/uArm-Developer/uArm-Python-SDK

Please install modern robotics python library via pip:
```
pip install modern-robotics
```

## UArm_SDK.py
Control uArm via python SDK library by sending joint angles. Jittering problem since it has to send each joint angle sequentially.

## UArm_SDK_FK.py
Calculate forward kinematics in python and control uArm via python SDK by sending end-effector position and orientation. Jittering is reduced.
