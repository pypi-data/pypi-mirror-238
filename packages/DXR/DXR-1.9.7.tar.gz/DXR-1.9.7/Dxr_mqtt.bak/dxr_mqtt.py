# -*- coding: utf-8 -*-
import json
import threading
import time

import paho.mqtt.client as mqtt

server_url = '127.0.0.1'
server_port = 1883
callback_dit = {}
publish_dit = []
mqttc = None
rc = -1
isPrintLog = False
client_id = str(int(time.time() * 1000))
topic_list_str_pub = ''
topic_list_str_sub = ''


def setServerUrl(url='127.0.0.1', port=1883, clientID=str(int(time.time() * 1000))):
    global server_url, server_port, client_id
    server_url = url
    server_port = port
    client_id = clientID


def setMqttLog(PrintLog=False):
    global isPrintLog
    isPrintLog = PrintLog


class Dxr_url_port:
    pass


def on_connect(client, userdata, flags, rrc):
    global rc
    rc = rrc
    print("Connected with result code " + str(rc))


# 一旦订阅到消息，回调此方法
def on_message(client, obj, msg):
    global callback_dit
    topic = msg.topic
    try:
        callback_dit[topic](json.loads(str(msg.payload, encoding="utf-8")), str(client._client_id, encoding='utf-8'))
    except Exception as ex:
        print(ex)
        keys = callback_dit.keys()
        topic_arr = topic.split("/")[1:]
        print(topic_arr)
        for item in keys:
            item_arr = item.split("/")[1:]
            print(item_arr)
            isThisTopic = True
            if len(item_arr) == len(topic_arr):
                for i in range(len(item_arr)):
                    if item_arr[i] == "+":
                        continue
                    if item_arr[i] != topic_arr[i]:
                        isThisTopic = False
                        break
            if isThisTopic:
                callback_dit[item](json.loads(str(msg.payload, encoding="utf-8")), topic)
                break


def callback():
    pass


# 一旦订阅成功，回调此方法
def on_subscribe(mqttc, obj, mid, granted_qos):
    # print("Subscribed: " + str(mid) + " " + str(granted_qos))
    pass


# 一旦有log，回调此方法
def on_log(mqttc, obj, level, string):
    global isPrintLog
    if isPrintLog:
        print(string)


def Mqtt():
    global mqttc, server_url, server_port, client_id
    if mqttc is None:
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        mqttc = mqtt.Client(client_id=client_id)
        mqttc.will_set('/topic/' + client_id, '', retain=True)
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        mqttc.on_log = on_log
        # 连接broker，心跳时间为60s
        mqttc.connect(server_url, server_port, 60)
        # 订阅该主题，QoS=0
        t = threading.Thread(target=mqttc.loop_forever)
        t.start()
    return mqttc


class Dxr_Subscriber:
    def __init__(self, topic, callback):
        global callback_dit, topic_list_str_pub, topic_list_str_sub
        self.mqttc = Mqtt()
        if isinstance(topic, str):
            self.mqttc.subscribe(topic)
            self.topic = topic
        else:
            self.mqttc.subscribe(topic.topic)
            self.topic = topic.topic
        self.callback = callback
        callback_dit[self.topic] = callback
        topic_list_str_sub = client_id + '_sub:\n'
        for item in callback_dit.keys():
            topic_list_str_sub = '' + topic_list_str_sub + item + '\n'
        self.mqttc.publish('/topic/' + client_id, retain=True, payload=topic_list_str_pub + topic_list_str_sub)


class Dxr_Publisher:
    def __init__(self, topic):
        global publish_dit, topic_list_str_pub, topic_list_str_sub
        if isinstance(topic, str):
            self.topic = topic
            self.data_type = None
        else:
            self.topic = topic.topic
            self.data_type = topic
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        self.mqttc = Mqtt()
        if self.topic not in publish_dit:
            publish_dit.append(self.topic)
        topic_list_str_pub = client_id + '_pub:\n'
        for item in publish_dit:
            topic_list_str_pub = '' + topic_list_str_pub + item + '\n'
        self.mqttc.publish('/topic/' + client_id, retain=True, payload=topic_list_str_pub + topic_list_str_sub)

    def publish(self, msg):
        if self.data_type:
            self.mqttc.publish(self.topic, str(msg), qos=0)
        else:
            self.mqttc.publish(self.topic, json.dumps(msg), qos=0)


class Dxr_UnSubscriber:
    def __init__(self, topic):
        global callback_dit
        self.topic = topic
        self.mqttc = Mqtt()
        self.mqttc.unsubscribe(self.topic)
        callback_dit.pop(self.topic)
