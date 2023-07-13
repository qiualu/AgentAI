#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
import shlex
import time

import inspect


def  main():
    game_name = "DNF"
    data = f"python Serpent.py test"
    print(data,len(data),type(data))
    print(shlex.split(data))
    subprocess.call(shlex.split(data))




if __name__ == '__main__':
    # main()


