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


class Greeter(Server_pb2_grpc.MainServerServicer):

    # ==========
    def __init__(self):
        pass

    # ==========
    def getStream(self, request_iterator, context):
        timer = 0

        # リクエストデータを表示クラスに渡す
        for req in request_iterator:
            print('process time = ' + str(time.clock() - timer))
            timer = time.clock()
            dBuf = np.frombuffer(req.datas, dtype=np.uint8)
            dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
            yield Server_pb2.Reply(reply=1)


def serve():
    # サーバーを生成
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Server_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)
    # ポートを設定
    server.add_insecure_port('[::]:50051')
    # 動作開始
    server.start()
    print('server start')
    # プロセスが止まらないようにメインプロセスを常に動作させておく
    try:
        while True:
            time.sleep(1 / 60)
    except KeyboardInterrupt:
        server.stop(0)


serve()
