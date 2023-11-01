from concurrent import futures
import grpc
import cv2
import Server_pb2
import Server_pb2_grpc
import time
import base64
import sys

cap = cv2.VideoCapture(0)


def Request(frame):
    ret, buf = cv2.imencode('.jpg', frame)
    if ret != 1:
        return
    data = Server_pb2.Request(datas=buf.tobytes())
    print(len(data))
    yield data


def run():
    # 送信先を指定
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = Server_pb2_grpc.MainServerStub(channel)

    while True:

        try:
            ret, frame = cap.read()
            if ret != 1:
                continue
            cv2.imshow('Capture Image', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
            responses = stub.getStream(Request(frame))
            for res in responses:
                print(res)
            time.sleep(1 / 60)
        except grpc.RpcError as e:
            print(e.details())


run()
