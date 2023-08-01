import os
from PIL import Image


def convert_png_to_jpg(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            # 拼接文件路径
            file_path = os.path.join(folder_path, filename)

            # 打开并转换图片格式
            image = Image.open(file_path)
            new_file_path = os.path.splitext(file_path)[0] + ".jpg"
            image.convert("RGB").save(new_file_path, "JPEG")

            # 删除原先的png图片
            os.remove(file_path)

    print("转换完成！")


# 指定要转换的文件夹路径
folder_path = r"E:\Projece\python\AgentAI\yolov7-main\mask\valid\images"

# 调用函数进行转换
convert_png_to_jpg(folder_path)