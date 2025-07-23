import sys
sys.path.append("./")

import numpy as np
import time

from controller.ABB_controller import ABBController
from utils.data_handler import debug_print
from data.collect_any import CollectAny
from sensor.Kinect_sensor import KinectSensor
condition ={
    "robot":"abb_single",
    "save_path":"./datasets/",
    "task_name": "test", 
    "save_format": "hdf5", 
    "save_interval": 10, 
}

class Abb:
    def __init__(self, start_episode=0):
        self.condition = condition
        self.arm_controllers = {
            "left_arm": ABBController("left")
        }
        self.image_sensors ={
            "cam_side":KinectSensor("cam_side")
        }
        self.collection = CollectAny(condition, start_episode=start_episode)

    def set_collect_type(self,ARM_INFO_NAME,IMG_INFO_NAME):
        for controller in self.arm_controllers.values():
            controller.set_collect_info(ARM_INFO_NAME)

    def set_up(self,ip="192.168.125.1"):
        self.arm_controllers["left_arm"].set_up(ip)
        self.image_sensors["cam_side"].set_up(is_depth=False)
        self.set_collect_type(["joint","qpos","gripper"],["color"])
        print("set up success!")
    def is_start(self):
        return True
    # ============== arm info ==============
    def get(self):
        controller_data = {}
        if self.arm_controllers is not None:    
            for controller_name, controller in self.arm_controllers.items():
                controller_data[controller_name] = controller.get()
        # return [controller_data]
        sensor_data = {}
        if self.image_sensors is not None:  
            for sensor_name, sensor in self.image_sensors.items():
                sensor_data[sensor_name] = sensor.get()
        return [controller_data, sensor_data]


    def collect(self, data):
        self.collection.collect(data[0],data[1])

    def finish(self):
        self.collection.write()
    # ============== arm control ==============
    def move(self, move_data):  
        self.arm_controllers["left_arm"].move(move_data["left_arm"],is_delta=False)