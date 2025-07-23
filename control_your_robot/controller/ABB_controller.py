import sys
sys.path.append("/home/aiseon/Project/abb_data_collect/control_your_robot/controller")

from controller.arm_controller import ArmController


from ABB.abb_base import Robot
import numpy as np
import time

class ABBController(ArmController):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.controller_type = "user_controller"
        self.controller = None
    
    def set_up(self, ip:str):
        abb_robot = Robot(ip)
        self.controller = abb_robot
        # self.controller.start()
        
    
    def reset(self, start_state):
        """Move robot to the specified start position"""
        print(f"\nMoving {self.name} arm to start position...")
    
    def move(self,move_data,is_delta=False):
        joint = move_data["qpos"]
        self.set_joint(joint)

    def get_state(self):
        state = {}
        # data = self.controller.get_data()
        state["joint"] = self.controller.get_joints()
        pose = self.controller.get_cartesian() #fix this name 
        state["qpos"] = pose[0]+pose[1]
        # state["gripper"] = self.controller.get_robotinfo() #todo: fix this
        state["gripper"] = [0]
        # state["gripper"] = self.controller.get_gripper_state()

        return state
    
    def set_position(self):
        pass
    
    def set_joint(self, joint):
        self.controller.set_joints(joint)
        
    
    def set_gripper(self, gripper):
        self.controller.set_dio(1,gripper)
    
    def __del__(self):
        try:
            if hasattr(self, "controller"):
                pass
        except:
            pass
        
def enable_fun(cr5):
    pass

if __name__=="__main__":
    controller = ABBController("test_abb")
    controller.set_up(ip="192.168.125.1")
    controller.set_joint(np.array([94.5046,14.5652,7.14539,-0.000668064,68.2835,-83.5819]))
    controller.set_gripper(1)
