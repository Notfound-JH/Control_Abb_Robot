import sys
sys.path.append("./")

from controller.arm_controller import ArmController


sys.path.append("/home/thu/arlen/TCP-IP-Python-V4/control_your_robot/controller")
from CR5.DobotDemo import DobotDemo
import numpy as np
import time

class CR5Controller(ArmController):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.controller_type = "user_controller"
        self.controller = None
    
    def set_up(self, ip:str):
        dobot = DobotDemo(ip)
        self.controller = dobot
        self.controller.start()
        
    
    def reset(self, start_state):
        """Move robot to the specified start position"""
        print(f"\nMoving {self.name} arm to start position...")
    
    def move(self,move_data,is_delta=False):
        joint = move_data["qpos"]
        self.set_joint(joint)

    def get_state(self):
        state = {}
        data = self.controller.get_data()
        state["joint"] = data[0]
        state["qpos"] = data[1]
        state["gripper"] = [0]
        return state
    
    def set_position(self):
        pass
    
    def set_joint(self, joint):
        self.controller.RunPoint(joint)
        
    
    def set_gripper(self, gripper):
        pass
    
    def __del__(self):
        try:
            if hasattr(self, "controller"):
                pass
        except:
            pass
        
def enable_fun(cr5):
    pass

if __name__=="__main__":
    controller = CR5Controller("test_cr5")
    controller.set_up(ip="192.168.1.54")
    controller.set_joint(np.array([136.3759,-243.4321,432.3956,177.7879,-1.8540,147.5821]))
