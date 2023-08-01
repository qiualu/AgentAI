print("Hello wolrd!")
import urllib3
import torch

import typing_extensions

print(torch.__version__)
print(torch.cuda.is_available())

# CUDA Version: 11.7
#
# pip3 install torch == 1.9.0+cu111 torchvision == 0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
#
# torch>=1.7.0,!=1.12.0
# torchvision>=0.8.1,!=0.13.0