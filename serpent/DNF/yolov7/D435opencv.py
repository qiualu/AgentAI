import pyrealsense2 as rs
import numpy as np
import cv2
# import dlib
# from _dlib_pybind11 import *
# 创建一个管道
pipeline = rs.pipeline()

# 创建一个配置并配置管道以流式传输
#  颜色和深度流
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 开始流式传输
pipeline.start(config)
def showD435显示RGB图像与深度图像():
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)

    finally:
        # Stop streaming
        pipeline.stop()


def showD435显示RGB图像():
    try:
        while True:
            # 等待一个连续的帧：深度和颜色
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # 将颜色帧转换为 numpy 数组
            color_image = np.asanyarray(color_frame.get_data())

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)
            cv2.waitKey(1)

    finally:
        # Stop streaming
        pipeline.stop()




def showD435显示RGB单张测试():

    # 等待一个连续的帧：深度和颜色
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    # 将颜色帧转换为 numpy 数组
    color_image = np.asanyarray(color_frame.get_data())

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', color_image)
    cv2.waitKey(2000)

    pipeline.stop()


def yolov7_opencv():

    # Load YOLOv7 model and weights
    net = cv2.dnn.readNet("yolov7.weights", "yolov7.cfg")

    # Set up input layer
    layer_names = net.getLayerNames()

    output_layers = [layer_names[int(i) - 1] for i in net.getUnconnectedOutLayers()]

    # return
    classes = ["person", "dog", "cat"]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Load video
    # cap = cv2.VideoCapture("video.mp4")

    try:

        while True:
            # Read frame

            # 等待一个连续的帧：深度和颜色
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # 将颜色帧转换为 numpy 数组
            color_image = np.asanyarray(color_frame.get_data())

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)

            img = color_image

            # Resize and normalize
            height, width, channels = img.shape
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            # Forward pass through YOLOv7
            net.setInput(blob)
            outs = net.forward(output_layers)

            # Get detections
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Non-maximum suppression
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            print("indexes",indexes,"len(boxes)",len(boxes),"indexes",indexes)
            # Draw detections
            font = cv2.FONT_HERSHEY_SIMPLEX
            # for i in range(len(boxes)):
            #     if i in indexes:
            #         x, y, w, h = boxes[i]
            #         print("i",i ,class_ids[i])
            #         # label = str(classes[class_ids[i]])
            #         label = "person"
            #
            #         # # color = colors[i]
            #         # color = colors
            #         # cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            #         # cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

            # Show result
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == 27:
                break



    finally:
        # Stop streaming
        pipeline.stop()



    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # showD435显示RGB图像与深度图像()
    # showD435显示RGB图像()
    # showD435显示RGB单张测试()
    yolov7_opencv()


