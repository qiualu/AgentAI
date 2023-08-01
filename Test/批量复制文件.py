import os
import os
import shutil

def merge_folders(folder1,out):
    # 获取文件夹1和文件夹2中的文件列表
    files1 = os.listdir(folder1)


    # 创建新文件夹来存放合并后的文件
    merged_folder = out
    if not os.path.exists(merged_folder):
        os.makedirs(merged_folder)
    mmingzhi = 46
    # 遍历文件夹1和文件夹2中的文件
    for i in range(len(files1)):
        file1 = files1[i]

        # 获取文件名和扩展名
        file_name, ext = os.path.splitext(file1)

        if ext == '.png':
            # print(" png ")
            new_file_name = str(mmingzhi + 1).zfill(5)  # 递增命名，填充0至5位数字
            oldpng = os.path.join(folder1, file_name + ".png")
            oldjson = os.path.join(out, file_name + ".png")

            # new_filepng = os.path.join(merged_folder, new_file_name + ".png")
            # new_filejson = os.path.join(merged_folder, new_file_name + ".json")
            # shutil.copy2(oldpng, new_filepng)
            # shutil.copy2(oldjson, new_filejson)

            shutil.copy2(oldpng, oldjson)

            # mmingzhi += 1
            # print(oldpng,new_filepng,new_filejson)
        continue

        # 重命名并复制文件到新文件夹
        # new_file_name = str(i + 1).zfill(5)  # 递增命名，填充0至5位数字
        # new_file = os.path.join(merged_folder, new_file_name + ext)
        # print(file_name, ext)
        # 复制文件
        # os.rename(os.path.join(folder1, file1), os.path.join(folder1, new_file))
        # os.rename(os.path.join(folder2, file2), os.path.join(folder2, new_file))

        # print(f"{file1} and {file2} merged as {new_file}")
        # os.rename(os.path.join(folder1, file1), new_file)
    print("文件合并完成！")


import json



def merge_foldersxiu(folder1):
    # 获取文件夹1和文件夹2中的文件列表
    files1 = os.listdir(folder1)

    # 遍历文件夹1和文件夹2中的文件
    for i in range(len(files1)):
        file1 = files1[i]


        # 获取文件名和扩展名
        file_name, ext = os.path.splitext(file1)

        if ext == '.json':
            # print(" png ")
            # new_file_name = str(mmingzhi + 1).zfill(5)  # 递增命名，填充0至5位数字
            oldpng = os.path.join(folder1, file_name + ".png")
            oldjson = os.path.join(folder1, file_name + ".json")

            with open(oldjson, 'r', encoding="utf-8") as file:
                json_data = json.load(file)

            # json_data["imagePath"] =  file_name + ".png"
            print(json_data["imagePath"],file_name + ".png")
            # 更新 JSON 数据
            # json_data.update(update_data)

            # 保存更新后的 JSON 数据到原始文件
            # with open(oldjson, 'w', encoding="utf-8") as file:
                # json.dump(json_data, file, indent=4)





out = r"E:\Projece\python\AgentAI\yolov7\dataimg\boat_dataset\images"
# 示例用法
folder1 = r"E:\Projece\python\AgentAI\yolov7\dataimg\data_imgage"
merge_folders(folder1,out)
# merge_foldersxiu(r"E:\Projece\python\AgentAI\yolov7\dataimg\data_imgage")








"""
# 训练数据集
!python train.py --batch-size 4 --epochs 200 --data .dataimg/dnfdata.yaml --weights .\weights\yolov7.pt
#测试
!python .\detect.py --source ./leaf/valid/images --weights runs/train/leaf_det_model/weights/best.pt

"""


