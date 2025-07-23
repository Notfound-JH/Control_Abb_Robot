import sys
sys.path.append("./")

import select

from my_robot.abb_base import Abb

import time

from utils.data_handler import is_enter_pressed,debug_print

if __name__ == "__main__":
    import os
    os.environ["INFO_LEVEL"] = "DEBUG" # DEBUG , INFO, ERROR

    robot = Abb()
    robot.set_up(ip="192.168.125.1")
    
    # joint_list = [
    #     [98.3218, 26.2561, -12.6149, 0.000100979, 76.3659, -79.7669],
    #     [94.5038, 34.4333, 22.9666, -0.000668064, 32.61, -83.5843],
    #     [94.5046, 57.7038, 17.2206, -0.00121738, 15.066, -83.5811],
    #     [94.5046, 33.4183, 22.9163, -0.000668064, 33.6582, -83.5813],
    #     [94.5046, 14.5652, 7.14539, -0.000668064, 68.2835, -83.5819],
    #     [4.41758, 14.5998, 7.1455, -0.000668064, 68.2835, -83.5819],
    #     [3.86994, 38.6464, 7.83732, -0.000668064, 43.5466, -84.1318],
    #     [3.87003, 54.8324, 6.42372, -0.000668064, 28.7793, -84.1314]
    # ]
    # for joint in joint_list:
    #     robot.set_joints(joint)

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
