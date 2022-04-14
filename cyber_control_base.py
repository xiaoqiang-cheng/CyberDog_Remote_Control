import grpc

import utils.cyberdog_app_pb2 as cyber_app_pb2
import utils.cyberdog_app_pb2_grpc as cyber_app_grpc

class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

class GrpcConnectBase(object):
    def __init__(self, dog_ip = "192.168.1.4") -> None:
        self.dog_ip = dog_ip
        self.stub = None

    def check_connect_ready(self):
        if (self.dog_ip is None):
            with grpc.insecure_channel(self.dog_ip + ':50051') as channel:
                try:
                    grpc.channel_ready_future(channel).result(timeout=10)
                except grpc.FutureTimeoutError:
                    return False
        self.stub = cyber_app_grpc.CyberdogAppStub(channel)
        return True

    def check_stand_up(self):
        if self.stub is None:
            return False
        # Stand up
        response = self.stub.setMode(
            cyber_app_pb2.CheckoutMode_request(
                next_mode=cyber_app_pb2.ModeStamped(
                    header=cyber_app_pb2.Header(
                        stamp=cyber_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyber_app_pb2.Mode(
                        control_mode=cyber_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
        return succeed_state

    def check_move_mode(self):
        # Change gait to walk
        if self.stub is None:
            return False
        response = self.stub.setPattern(
            cyber_app_pb2.CheckoutPattern_request(
                patternstamped=cyber_app_pb2.PatternStamped(
                    header=cyber_app_pb2.Header(
                        stamp=cyber_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    pattern=cyber_app_pb2.Pattern(
                        gait_pattern=cyber_app_pb2.Pattern.GAIT_TROT
                    )
                ),
                timeout=10
            )
        )
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
        return succeed_state

    def check_sit_down(self):
        if self.stub is None:
            return False
        response = self.stub.setMode(
            cyber_app_pb2.CheckoutMode_request(
                next_mode=cyber_app_pb2.ModeStamped(
                    header=cyber_app_pb2.Header(
                        stamp=cyber_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyber_app_pb2.Mode(
                        control_mode=cyber_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
        return succeed_state

    def send_data(self, linear:Vector3,  angular:Vector3):
        # 一切运动的本质就是在控制线速度和角速度
        if self.stub is None:
            return False
        self.stub.sendAppDecision(
            cyber_app_pb2.Decissage(
                twist=cyber_app_pb2.Twist(
                    linear=cyber_app_pb2.Vector3(
                        x=linear.x,
                        y=linear.y,
                        z=linear.z
                    ),
                    angular=cyber_app_pb2.Vector3(
                        x=angular.x,
                        y=angular.y,
                        z=angular.z
                    )
                )
            )
        )
        return True

class ControlBase(object):
    '''
        运动模式步骤：
        1，打开铁蛋APP，连接成功cyberdog
        2，指定IP， connect_cyber_dog
        3，切换到运动模式 switch_move_mode
        4，调用运动API 指定速度
    '''
    def __init__(self, dog_ip = "192.168.1.4") -> None:
        self.grpc_base = GrpcConnectBase(dog_ip)
        self.linear = Vector3(0, 0, 0)
        self.angular = Vector3(0, 0, 0)

    def connect_cyber_dog(self):
        ret = self.grpc_base.check_connect_ready()
        return ret

    def switch_move_mode(self):
        if self.grpc_base.stub is None:
            return False
        ret = self.grpc_base.check_stand_up()
        if ret:
            ret = self.grpc_base.check_move_mode()
        return ret

    def Stop(self):
        self.linear = Vector3(0, 0, 0)
        self.angular = Vector3(0, 0, 0)
        self.grpc_base.send_data(self.linear, self.angular)

    def GoForward(self, vx = 0.1):
        self.linear.x = vx
        self.linear.y = 0
        self.angular.z = 0
        self.grpc_base.send_data(self.linear, self.angular)

    def GoBack(self, vx = 0.1):
        self.linear.x = -vx
        self.linear.y = 0
        self.angular.z = 0
        self.grpc_base.send_data(self.linear, self.angular)

    def GoLeft(self, vy = 0.1):
        self.linear.x = 0
        self.linear.y = vy
        self.angular.z = 0
        self.grpc_base.send_data(self.linear, self.angular)

    def GoRight(self, vy = 0.1):
        self.linear.x = 0
        self.linear.y = vy
        self.angular.z = 0
        self.grpc_base.send_data(self.linear, self.angular)

    def TurnLeft(self, vz = 0.1):
        self.linear.x = 0
        self.linear.y = 0
        self.angular.z = vz
        self.grpc_base.send_data(self.linear, self.angular)


    def TurnRight(self, vz = 0.1):
        self.linear.x = 0
        self.linear.y = 0
        self.angular.z = -vz
        self.grpc_base.send_data(self.linear, self.angular)


    def MoveControl(self, vx = 0, vy = 0, vz = 0):
        self.linear.x = vx
        self.linear.y = vy
        self.angular.z = vz
        self.grpc_base.send_data(self.linear, self.angular)


if __name__ == "__main__":
    pass