import json,os

def convert_to_yolo(annotation_files, image_width, image_height, output_file):
    yolo_annotations = []
    files1 = os.listdir(annotation_files)
    for annotation_file in files1:

        # 获取文件名和扩展名
        file_name, ext = os.path.splitext(annotation_file)
        if ext == '.json':
            annotation_file = os.path.join(annotation_files, file_name + ".json")
            print(annotation_file)
        else:
            continue

        with open(annotation_file, 'r', encoding='utf-8') as f:
            annotation = json.load(f)

        shapes = annotation['shapes']

        for shape in shapes:
            label = shape['label']  # 中文类别名称
            points = shape['points']

            if label == '掉落物':
                label = 0
            elif label == '通关门':
                label = 1
            elif label == '怪':
                label = 2
            elif label == '角色':
                label = 3

            x1 = points[0][0] / image_width
            y1 = points[0][1] / image_height
            x2 = points[1][0] / image_width
            y2 = points[1][1] / image_height

            width = x2 - x1
            height = y2 - y1

            x_center = x1 + (width / 2)
            y_center = y1 + (height / 2)

            yolo_annotation = f"{label} {x_center} {y_center} {width} {height}"
            yolo_annotations.append(yolo_annotation)

        # yolo_annotations.append(file_name)
        output_filetxt  = os.path.join(output_file, file_name + ".txt")
        # output_filetxt = r"E:\Projece\python\AgentAI\yolov7\dataimg\dnfdata\labels\moszhi.txt"

        with open(output_filetxt, 'w', encoding='utf-8') as f:
            for annotation in yolo_annotations:
                f.write(annotation + '\n')

        yolo_annotations = []



# 示例用法
# annotation_files = ['annotation1.json', 'annotation2.json', 'annotation3.json']
annotation_file = r'E:\Projece\python\AgentAI\yolov7\dataimg\data_imgage'
image_width = 1600
image_height = 900
# output_file = 'yolo_annotations.txt'
output_file = r"E:\Projece\python\AgentAI\yolov7\dataimg\dnfdata\valid\labels"
convert_to_yolo(annotation_file, image_width, image_height, output_file)

