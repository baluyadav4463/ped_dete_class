#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 14:35:34 2017

@author: jaerock
"""
import tensorflow as tf
from keras import applications
#from keras.applications.vgg16 import VGG16
#from keras.applications.vgg16 import preprocess_input
from keras.models import Sequential
from keras.layers import Lambda, Dropout, Flatten, Dense, Activation
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, Convolution2D, AveragePooling2D 
#, Cropping2D
from keras.optimizers import SGD

from config import Config
#run_opts = tf.RunOptions(report_tensor_allocations_upon_oom = True)
class NetModel:
    def __init__(self, model_path):
        self.model = None
        model_name = model_path[model_path.rfind('/'):] # get folder name
        self.name = model_name.strip('/')

        self.model_path = model_path
        self.config = Config()

        self._model()
        
    ###########################################################################
    #
     
    def _model(self):
        input_shape = (self.config.image_size[1], self.config.image_size[0],
                       self.config.image_size[2])

        self.model = Sequential([
                Lambda(lambda x: x/127.5 - 1.0, input_shape=input_shape),
                Conv2D(32, (3, 3), activation='relu', padding='valid'),
                Conv2D(32, (3, 3), activation='relu', padding='valid'),
                #MaxPooling2D(pool_size=(2, 2)),
                Conv2D(64, (3, 3), activation='relu', padding='valid'),
                #Conv2D(64, (3, 3), activation='relu', padding='valid'),
                #MaxPooling2D(pool_size=(2, 2)),
                Flatten(),
                Dense(100, activation='relu'),
		Dense(50, activation='relu'),
                Dense(self.config.num_outputs, activation='softmax')
        ])
        self._compile()

    ##########################################################################
    #
    def _compile(self):
        self.model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['accuracy'])


    ###########################################################################
    #
    # save model
    def save(self):
        
        json_string = self.model.to_json()
        open(self.model_path+'.json', 'w').write(json_string)
        self.model.save_weights(self.model_path+'.h5', overwrite=True)
    
    
    ###########################################################################
    # model_path = '../data/2007-09-22-12-12-12.
    def load(self):
        
        from keras.models import model_from_json
        
        self.model = model_from_json(open(self.model_path+'.json').read())
        self.model.load_weights(self.model_path+'.h5')
        self._compile()
        
    ###########################################################################
    #
    # show summary
    def summary(self):
        self.model.summary()	
    
        
