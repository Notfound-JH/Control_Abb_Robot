import sys
sys.path.append("./")

#import select
import socket
import keyboard
from my_robot.abb_base import Abb

# from my_robot.abb_base import Abb

import time
# from utils.data_handler import is_enter_pressed,debug_print

if __name__ == "__main__":
    import os
    os.environ["INFO_LEVEL"] = "DEBUG" # DEBUG , INFO, ERROR
    # robot = Abb()
    # image_sensors = robot.image_sensors
    
    # for sensor_name, sensor in image_sensors.items():
    #         cold_start_sensor = sensor.get()
    # print(cold_start_sensor)
    
    sensor_data = {}

    data = {}
    # robot = Abb()
    # robot.set_up(ip="192.168.125.1")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.125.10', 3000)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"服务器正在监听 {server_address}...")
    # while True:
    # 等待客户端连接
    print("等待客户端连接...")
    client_socket, client_address = server_socket.accept()
    # break 
    client_socket.setblocking(0)  # 设置客户端为非阻塞

    i = 0
    while True:

        # if i>3000:
        #     break

        # i += 1 
        time.sleep(0.01)
        # try:e
        print(f"客户端 {client_address} 已连接")
        timesteps = time.time()
        # 接收客户端消息
        data = client_socket.recv(4096)
        message = data.decode('utf-8')
        # joint_data = message.split("joint")[1].split("ee")[0].split(" ")
        # ee_data = message.split("joint")[1].split("ee")[1].split(" ")
        print(f"{timesteps} steps 收到消息: {message}")
        # data['joints_angle'] = joint_data
        # data['ee_pos_and_quat'] = ee_data
        # 发送响应
        response = f"服务器已收到: {message}"

        # import pprint
        # pprint.pprint(data)

        # if response:
        #     for sensor_name, sensor in image_sensors.items():
        #         sensor_data[sensor_name] = sensor.get()
    
        client_socket.sendall(response.encode('utf-8'))
        recv_buffer_size = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print(f"接收缓冲区总大小: {recv_buffer_size} 字节")

        # 获取发送缓冲区总大小
        send_buffer_size = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        print(f"发送缓冲区总大小: {send_buffer_size} 字节")
        # if keyboard.is_pressed('e'):
        #     print("\n检测到 'e' 键，退出程序")
        #     break
    
    client_socket.close()
        # finally:
            # 关闭客户端连接
            # client_socket.close()

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

    # num_episode = 10
    # robot.condition["task_name"] = "my_test"

    # for _ in range(num_episode):
    #     # robot.reset()
    #     debug_print("main", "Press Enter to start...", "INFO")
    #     while not robot.is_start() or not is_enter_pressed():
    #         time.sleep(1/robot.condition["save_interval"])
        
    #     debug_print("main", "Press Enter to finish...", "INFO")

    #     while True:
    #         data = robot.get()
    #         robot.collect(data)
            
    #         if is_enter_pressed():
    #             robot.finish()
    #             break
                
    #         time.sleep(1/robot.condition["save_interval"])
