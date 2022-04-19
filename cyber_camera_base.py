
import socket
import time
import cv2
import numpy
from cvzone.HandTrackingModule import HandDetector

class ImageGrabberBase(object):
    def __init__(self):
        self.sock = None
        self.cv_callback = None

    def cv_connect(self, func):
        self.cv_callback = func

    def scoket_connect(self, ip = "0.0.0.0", port = 8002):
        address = ('0.0.0.0', 8002)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print('connect from:'+str(addr))

    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def spin(self):
        while True:
            start = time.time()
            length = recvall(conn,16)
            stringData = recvall(conn, int(length))
            data = numpy.frombuffer(stringData, numpy.uint8)
            img=cv2.imdecode(data,cv2.IMREAD_COLOR)
            self.cv_callback(img)
            end = time.time()
            seconds = end - start
            fps  = 1/seconds
            conn.send(bytes(str(int(fps)),encoding='utf-8'))
        self.sock.close()

if __name__ == '__main__':
    ReceiveVideo()
