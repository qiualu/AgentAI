import cv2
import numpy as np
import os
import argparse
import mss,math,torch



class YOLOv7:
    def __init__(self, path, conf_thres=0.7, iou_thres=0.5):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.class_names = ["drop", "door", "foe", "role"] # list(map(lambda x: x.strip(), open('coco.names', 'r').readlines()))
        # Initialize model
        self.net = cv2.dnn.readNet(path)
        print("[INFO] setting preferable backend and target to CUDA...")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        input_shape = os.path.splitext(os.path.basename(path))[0].split('_')[-1].split('x')
        self.input_height = int(input_shape[0])
        self.input_width = int(input_shape[1])
        
        self.output_names = self.net.getUnconnectedOutLayersNames()
        self.has_postprocess = 'score' in self.output_names
    
    def detect(self, image):
        input_img = self.prepare_input(image)
        blob = cv2.dnn.blobFromImage(input_img, 1 / 255.0)
        # Perform inference on the image
        self.net.setInput(blob)
        # Runs the forward pass to get output of the output layers
        outputs = self.net.forward(self.output_names)
        
        if self.has_postprocess:
            boxes, scores, class_ids = self.parse_processed_output(outputs)
        
        else:
            # Process output data
            boxes, scores, class_ids = self.process_output(outputs)
        
        return boxes, scores, class_ids
    
    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]
        
        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))
        
        # Scale input pixel values to 0 to 1
        return input_img
    
    def process_output(self, output):
        predictions = np.squeeze(output[0])
        
        # Filter out object confidence scores below threshold
        obj_conf = predictions[:, 4]
        predictions = predictions[obj_conf > self.conf_threshold]
        obj_conf = obj_conf[obj_conf > self.conf_threshold]
        
        # Multiply class confidence with bounding box confidence
        predictions[:, 5:] *= obj_conf[:, np.newaxis]
        
        # Get the scores
        scores = np.max(predictions[:, 5:], axis=1)
        
        # Filter out the objects with a low score
        valid_scores = scores > self.conf_threshold
        predictions = predictions[valid_scores]
        scores = scores[valid_scores]
        
        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 5:], axis=1)
        
        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)
        
        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        a = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), self.conf_threshold, self.iou_threshold)
        if isinstance(a, tuple):
            return [],[],[]
        indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), self.conf_threshold, self.iou_threshold).flatten()
        
        return boxes[indices], scores[indices], class_ids[indices]
    
    def parse_processed_output(self, outputs):
        
        scores = np.squeeze(outputs[self.output_names.index('score')])
        predictions = outputs[self.output_names.index('batchno_classid_x1y1x2y2')]
        
        # Filter out object scores below threshold
        valid_scores = scores > self.conf_threshold
        predictions = predictions[valid_scores, :]
        scores = scores[valid_scores]
        
        # Extract the boxes and class ids
        # TODO: Separate based on batch number
        batch_number = predictions[:, 0]
        class_ids = predictions[:, 1]
        boxes = predictions[:, 2:]
        
        # In postprocess, the x,y are the y,x
        boxes = boxes[:, [1, 0, 3, 2]]
        
        # Rescale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)
        
        return boxes, scores, class_ids
    
    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]
        
        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)
        
        # Convert boxes to xyxy format
        boxes_ = np.copy(boxes)
        boxes_[..., 0] = boxes[..., 0] - boxes[..., 2] * 0.5
        boxes_[..., 1] = boxes[..., 1] - boxes[..., 3] * 0.5
        boxes_[..., 2] = boxes[..., 0] + boxes[..., 2] * 0.5
        boxes_[..., 3] = boxes[..., 1] + boxes[..., 3] * 0.5
        
        return boxes_
    
    def rescale_boxes(self, boxes):
        
        # Rescale boxes to original image dimensions
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes
    
    def draw_detections(self, image, boxes, scores, class_ids):
        for box, score, class_id in zip(boxes, scores, class_ids):
            x1, y1, x2, y2 = box.astype(int)
            
            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
            label = self.class_names[class_id]
            label = f'{label} {int(score * 100)}%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            # top = max(y1, labelSize[1])
            # cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine), (255,255,255), cv.FILLED)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
        return image





范围DNF= [0,0,1600,900]

# "imageHeight": 900,
# "imageWidth": 1600



def 截屏(范围=None, 灰度=True):
    范围 = 范围DNF
    with mss.mss() as sct:
        # 设置需要捕获的区域（左上角坐标为(x1, y1)，宽度为width，高度为height）
        monitor = {"top": 范围[1], "left": 范围[0], "width": 范围[2], "height": 范围[3]}
        # 捕获屏幕特定位置
        screenshot = sct.grab(monitor)
        # 将PIL图像转换为NumPy数组
        image = np.array(screenshot)
        # 将图像转换为灰度图像
        if 灰度:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite(path, image) # 保存
        return image

def main():


    # 创建窗口并显示图像
    cv2.namedWindow('Image')
    # cv2.imshow('Image', resized_image)
    cv2.moveWindow('Image', 2000, 100)
    # cv2.waitKey(0)

    while True:
        image = 截屏(范围DNF)
        resized_image = cv2.resize(image, (int(image.shape[1] / 4), int(image.shape[0] / 4)))


        cv2.imshow('Image', resized_image)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':

    main()