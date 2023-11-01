from Dxr_mqtt.dxr_mqtt_mulity import MQTTManagerGroup
import time, json

if __name__ == '__main__':
    server_info = [
        {
            "server_url": "10.10.0.101",
            "client_id": "10.10.0.101",
        },
        {
            "server_url": "10.10.0.195",
            "client_id": "10.10.0.195",
        }
    ]
    group = MQTTManagerGroup(server_info)

    # 使用装饰器定义回调
    @group.topic_callback('/get_speed_response')
    def handle_message_1(client_id, message):
        json_str = message.payload.decode()
        data = json.loads(json_str)  # 假设消息总是JSON格式
        print(f"Received message from {client_id}: {data}")
        
    # 使用publish方法发布消息
    while True:
        time.sleep(1)
        group.publish("10.10.0.101", "/test", {"speed": 50})
        group.publish("10.10.0.195", "/test", {"speed": 75})