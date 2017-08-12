# -*- coding: utf-8 -*-

from PIL import Image
import os,sys


try:
    Image.open("1.jpg").save("1.png")
except IOError:
    print(" cannot convers",i)