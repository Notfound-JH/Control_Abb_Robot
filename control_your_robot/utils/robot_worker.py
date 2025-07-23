import sys
sys.path.append("./")
from controller import *
import time
from typing import *

from multiprocessing import Event, Semaphore

from utils.data_handler import debug_print

def RobotWorker(robot_class, start_episode,
                time_lock: Semaphore, start_event: Event, finish_event: Event, process_name: str):
    """
    Worker process function:
    - Uses a Semaphore to control time synchronization
    - Uses an Event to signal process termination
    """
    robot = robot_class(start_episode=start_episode)
    robot.set_up()
    while not start_event.is_set():
        debug_print(process_name ,"Press Enter to start...","INFO")
        time.sleep(1)
    
    debug_print(process_name, "Get start Event, start collecting...","INFO")
    debug_print(process_name, "To finish this episode, please press Enter. ","INFO")
    try:
        while not finish_event.is_set():
            time_lock.acquire()  
            if finish_event.is_set():
                break  # Prevent exiting immediately after acquire before processing data

            debug_print(process_name, "Time lock acquired. Processing data...")

            try:
                data = robot.get()
                robot.collect(data)
            except Exception as e:
                debug_print(process_name, f"Error: {e}", "ERROR")

            debug_print(process_name, "Data processed. Waiting for next time slot.")

        debug_print(process_name, "Finish event triggered. Finalizing...","INFO")
        robot.finish()
        debug_print(process_name, "Writing success!","DEBUG")
        
    except KeyboardInterrupt:
        debug_print(process_name, "Worker terminated by user.")
    finally:
        debug_print(process_name, "Worker exiting.")
