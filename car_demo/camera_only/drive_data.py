#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:37:04 2017

@author: jaerock
"""

import pandas as pd

from progressbar import ProgressBar
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder


class DriveData:
    
    csv_header = ['image_fname', 'class_1', 'class_2']
    
    def __init__(self, csv_fname):
        self.csv_fname = csv_fname
        self.df = None
        self.image_names = []
        self.measurements = []
    
    def read(self):
        self.df = pd.read_csv(self.csv_fname, names=self.csv_header, index_col=False)
        self.df = self.df.values
                
        num_data = len(self.df)
        
        bar = ProgressBar()
	encoder = LabelEncoder()
        
        for i in bar(range(num_data)): # we don't have a title
            self.image_names.append(self.df[i][0])
	    #y = self.df[i][2]
	    #y = encoder.fit(y)
            #y = encoder.transform(y)
            #y = np_utils.to_categorical(y)
            self.measurements.append(self.df[i][2])
	encoder.fit(self.measurements)
	self.measurements = encoder.transform(self.measurements)
	self.measurements = np_utils.to_categorical(self.measurements)

