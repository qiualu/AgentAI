
import paddleocr
from PIL import Image

# img = Image.open('af.png')
from paddleocr import PaddleOCR

ocr = PaddleOCR()
# result = ocr.ocr(img, det=True, rec=True)
imgname = 'data/af.png'
with open(imgname, 'rb') as f:
    img_bytes = f.read()

import time
start = time.time()
result = ocr.ocr(img_bytes, det=True, rec=True)
print("result: ",result,len(result))
for line in result:
    print('文本：', line[1][0])
    print('坐标：', line[0])

for line in result[0]:
    print('文本：', line[1][0])
    print('坐标：', line[0])


print("time: ", time.time()-start)