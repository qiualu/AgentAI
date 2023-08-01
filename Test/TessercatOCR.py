import pytesseract
from PIL import Image



def 案例1():
    # 2,输出验证码
    image=Image.open('./data/文本.png')
    text=pytesseract.image_to_string(image,lang='chi_sim')
    print("text : ",text)

def 案例2():
    # 加载中文语言包
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

    # 读取图像并进行中文识别
    image = Image.open('./data/文本2.png')
    # text = pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)
    text = pytesseract.image_to_string(image, lang='chi_sim')
    print("text : ",text)


# 案例1() # pip install Cython==0.26.1
案例2()