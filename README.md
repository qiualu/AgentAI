#  游戏AI代理

### torch 框架
Terminal: ...
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

### redis 服务器
pip3 install redis
Redis
然后打开dos窗口 进入redis解压目录
cd C:\Program Files\Redis

运行下面命令启动
redis-server.exe  redis.windows.conf


还可以把redis加入都开机自启动
redis-server --service-install redis.windows-service.conf --loglevel verbose
* 异常
redis启动异常：# Creating Server TCP listening socket 127.0.0.1:6379: bind: No error
解决方法：
D:\Program Files\Redis>redis-cli.exe
127.0.0.1:6379> shutdown
not connected> exit
三步搞定，然后重新启动redis成功。

  
### OCR 图文识别  OCRopus or Tesseract
1) OCRopus 
* pip install ocropy
2) Tesseract
* C:\Program Files\Tesseract-OCR
* pip install pytesseract


### pywin32 
Cython==0.26.1

清华大学 ：https://pypi.tuna.tsinghua.edu.cn/simple/
阿里云：http://mirrors.aliyun.com/pypi/simple/
中国科学技术大学 ：http://pypi.mirrors.ustc.edu.cn/simple/
华中科技大学：http://pypi.hustunique.com/
豆瓣源：http://pypi.douban.com/simple/
腾讯源：http://mirrors.cloud.tencent.com/pypi/simple
华为镜像源：https://repo.huaweicloud.com/repository/pypi/simple/




