import pygame


class HandleState:
    def __init__(self, button_num = 11, axis_num = 6, hat_num = 4) -> None:
        self.axis = {}
        self.button = {}
        self.hat = {}

        for i in range(button_num):
            self.button[str(i)] = 0

        for i in range(axis_num):
            self.axis[str(i)] = 0

        for i in range(hat_num):
            self.hat[str(i)] = (0, 0)

class GameHandle(object):
    def __init__(self, joy_stick_index = 1) -> None:
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(joy_stick_index)
        self.joystick.init()
        self.handle_state = HandleState()

        self.handle_callback = None

    def handle_connect(self, func):
        self.handle_callback = func

    def spin(self):
        while True:
            for event_ in pygame.event.get():
                # 退出事件
                if event_.type == pygame.QUIT:
                    pass
                elif event_.type == pygame.JOYBUTTONDOWN or event_.type == pygame.JOYBUTTONUP:
                    buttons = self.joystick.get_numbuttons()
                    for i in range(buttons):
                        button_value = self.joystick.get_button(i)
                        self.handle_state.button[str(i)] = button_value
                elif event_.type == pygame.JOYAXISMOTION:
                    axis = self.joystick.get_numaxes()
                    for i in range(axis):
                        axis = self.joystick.get_axis(i)
                        self.handle_state.axis[str(i)] = axis
                elif event_.type == pygame.JOYHATMOTION:
                    hats = self.joystick.get_numhats()
                    for i in range(hats):
                        hat = self.joystick.get_hat(i)
                        self.handle_state.hat[str(i)] = hat
                else:
                    pass
            self.handle_callback(self.handle_state)


if __name__ == "__main__":
    import time
    def fun(dic):
        print(dic.axis)
        print(dic.button)
        print(dic.hat)
        time.sleep(1)
    obj = GameHandle()
    obj.handle_connect(fun)
    obj.spin()