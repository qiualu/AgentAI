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

game = windows()

g = game.获取窗口信息(1)
print(g)
path = "data/50"
index = 1000
通关提示区 = game.DNF_btn["关卡"]["毁坏的寂静城"]["王之摇篮"]["通关提示区"]
通关提示区[2] = 通关提示区[2] - 通关提示区[0]
通关提示区[3] = 通关提示区[3] - 通关提示区[1]
gray_image = game.截屏("区域",范围 = 通关提示区,灰度=False)
filepath = path + "/" + str(index) + ".png"
index += 1
cv2.imwrite(filepath, gray_image)  # 保存
print("filepath",filepath)

cv2.imshow('Continuous Screenshot', gray_image)
cv2.moveWindow('Continuous Screenshot', 2046, 24)
cv2.waitKey(3000)
# 关闭窗口和摄像头
cv2.destroyAllWindows()