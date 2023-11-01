import json


class msg:
    topic = "/not_set_topic"

    def __init__(self):
        pass

    def __str__(self):
        co = self.__dict__
        return json.dumps(co)

    @staticmethod
    def getMsg(data):
        if isinstance(data, str):
            data = json.loads(data)
        msg_test = msg()
        for keyValue in data:
            msg_test.__setattr__(keyValue, data[keyValue])
        return msg_test


class test(msg):
    topic = "/test"

    def __init__(self):
        self.x = ""  # 只有web端发送带sn，服务端转发给客户端不需要sn
        self.y = ""  # float型
        self.z = ""  # float型


class app_cmd_vel(msg):
    topic = "/app_cmd_vel_test"

    def __init__(self):
        self.sn = ""  # 只有web端发送带sn，服务端转发给客户端不需要sn
        self.v = ""  # float型
        self.w = ""  #
        self.priority = 2

    def __str__(self):
        co = self.__dict__
        return json.dumps({
            "priority": co['priority'],
            "msg": {
                "v": co['v'],
                "w": co['w']
            }
        })


class cloud_platform_info(msg):
    def __init__(self):
        self.horizontal = ""  # 水平位置Int
        self.vertical = ""  # 垂直位置Int
        self.zoom = ""  # 变倍Int
        self.isPreset = ""  # 是否设置到预置点Int
        self.preset_state = ""  # 当前预置位状态Byte
        self.cam_ex_code = ""  # 云台模块异常代码Byte
