# クライアントから送信される映像データを表示する

# ============================================================
# import packages
# ============================================================
from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import Server_pb2
import Server_pb2_grpc
import sys


class ShowVideoStream:
    img = None
    thread = futures.ThreadPoolExecutor(max_workers=1)

    # ==========
    def start(self):
        self.thread.submit(self.ShowWindow)

    # ==========
    def set(self, img):
        self.img = img

    # ==========
    def ShowWindow(self):
        while True:
            if self.img is not None:
                cv2.imshow('dst Image', self.img)
                k = cv2.waitKey(1)
                if k == 27:
                    break


class Greeter(Server_pb2_grpc.MainServerServicer):
    def __init__(self):
        pass

    def getStream(self, request_iterator, context):
        for req in request_iterator:
            dBuf = np.frombuffer(req.datas, dtype=np.uint8)
            dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
            yield Server_pb2.Reply(reply=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Server_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    print('server start')
    try:
        while True:
            time.sleep(1 / 60)
            # print("-")
    except KeyboardInterrupt:
        server.stop(0)


serve()
