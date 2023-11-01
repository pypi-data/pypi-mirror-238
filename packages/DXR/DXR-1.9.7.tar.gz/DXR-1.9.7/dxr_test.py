from Dxr_grpc.dxr_grpc_server import Dxr_grpc_server
import cv2


def callbck(dst, json_data):
    # json_data的格式为：
    # {
    #     "type": "face  // 人脸识别",
    # }
    if json_data['type'] == 'face':
        # 模拟人脸识别
        cv2.rectangle(dst, (100, 100), (200, 200), (0, 0, 255), 2)
        cv2.putText(dst, 'face', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)   
    elif json_data['type'] == 'object':
        # 模拟物体识别
        cv2.rectangle(dst, (100, 100), (200, 200), (0, 255, 0), 2)
        cv2.putText(dst, 'object', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 返回处理后的图像和识别结果
    return dst, json_data

# 启动grpc服务，port为grpc服务端口，默认为50051，rec_callback为识别回调函数
server = Dxr_grpc_server(rec_callback=callbck)
server.run()