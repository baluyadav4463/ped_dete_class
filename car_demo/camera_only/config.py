#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 21:30:08 2017

@author: jaerock
"""

###############################################################################
#
class Config:
    def __init__(self): # model_name):
        self.version = (0, 4) # version 0.4
        self.valid_rate = 0.3
        self.image_size = (24, 68, 3) 
        self.num_outputs = 4  # classes
        self.fname_ext = '.jpg'
        self.num_epochs = 100 
        self.batch_size = 16 #64















"""
remember to change size to (24, 68,3) when using scratch network
"""
        
