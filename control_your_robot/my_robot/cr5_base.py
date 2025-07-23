import sys
sys.path.append("./")

import numpy as np
import time

from controller.Cr5_controller import CR5Controller
from utils.data_handler import debug_print
from data.collect_any import CollectAny
# from sensor.Realsense_sensor import RealsenseSensor
from sensor.Kinect_sensor import KinectSensor
condition = {
    "robot":"cr5_single",
    "save_path": "./datasets/", 
    "task_name": "test", 
    "save_format": "hdf5", 
    "save_interval": 10, 
}


class Cr5:
    def __init__ (self, start_episode=0):
        self.condition = condition
        self.arm_controllers = {
            "left_arm": CR5Controller("left_arm"),
        }
        self.image_sensors = {
            "cam_head": KinectSensor("cam_head"),
            # "cam_wrist": RealsenseSensor("cam_wrist"),
        }
        self.collection = CollectAny(condition, start_episode=start_episode)

    def set_collect_type(self,ARM_INFO_NAME,IMG_INFO_NAME):
        for controller in self.arm_controllers.values():
            controller.set_collect_info(ARM_INFO_NAME)
        # for sensor in self.image_sensors.values():
        #     sensor.set_collect_info(IMG_INFO_NAME)

    def set_up(self,ip):
        self.arm_controllers["left_arm"].set_up(ip)
        self.image_sensors["cam_head"].set_up(is_depth=False)
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
    
if __name__ == "__main__":
    import os
    os.environ["INFO_LEVEL"] = "DEBUG" # DEBUG , INFO, ERROR
    robot = Cr5()
    robot.set_up(ip="192.168.1.54")
    # while True:
    # robot.arm_controllers["left_arm"].set_joint([146.3759,-283.4321,332.3956,177.7879,-1.8540,147.5821])
    # robot.arm_controllers["left_arm"].set_joint([136.3759,-243.4321,432.3956,177.7879,-1.8540,147.5821])
    
    # collection test
    # data_list = []
    # for i in range(100):
    #     print(i)
    #     data = robot.get()
    #     robot.collect(data)
    #     time.sleep(0.1)
    # robot.finish()

    joint_1 = [136.3759,-243.4321,432.3956,177.7879,-1.8540,147.5821]
    joint_2 = [146.3759,-283.4321,332.3956,177.7879,-1.8540,147.5821]
    move_data_1 = {
        "left_arm":{
        "qpos":joint_1,
        # "gripper":0.2,
        },
    }

    move_data_2 = {
        "left_arm":{
        "qpos":joint_2,
        # "gripper":0.2,
        },
    }
    while True:
        robot.move(move_data_1)
        robot.move(move_data_2)
