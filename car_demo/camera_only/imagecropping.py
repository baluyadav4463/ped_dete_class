# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:55:21 2018

@author: mir-lab
"""

from PIL import Image
import os.path, sys

path = "/home/mir-lab/Desktop/2018-02-12-17-10-41"
dirs = os.listdir(path)

def crop():
    for item in dirs:
        fullpath = os.path.join(path,item)         #corrected
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            imCrop = im.crop((0, 402, 800, 800)) #corrected
            imCrop.save(f + '.jpg')

crop()
