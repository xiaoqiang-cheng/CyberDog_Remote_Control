from cyber_camera_base import ImageGrabberBase
from cyber_cv_detection_base import CVZoneModel
from cyber_control_base import ControlBase, HandsClassfier

from threading import Thread

import time
from datetime import datetime
from datetime import timedelta


def timeguard(time_interval, default=None):
    def decorator(function):
        # For first time always run the function
        function.__last_run = datetime.min
        def guard(*args, **kwargs):
            now = datetime.now()
            if now - function.__last_run >= time_interval:
                function.__last_run = now
                return function(*args, **kwargs)
            elif default is not None:
                return default(*args, **kwargs)
        return guard
    return decorator

class CyberCvControl(object):
    def __init__(self):
        self.image_grabber = ImageGrabberBase()
        self.image_grabber.cv_connect(self.image_callback)
        self.hands_detector = CVZoneModel()
        self.classfier = HandsClassfier()
        self.control_base = ControlBase(dog_ip = "192.168.1.4")
        self.control_thread = None
        self.cls_result = 0

        ret = False
        while not ret:
            ret = control_base.connect_cyber_dog()
            time.sleep(1)
            print("等待连接cyber dog")
            print("CyberDog 连接成功！")

    def image_callback(self, image):
        hands_info, image = self.hands_detector.inference(image)
        self.cls_result = self.classfier(hands_info)
        if self.cls_result  == 0:
            pass
        else:
            if self.control_thread == None or self.control_thread._is_stopped == True:
                self.control_thread = Thread(target=self.control_fun, args=(self.cls_result, self.control_base))
                self.control_thread.start()

    # @timeguard(timedelta(seconds=5), None)
    def control_fun(self,cls, control_base):
        if cls == 0:
            pass
        elif cls == 1:
            control_base.switch_move_mode()
        elif cls == 2:
            control_base.HiFive()
        elif cls == 3:
            control_base.switch_sit_mode()
        time.sleep(5)
        self.control_thread._is_stopped = True

    def run(self):
        self.image_grabber.spin()


