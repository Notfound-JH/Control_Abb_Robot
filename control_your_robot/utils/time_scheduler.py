import time
import multiprocessing as mp
from multiprocessing import Array, Process, Semaphore, Lock
from typing import List
import numpy as np

DEBUG = False
Release = True

from utils.data_handler import debug_print

def worker(process_id: int, process_name: str, time_semaphore: Semaphore, result_array: Array, result_lock: Lock):
    while True:
        # Block until the scheduler issues an "execution token"
        time_semaphore.acquire()  
        debug_print(process_name, "received time slot", "DEBUG")

        # Simulate task processing + data writing (with locking)
        result = np.random.randn(5,5).flatten()
        with result_lock:
            result_array[process_id*25:(process_id+1)*25] = result
        time.sleep(0.01) 

class TimeScheduler:
    def __init__(self, time_semaphores: List[Semaphore], time_interval=10):
        self.time_interval = time_interval
        self.time_semaphores = time_semaphores
        self.process_name = "time_scheduler"

    def time_worker(self):
        while True:
            for sem in self.time_semaphores:
                # Issue "time slice token"
                sem.release()  
                debug_print(self.process_name, "released time slot to one worker", "DEBUG")
            time.sleep(1 / self.time_interval)

    def start(self):
        self.time_locker = Process(target=self.time_worker)
        self.time_locker.start()

    def stop(self):
        for sem in self.time_semaphores:
                sem.release()  # 防止卡在获取锁
        self.time_locker.terminate()
        self.time_locker.join()
        self.time_locker.close()
        self.time_locker = None

if __name__ == "__main__":
    processes = []
    process_num = 4
    result_array = Array('d', process_num * 25)
    time_semaphores = [Semaphore(0) for _ in range(process_num)]
    result_lock = Lock()

    # start workers
    for i in range(process_num):
        process = Process(target=worker, args=(i, f"process_{i}", time_semaphores[i], result_array, result_lock))
        process.start()
        processes.append(process)

    # start time scheduler
    time_scheduler = TimeScheduler(time_semaphores, time_interval=10)
    time_scheduler.start()

    # (optional)
    try:
        time.sleep(5)
        print("Sample result snapshot:", result_array[:])
    except KeyboardInterrupt:
        print("Main process interrupted.")
    finally:
        time_scheduler.stop()
        for p in processes:
            p.terminate()
            p.join()
