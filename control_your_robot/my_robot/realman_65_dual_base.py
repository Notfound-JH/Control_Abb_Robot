import sys
sys.path.append("./")
from controller.Realman_controller import RealmanController
from sensor.Realsense_sensor import RealsenseSensor
from data.collect_any import CollectAny
from Robotic_Arm.rm_robot_interface import rm_thread_mode_e

import numpy as np

# 组装你的控制器
CAMERA_SERIALS = {
    'head': '111',  # Replace with actual serial number
    'left_wrist': '111',   # Replace with actual serial number
    'right_wrist': '111',   # Replace with actual serial number
}

# Define start position (in degrees)
START_POSITION_ANGLE_LEFT_ARM = [
    65,   # Joint 1
    38,    # Joint 2
    -66,  # Joint 3
    12,   # Joint 4
    6,  # Joint 5
    119,    # Joint 6
    66    # Joint 7
]

# Define start position (in degrees)
START_POSITION_ANGLE_RIGHT_ARM = [
    -59,   # Joint 1
    38,    # Joint 2
    -123,  # Joint 3
    -9,   # Joint 4
    -10,  # Joint 5
    -120,    # Joint 6
    32    # Joint 7
]

# 记录统一的数据操作信息, 相关配置信息由CollectAny补充并保存
condition = {
    "save_path": "./save/",
    "task_name": "test", 
    "save_interval": 10,
}

class MyRobot:
    def __init__(self, start_episode=0):
        self.arm_controllers = {
            "left_arm": RealmanController("left_arm"),
            "right_arm": RealmanController("right_arm"),
        }
        self.image_sensors = {
            "cam_head": RealsenseSensor("cam_head"),
            "cam_left_wrist": RealsenseSensor("cam_left_wrist"),
            "cam_right_wrist": RealsenseSensor("cam_right_wrist"),
        }
        self.condition = condition
        self.collection = CollectAny(condition, start_episode=start_episode)

    def set_up(self):
        self.arm_controllers["left_arm"].set_up("192.168.80.18", rm_thread_mode_e.RM_TRIPLE_MODE_E)
        self.arm_controllers["right_arm"].set_up("192.168.80.19", rm_thread_mode_e.RM_TRIPLE_MODE_E)
        self.image_sensors["cam_head"].set_up(CAMERA_SERIALS['head'], is_depth=False)
        self.image_sensors["cam_left_wrist"].set_up(CAMERA_SERIALS['left_wrist'], is_depth=False)
        self.image_sensors["cam_right_wrist"].set_up(CAMERA_SERIALS['right_wrist'], is_depth=False)
        self.set_collect_type(["joint","qpos","gripper"],["color"])
        print("set up success!")
        
    def get(self):
        controller_data = {}
        if self.arm_controllers is not None:    
            for controller_name, controller in self.arm_controllers.items():
                controller_data[controller_name] = controller.get()
        sensor_data = {}
        if self.image_sensors is not None:  
            for sensor_name, sensor in self.image_sensors.items():
                sensor_data[sensor_name] = sensor.get()
        return [controller_data, sensor_data]
    
    def move(self, move_data):
        self.arm_controllers["left_arm"].move(move_data["left_arm"],is_delta=False)
        self.arm_controllers["right_arm"].move(move_data["right_arm"],is_delta=False)
    
    def reset(self):
        self.arm_controllers["left_arm"].reset(START_POSITION_ANGLE_LEFT_ARM)
        self.arm_controllers["right_arm"].reset(START_POSITION_ANGLE_RIGHT_ARM)

    def finish(self):
        self.collection.write()
    
    def set_collect_type(self,ARM_INFO_NAME,IMG_INFO_NAME):
        for controller in self.arm_controllers.values():
            controller.set_collect_info(ARM_INFO_NAME)
        for sensor in self.image_sensors.values():
            sensor.set_collect_info(IMG_INFO_NAME)

    def is_start(self):
        if max(abs(self.arm_controllers["left_arm"].get_state()["joint"] - START_POSITION_ANGLE_LEFT_ARM), abs(self.arm_controllers["right_arm"].get_state()["joint"] - START_POSITION_ANGLE_RIGHT_ARM)) > 0.01:
            return True
        else:
            return False
    
    def collect(self, data):
        self.collection.collect(data[0], data[1])
    
    def set_action(self, action):
        self.arm_controllers["left_arm"].set_action(action)
        self.arm_controllers["right_arm"].set_action(action)

if __name__ == "__main__":
    robot = MyRobot()

    robot.reset()
    