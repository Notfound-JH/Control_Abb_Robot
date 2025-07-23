import pyrealsense2 as rs
ctx = rs.context()
devs = ctx.query_devices()
for dev in devs:
    serial_number = dev.get_info(rs.camera_info.serial_number)
    print(serial_number)