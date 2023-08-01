import json,cv2
#
# # 读取 JSON 文件
# with open('配置文件.json', 'r',encoding="utf-8") as file:
#     json_data = file.read()
#
# # 将 JSON 数据解析为字典
# data_dict = json.loads(json_data)
#
# # 现在，你可以像操作其他字典一样使用 data_dict
# print(data_dict)

from serpent.DNF.windows import windows

# game = windows()
#
# game.跑图(1)




import paho.mqtt.client as mqtt

# 连接成功回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("udpmanage")

# 消息接收回调函数
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# 创建客户端实例
client = mqtt.Client()

# 设置连接成功和消息接收的回调函数
client.on_connect = on_connect
client.on_message = on_message
print("start coo ")
# 连接到 MQTT 代理
client.connect("ws://175.178.159.67", 8083, 60)
print("start 123")
# 循环处理网络流量
client.loop_forever()













