import argparse
import time
from pathlib import Path


# import torch.backends.cudnn as cudnn
# from numpy import random
# from utils.datasets import LoadStreams, LoadImages,letterbox
# from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
#     scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
# from utils.plots import plot_one_box
# from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

import numpy as np
import cv2,socket,threading
import torch
from models.experimental import attempt_load
from yolov7.utils.datasets import letterbox
from yolov7.utils.general import check_img_size, non_max_suppression, set_logging
from yolov7.utils.torch_utils import select_device, TracedModel


from yolov7.DNFlib.dnfkernel import kernelapi


class DNFmanage(kernelapi):

    def __init__(self,opt):

        super().__init__()
        self.opt = opt
        self.running = False
        print(self.opt)

        # self.run()
        self.test()

        self.mainbreak = True


    def main(self):
        while True:
            if self.mainbreak:
                self.loop()
            else:
                break

    def loop(self):


    def test(self):
        print(self.DNF_btn)
        self.udp_loop()


    def start_thread(self):
        if not self.running:
            self.running = True
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.udpKey)
            thread.start()
            # thread = threading.Thread(target=self.DNF_loop)
            # thread.start()

            # thread = threading.Thread(target=self.跑图)
            # thread.start()

    # DNF_loop
    def stop_thread(self):
        print("stop DNF 循环")
        self.running = False


    def udp_loop(self):
        # 创建UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 8848)
        sock.bind(server_address)

        while True:
            data, address = sock.recvfrom(1024)
            print('从客户端', address, '接收到数据:', data.decode()[:-1])
            zl = data.decode()[:-1]
            # 根据接收到的命令控制while循环的状态

            # continue

            if int(zl) == 1:
                # self.跑图暂停 = False
                # self.index =  int(zl)
                self.start_thread()  # 启动游戏循环
                # self.跑图(int(zl))
                # pass

            # 根据接收到的命令控制while循环的状态
            if int(zl) < 13:
                self.跑图暂停 = False
                self.index =  int(zl)
                # self.start_thread()  # 启动游戏循环
                # self.跑图(int(zl))
                # pass
            elif zl == "13":
                self.跑图停止 = True
            elif zl == "14":
                self.start_thread()  # 启动游戏循环

            elif zl == "15":
                self.stop_thread()  # 启动游戏循环
            elif zl == "17":
                break

            elif zl == "19":
                self.xunhuan -= 1
                if  self.xunhuan <= 0:
                    self.xunhuan = 0
                print(" xlxunhuan : ", self.xunhuan, self.light)
            elif zl == "20":  # 退出整个程序
                self.xunhuan += 1
                print(" xlxunhuan : ", self.xunhuan, self.light)

            elif zl == "18":  # 退出整个程序
                if self.fangan:
                    self.fangan = False
                else:
                    self.fangan = True
            elif zl == "16":  # 退出整个程序
                if self.跑图暂停:
                    self.跑图暂停 = False
                else:
                    self.跑图暂停 = True

            # -----101 key相关-----
            elif int(zl) > 80 and int(zl) < 100:  # 退出整个程序
                if str(int(zl) - 80) in self.keyjson:
                    print("key记录的编号 : ",int(zl) - 80,self.keyjson[str(int(zl) - 80)])
                    self.udp跑图loopKeylist = self.keyjson2[str(int(zl) - 80)]
                else:
                    print("key记录的编号 : ",int(zl) - 120,"无记录")
            elif int(zl) > 100 and int(zl) < 120:  # 退出整个程序
                print("设置存储key记录的编号 : ",int(zl) - 100)
                self.udpKey_loop_keyindex = int(zl) - 100
            elif int(zl) > 120 and int(zl) < 140:  # 退出整个程序
                if str(int(zl) - 120) in self.key记录:
                    print("key记录的编号 : ",int(zl) - 120,self.key记录[str(int(zl) - 120)])
                    self.udp跑图loopKeylist = self.key记录[str(int(zl) - 120)]
                else:
                    print("key记录的编号 : ",int(zl) - 120,"无记录")
            elif int(zl) > 180 and int(zl) < 200:  # 退出整个程序
                if str(int(zl) - 180) in self.keyjson:
                    print("key记录的编号 : ",int(zl) - 180,self.keyjson[str(int(zl) - 180)])
                    self.udp跑图loopKeylist = self.keyjson[str(int(zl) - 180)]
                else:
                    print("key记录的编号 : ",int(zl) - 180,"无记录")
            elif  zl == "141":  # 退出整个程序 打印
                self.printKey = True
            elif  zl == "142":  # 退出整个程序
                self.printKey = False
            elif zl == "143":  # 退出整个程序
                self.udpKey_loop_keylist = []
            elif zl == "163":  # 退出整个程序
                print(" 待保存键盘 : ",self.udpKey_loop_keyindex,self.udpKey_loop_keylist)

            elif zl == "144":  # 退出整个程序
                self.start_udpKey_loop()
            elif zl == "164":  # 退出整个程序
                self.stop_udpKey_loop()
            elif zl == "145":  # 退出整个程序
                self.start_DNF_loop()
            elif zl == "165":  # 退出整个程序
                self.stop_DNF_loop()
            elif zl == "146":  # 退出整个程序
                self.start_udp跑图loop()
            elif zl == "166":  # 退出整个程序
                self.stop_udp跑图loop()

            elif zl == "147":  # 退出整个程序
                self.stopallloop()
                break
            elif zl == "148":  # 退出整个程序
                print(self.keyjson)
            elif zl == "149":  # 退出整个程序
                print(self.keyjson2)
            elif zl == "150":  # 退出整个程序
                self.udp跑图loopKeyindex = 0
                self.udp跑图loopKeyrun = True
                print("跑图开始")
            elif zl == "151":  # 退出整个程序
                self.udp跑图loopKeyindex = 0
                self.udp跑图loopKeyrun = False
                print("跑图暂停")
            elif zl == "152":  # 退出整个程序
                print("151 152 跑图开始暂停: ",self.udp跑图loopKeyrun,self.udp跑图loopKeyindex)
                print("146 166 跑图开始暂停: 线程开始 : ",self.runloop_udp跑图loop)
                print("self.printKey : ", self.printKey)
            elif zl == "170":  # 从头开始
                #self.udp跑图loopKeyindex = 0
                print("151跑图遍历列表 : ", self.udp跑图loopKeyindex, len(self.udp跑图loopKeylist), self.udp跑图loopKeylist)

            # 关闭套接字
        sock.close()


    def run(self):
        img0 = cv2.imread(r'E:\Projece\python\AgentAI\yolov7\mask\train\images\00031.jpg')
        self.start_torch()
        lt = self.discern(img0)

        img = letterbox(img0, self.imgsz, stride=self.stride)[0]
        # print("letterbox img  ", img.shape)
        img0tq = self.显示图片(img,1,lt)
        print("img0ds ", img0tq.shape )

        cv2.namedWindow('Image')
        cv2.imshow('Image', img0tq)
        cv2.moveWindow('Image', 2000, 100)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        return

        while True:
            img0 = self.截屏()

            # print(img0.shape)

            lt = self.discern(img0)
            img = letterbox(img0, self.imgsz, stride=self.stride)[0]
            img0tq = self.显示图片(img, 1, lt)
            cv2.imshow('Image', img0tq)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def start_torch(self):
        with torch.no_grad():
            # detect()
            self.torchinit()


    def torchinit(self, img=False):

        self.source, self.weights, self.view_img, self.save_txt, self.imgsz, self.trace = self.opt.source, self.opt.weights, self.opt.view_img, self.opt.save_txt, self.opt.img_size, not self.opt.no_trace

        # Initialize
        set_logging()
        self.device = select_device(opt.device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(self.imgsz, s=self.stride)  # check img_size

        if self.trace:
            self.model = TracedModel(self.model, self.device, self.opt.img_size)

        if self.half:
            self.model.half()  # to FP16

        # Get names and colors
        # names = model.module.names if hasattr(model, 'module') else model.names
        # colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(
                next(self.model.parameters())))  # run once
        self.old_img_w = self.old_img_h = self.imgsz
        self.old_img_b = 1

    def discern(self, im0s):
        tensor_list = []
        t0 = time.time()

        # im0s = 截屏(灰度=False)
        print(im0s.shape)
        if im0s.shape[2] == 4:
            im0s = cv2.cvtColor(im0s, cv2.COLOR_BGRA2BGR)

        # print(" im0s : ", im0s.shape)
        # img.shape (3, 384, 640)
        # im0s.shape (900, 1600, 3)
        img = letterbox(im0s, self.imgsz, stride=self.stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        # print(" 02 ************  img  : ", type(img))

        # Warmup
        if self.device.type != 'cpu' and (
                self.old_img_b != img.shape[0] or self.old_img_h != img.shape[2] or self.old_img_w != img.shape[3]):
            # print(" 03 ************  old_img_h  : ")
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            # print(" 03 ************  old_img_ b h w  ")
            for i in range(3):
                self.model(img, augment=self.opt.augment)[0]

        # print(" 04.5 ************  img  : ", type(img))

        # Inference
        # 识别
        with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = self.model(img, augment=self.opt.augment)[0]
        # 结果 转换
        # Apply NMS
        pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes,
                                   agnostic=self.opt.agnostic_nms)

        # Process detections
        for i, det in enumerate(pred):  # detections per image

            # print(f" 08 1 ************  det[i]  : ", type(det), type(i), i, len(det), det)
            tensor_list = det.tolist()
            print(f"识别结果 : ", len(tensor_list), img.shape, im0s.shape )

        t1 = time.time()
        print("时间 : ", t1 - t0, " 识别数量 ", len(tensor_list))
        return tensor_list




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='weights/dnf/last.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='mask/test/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
    opt = parser.parse_args()
    print("opt 初始配置 : ",opt)


    game = DNFmanage(opt)
    # game.run()

    # #check_requirements(exclude=('pycocotools', 'thop'))
    # with torch.no_grad():
    #     detect()