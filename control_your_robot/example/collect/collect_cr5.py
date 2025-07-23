import sys
sys.path.append("./")

import select

# from my_robot.test_robot import TestRobot
from my_robot.cr5_base import Cr5

import time

from utils.data_handler import is_enter_pressed,debug_print


if __name__ == "__main__":
    import os
    os.environ["INFO_LEVEL"] = "DEBUG" # DEBUG , INFO, ERROR

    robot = Cr5()
    robot.set_up(ip="192.168.1.54")
    num_episode = 10
    robot.condition["task_name"] = "my_test"

    for _ in range(num_episode):
        # robot.reset()
        debug_print("main", "Press Enter to start...", "INFO")
        while not robot.is_start() or not is_enter_pressed():
            time.sleep(1/robot.condition["save_interval"])
        
        debug_print("main", "Press Enter to finish...", "INFO")

        while True:
            data = robot.get()
            robot.collect(data)
            
            if is_enter_pressed():
                robot.finish()
                break
                
            time.sleep(1/robot.condition["save_interval"])