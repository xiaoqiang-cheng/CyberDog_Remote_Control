
import socket
import time
import cv2
import numpy
import cv2
from cvzone.HandTrackingModule import HandDetector
from cyber_control_base import ControlBase

control_base = ControlBase(dog_ip = "192.168.1.4")
ret = False


def ReceiveVideo():
    address = ('0.0.0.0', 8002)
    detector = HandDetector(detectionCon=0.8)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    conn, addr = s.accept()
    print('connect from:'+str(addr))
    ret = False
    while not ret:
        ret = control_base.connect_cyber_dog()
        time.sleep(1)
        print("等待连接cyber dog")
        print("CyberDog 连接成功！")
    while 1:
        start = time.time()#用于计算帧率信息
        length = recvall(conn,16)#获得图片文件的长度,16代表获取长度
        stringData = recvall(conn, int(length))#根据获得的文件长度，获取图片文件
        data = numpy.frombuffer(stringData, numpy.uint8)#将获取到的字符流数据转换成1维数组
        decimg=cv2.imdecode(data,cv2.IMREAD_COLOR)#将数组解码成图像
        hands, img = detector.findHands(decimg)
        print(len(hands))
        if (len(hands) == 2):
            print("get two hands to reset!")
            control_base.switch_sit_mode()
        elif (len(hands) == 1):
            print(hands[0]["type"] )
            if hands[0]["type"] == "Right":
                print("detection right hand,ready hi five")
                control_base.HiFive()
            if hands[0]["type"] == "Left":
                control_base.switch_move_mode()
                print("detect left hand, ready to zuoyi")
        cv2.imshow('SERVER',img)#显示图像
        end = time.time()
        seconds = end - start
        fps  = 1/seconds;
        conn.send(bytes(str(int(fps)),encoding='utf-8'))
        k = cv2.waitKey(10)&0xff
        if k == 27:
            break
    s.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ReceiveVideo()
