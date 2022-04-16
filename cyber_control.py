from cyber_control_base import ControlBase
from remote_control_base import GameHandle
from remote_control_base import HandleState
import time


class CyberRemoteControl(object):
    def __init__(self) -> None:
        self.control_base = ControlBase(dog_ip = "192.168.1.4")
        ret = False
        while not ret:
            ret = self.control_base.connect_cyber_dog()
            time.sleep(1)
            print("等待连接cyber dog")
        print("CyberDog 连接成功！")

        self.remote_handle = GameHandle(joy_stick_index = 1)
        self.remote_handle.handle_connect(self.remote_callback)
        self.hz = 10


    def set_control_hz(self, hz):
        self.hz = hz


    def remote_callback(self, handle_state : HandleState):
        if handle_state.button["9"] == 1:
            self.control_base.switch_move_mode()

        elif handle_state.button["10"] == 1:
            self.control_base.switch_sit_mode()


    def run(self):
        self.remote_handle.spin()
        time.sleep(1 / self.hz)


if __name__ == "__main__":
    obj = CyberRemoteControl()
    obj.run()