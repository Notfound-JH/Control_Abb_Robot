from sensor.vision_sensor import VisionSensor
import cv2
import pykinect_azure as pykinect
class KinectSensor(VisionSensor):
    def __init__ (self, name):
        super().__init__()
        self.name = name
    
    def set_up(self,is_depth=None):
        pykinect.initialize_libraries()
        device_config = pykinect.default_configuration
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
        self.device = pykinect.start_device(config=device_config)
        self.set_collect_info(["color"])
        # cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)


    def get_image(self):
        capture = self.device.update()
        ret = None
        while not ret:
            ret, color_image = capture.get_color_image()

        return color_image

    def __del__(self):
        pass

if __name__ == "__main__":
    cam = KinectSensor("test")
    cam.set_up()
    image = cam.get_image()