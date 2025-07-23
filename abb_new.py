import socket
import json
import time
import inspect
from threading import Thread
from collections import deque
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Robot:
    def __init__(self,
                 ip='192.168.125.1',
                 port_motion=5000,
                 port_logger=5001):

        self.delay = .08

        self.connect_motion((ip, port_motion))
        # log_thread = Thread(target=self.get_net, args=((ip, port_logger))).start()

        self.set_units('millimeters', 'degrees')
        self.set_tool()
        self.set_workobject()
        self.set_speed()
        self.set_zone()

    def connect_motion(self, remote):
        log.info('Attempting to connect to robot motion server at %s', str(remote))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.5)
        self.sock.connect(remote)
        self.sock.settimeout(None)
        log.info('Connected to robot motion server at %s', str(remote))

    def connect_logger(self, remote, maxlen=None):
        self.pose = deque(maxlen=maxlen)
        self.joints = deque(maxlen=maxlen)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(remote)
        s.setblocking(1)
        try:
            while True:
                data = s.recv(4096).decode().split()  # Python 3: 需解码字节为字符串
                data = list(map(float, data))  # Python 3: map返回迭代器，需转为列表
                if int(data[1]) == 0:
                    self.pose.append([data[2:5], data[5:]])
                # elif int(data[1]) == 1: self.joints.append([a[2:5], a[5:]])
        finally:
            s.shutdown(socket.SHUT_RDWR)

    def set_units(self, linear, angular):
        units_l = {'millimeters': 1.0,
                   'meters': 1000.0,
                   'inches': 25.4}
        units_a = {'degrees': 1.0,
                   'radians': 57.2957795}
        self.scale_linear = units_l[linear]
        self.scale_angle = units_a[angular]

    def set_cartesian(self, pose):
        """
        Executes a move immediately from the current pose,
        to 'pose', with units of millimeters.
        """
        msg = "01 " + self.format_pose(pose)
        return self.send(msg)

    def set_joints(self, joints):
        """
        Executes a move immediately, from current joint angles,
        to 'joints', in degrees.
        """
        if len(joints) != 6:
            return False
        msg = "02 "
        for joint in joints:
            msg += f"{joint * self.scale_angle:+08.2f} "  # Python 3: 使用f-string格式化
        msg += "#"
        return self.send(msg)

    def get_cartesian(self):
        """
        Returns the current pose of the robot, in millimeters
        """
        msg = "03 #"
        data = self.send(msg).split()
        r = [float(s) for s in data]
        return [r[2:5], r[5:9]]

    def get_joints(self):
        """
        Returns the current angles of the robots joints, in degrees.
        """
        msg = "04 #"
        data = self.send(msg).split()
        return [float(s) / self.scale_angle for s in data[2:8]]

    def get_external_axis(self):
        """
        If you have an external axis connected to your robot controller
        (such as a FlexLifter 600, google it), this returns the joint angles
        """
        msg = "05 #"
        data = self.send(msg).split()
        return [float(s) for s in data[2:8]]

    def get_robotinfo(self):
        """
        Returns a robot- unique string, with things such as the
        robot's model number.
        Example output from and IRB 2400:
        ['24-53243', 'ROBOTWARE_5.12.1021.01', '2400/16 Type B']
        """
        msg = "98 #"
        data = str(self.send(msg))[5:].split('*')
        log.debug('get_robotinfo result: %s', str(data))
        return data

    def set_tool(self, tool=[[0, 0, 0], [1, 0, 0, 0]]):
        """
        Sets the tool centerpoint (TCP) of the robot.
        When you command a cartesian move,
        it aligns the TCP frame with the requested frame.

        Offsets are from tool0, which is defined at the intersection of the
        tool flange center axis and the flange face.
        """
        msg = "06 " + self.format_pose(tool)
        self.send(msg)
        self.tool = tool

    def load_json_tool(self, file_obj):
        if isinstance(file_obj, str):  # Python 3: 使用isinstance代替__class__.__name__判断
            with open(file_obj, 'rb') as f:  # Python 3: 推荐使用with语句管理文件
                tool = check_coordinates(json.load(f))
        else:
            tool = check_coordinates(json.load(file_obj))
        self.set_tool(tool)

    def set_workobject(self, work_obj=[[0, 0, 0], [1, 0, 0, 0]]):
        """
        The workobject is a local coordinate frame you can define on the robot,
        then subsequent cartesian moves will be in this coordinate frame.
        """
        msg = "07 " + self.format_pose(work_obj)
        self.send(msg)

    def set_speed(self, speed=[100, 50, 50, 50]):
        """
        speed: [robot TCP linear speed (mm/s), TCP orientation speed (deg/s),
                external axis linear, external axis orientation]
        """

        if len(speed) != 4:
            return False
        msg = "08 "
        msg += f"{speed[0]:+08.1f} "  # Python 3: f-string格式化
        msg += f"{speed[1]:+08.2f} "
        msg += f"{speed[2]:+08.1f} "
        msg += f"{speed[3]:+08.2f} #"
        self.send(msg)

    def set_zone(self,
                 zone_key='z1',
                 point_motion=False,
                 manual_zone=[]):
        zone_dict = {'z0': [.3, .3, .03],
                     'z1': [1, 1, .1],
                     'z5': [5, 8, .8],
                     'z10': [10, 15, 1.5],
                     'z15': [15, 23, 2.3],
                     'z20': [20, 30, 3],
                     'z30': [30, 45, 4.5],
                     'z50': [50, 75, 7.5],
                     'z100': [100, 150, 15],
                     'z200': [200, 300, 30]}
        """
        Sets the motion zone of the robot. This can also be thought of as
        the flyby zone, AKA if the robot is going from point A -> B -> C,
        how close do we have to pass by B to get to C

        zone_key: uses values from RAPID handbook (stored here in zone_dict)
        with keys 'z*', you should probably use these

        point_motion: go to point exactly, and stop briefly before moving on

        manual_zone = [pzone_tcp, pzone_ori, zone_ori]
        pzone_tcp: mm, radius from goal where robot tool centerpoint
                   is not rigidly constrained
        pzone_ori: mm, radius from goal where robot tool orientation
                   is not rigidly constrained
        zone_ori: degrees, zone size for the tool reorientation
        """

        if point_motion:
            zone = [0, 0, 0]
        elif len(manual_zone) == 3:
            zone = manual_zone
        elif zone_key in zone_dict:  # Python 3: dict.keys()返回视图对象，可直接用于in判断
            zone = zone_dict[zone_key]
        else:
            return False

        msg = "09 "
        msg += str(int(point_motion)) + " "
        msg += f"{zone[0]:+08.4f} "
        msg += f"{zone[1]:+08.4f} "
        msg += f"{zone[2]:+08.4f} #"
        self.send(msg)

    def buffer_add(self, pose):
        """
        Appends single pose to the remote buffer
        Move will execute at current speed (which you can change between buffer_add calls)
        """
        msg = "30 " + self.format_pose(pose)
        self.send(msg)

    def buffer_set(self, pose_list):
        """
        Adds every pose in pose_list to the remote buffer
        """
        self.clear_buffer()
        for pose in pose_list:
            self.buffer_add(pose)
        if self.buffer_len() == len(pose_list):
            log.debug('Successfully added %i poses to remote buffer',
                      len(pose_list))
            return True
        else:
            log.warning('Failed to add poses to remote buffer!')  # Python 3: warn改为warning
            self.clear_buffer()
            return False

    def clear_buffer(self):
        msg = "31 #"
        data = self.send(msg)
        if self.buffer_len() != 0:
            log.warning('clear_buffer failed! buffer_len: %i', self.buffer_len())  # Python 3: warn改为warning
            raise NameError('clear_buffer failed!')
        return data

    def buffer_len(self):
        """
        Returns the length (number of poses stored) of the remote buffer
        """
        msg = "32 #"
        data = self.send(msg).split()
        return int(float(data[2]))

    def set_external_axis(self, axis_values=[-550, 0, 0, 0, 0, 0]):  # Python 3: 修复参数名拼写错误axis_unscaled→axis_values
        if len(axis_values) != 6:
            return False
        msg = "34 "
        for axis in axis_values:
            msg += f"{axis:+08.2f} "
        msg += "#"
        return self.send(msg)

    def move_circular(self, pose_onarc, pose_end):
        """
        Executes a movement in a circular path from current position,
        through pose_onarc, to pose_end
        """
        msg_0 = "35 " + self.format_pose(pose_onarc)
        msg_1 = "36 " + self.format_pose(pose_end)

        data = self.send(msg_0).split()
        if data[1] != '1':
            log.warning('move_circular incorrect response, bailing!')  # Python 3: warn改为warning
            return False
        return self.send(msg_1)

    def set_dio(self, num, value, id=0):
        """
        num = 1, doGripperOpen; num=2, doGripperClose;
        value=0, Reset; value=1,Set;
        """
        msg = f'97 {int(num)} {int(bool(value))} #'  # Python 3: f-string格式化
        return self.send(msg)

    def send(self, message, wait_for_response=True):
        """
        Send a formatted message to the robot socket.
        if wait_for_response, we wait for the response and return it
        """
        caller = inspect.stack()[1][3]
        log.debug('%-14s sending: %s', caller, message)
        self.sock.send(message.encode())  # Python 3: 发送字节需编码字符串
        time.sleep(self.delay)
        if not wait_for_response:
            return
        data = self.sock.recv(4096).decode()  # Python 3: 接收字节需解码为字符串
        log.debug('%-14s received: %s', caller, data)  # Python 3: 修复拼写错误recieved→received
        return data

    def format_pose(self, pose):
        pose = check_coordinates(pose)
        msg = ''
        for cartesian in pose[0]:
            msg += f"{cartesian * self.scale_linear:+08.1f} "  # Python 3: f-string格式化
        for quaternion in pose[1]:
            msg += f"{quaternion:+08.5f} "  # Python 3: f-string格式化
        msg += "#"
        return msg

    def close(self):
        self.send("99 #", False)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def check_coordinates(coordinates):
    if (len(coordinates) == 2 and
            len(coordinates[0]) == 3 and
            len(coordinates[1]) == 4):
        return coordinates
    elif len(coordinates) == 7:
        return [coordinates[0:3], coordinates[3:7]]
    log.warning('Received malformed coordinate: %s', str(coordinates))  # Python 3: warn改为warning，修复拼写错误Recieved→Received
    raise NameError('Malformed coordinate!')


if __name__ == '__main__':
    import json

    ip = "192.168.125.1"
    abb = Robot(ip)
    abb.set_dio(1, 1) #1or0
    abb.set_speed([250, 500, 5000, 1000])

    joint_list = [
        [98.3218, 26.2561, -12.6149, 0.000100979, 76.3659, -79.7669],
        [94.5038, 34.4333, 22.9666, -0.000668064, 32.61, -83.5843],
        [94.5046, 57.7038, 17.2206, -0.00121738, 15.066, -83.5811],
        [94.5046, 33.4183, 22.9163, -0.000668064, 33.6582, -83.5813],
        [94.5046, 14.5652, 7.14539, -0.000668064, 68.2835, -83.5819],
        [4.41758, 14.5998, 7.1455, -0.000668064, 68.2835, -83.5819],
        [3.86994, 38.6464, 7.83732, -0.000668064, 43.5466, -84.1318],
        [3.87003, 54.8324, 6.42372, -0.000668064, 28.7793, -84.1314]
    ]

    for joint in joint_list:
        abb.set_joints(joint)
    
    abb.set_dio(1, 0)