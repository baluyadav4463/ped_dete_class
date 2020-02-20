#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 9 16:14:50 2018

@author: MIR-LAB
"""

import sys
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
import cv2
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess

#image reszie parameter, same as used for training 
xMin = 0
yMin = 0
xMax = 640
yMax = 310

video = cv2.VideoCapture(0)

#pre process of image and then calculate the prediction and passing to steering_commands function
def predict_from_camera(drive):
    check, frame = video.read()
    cropImg = frame[yMin:yMax,xMin:xMax]
    newimg = cv2.resize(frame,(160,70))
    image_process = ImageProcess()                              #normalize the image
    IImage = cv2.cvtColor(newimg, cv2.COLOR_RGB2BGR)  
    IImage = image_process.process(IImage)
    prediction= drive.run(IImage)
    print(prediction)
    steering_commands(prediction)

#sending steering commands after the calibration
def steering_commands(prediction):
    joy_pub = rospy.Publisher('/joy', Joy, queue_size = 10)
    rospy.init_node('conerted_image', anonymous=True)
    rate = rospy.Rate(10)
    joy_data = Joy()
    #print(prediction)
#####################################################################################    
    if(prediction[0][0] < 0.1 and prediction[0][0] > -0.1):
	print("straight")
        prediction[0][0] = prediction[0][0]
        joy_data.axes = [0,0,0,0,0,0]
        joy_data.buttons = [0,0,0,1,0,0,0,1,0,0,0,0]
#####################################################################################
    elif(prediction[0][0] < 0.5 and prediction[0][0] > 0.1):
	print("Left")
        prediction[0][0] = prediction[0][0]
        joy_data.axes = [0,0,0,0,1.0,0]
        joy_data.buttons = [0,0,0,0,0,0,0,1,0,0,0,0]
#####################################################################################
    elif(prediction[0][0] < 1 and prediction[0][0] > 0.5):
	print("Ext.Left")
        prediction[0][0] = prediction[0][0]
        joy_data.axes = [0,0,0,0,0,1.0]
        joy_data.buttons = [0,0,0,0,0,0,0,1,0,0,0,0]
#####################################################################################        
    elif(prediction[0][0] < -0.1 and prediction[0][0] > -0.5):
	print("Right")
        prediction[0][0] = -prediction[0][0]
        joy_data.axes = [0,0,0,0,-1.0,0]
        joy_data.buttons = [0,0,0,0,0,0,0,1,0,0,0,0]
#####################################################################################
    elif(prediction[0][0] < -0.5 and prediction[0][0] > -1):
	print("Ext.Right")
        prediction[0][0] = prediction[0][0]
        joy_data.axes = [0,0,0,0,0,-1.0]
        joy_data.buttons = [0,0,0,0,0,0,0,1,0,0,0,0]
#####################################################################################
    joy_pub.publish(joy_data)
    print(prediction[0][0])
    camera_pub=rospy.Publisher('/Camera_Prediction', Float32, queue_size = 100)
    camera_pub.publish(prediction[0][0])

def main():
    try:
        if(len(sys.argv) != 2):
            print('Use model_name')
            return

        drive= DriveRun(sys.argv[1])

        while not rospy.is_shutdown():
            try:
                predict_from_camera(drive)
            except KeyboardInterrupt:
                break
                print("out")
    except KeyboardInterrupt:
        print('\nShutdown requested. Exiting...')

if __name__ == '__main__':    
	main()
