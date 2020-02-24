#!/usr/bin/env python

import rospy
import cv2
import os
import datetime
import time


from sensor_msgs.msg import Image
from image_converter import ImageConverter
from darknet_ros_msgs.msg import BoundingBox
from darknet_ros_msgs.msg import BoundingBoxes 

from drive_run import DriveRun
from config import Config
from image_process import ImageProcess

model_path = '/home/yadav/Data_collection/classification/trained models/3cnn/final'

ic = ImageConverter()
drive_run = DriveRun(model_path)
config = Config()
image_process = ImageProcess()
path = '/home/yadav/Data_collection/' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
if os.path.exists(path + 'standing'):
  print('path fucking exists')
else:
  os.makedirs(path + 'standing')

camera_text = open(str(path) + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".txt", "w+")

x_min = 0
y_min = 0 
x_max = 0
y_max = 0


measurements = []

def bb_callback(data):
  bb_points = data.bounding_boxes
  global x_min, y_min, x_max, y_max
  x_min = bb_points[0].xmin
  y_min = bb_points[0].ymin
  x_max = bb_points[0].xmax
  y_max = bb_points[0].ymax  



def image_callback(data):
  img = ic.imgmsg_to_opencv(data)
  crop_img = img[y_min:y_max, x_min:x_max]
  image = cv2.resize(crop_img, (config.image_size[0], config.image_size[1])) 
  cv2.imshow('fucking_bs', img)
  image = image_process.process(image)
  measurement = drive_run.run(image)
  measurement = measurement[0]
  if measurement[0] == max(measurement):
    measurements.append('not_crossing')
  elif measurement[1] == max(measurement):
    measurements.append('standing')
  elif measurement[2] == max(measurement):
    measurements.append('talking')
  else:
    measurements.append('crossing')
  #print('standing')
  
  #image = cv2.resize(crop_img, (18, 64))
  #image = cv2.Rectangle(img, (x_min, y_min), (x_max, y_max), color, thickness=1, lineType=1, shift=0)
  #time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
  #cv2.imwrite(str(path) + 'standing'+ str(time_stamp) + '.jpg', img)
  #camera_text.write(str(time_stamp) + ',' + str(x_min) + ',' + str(y_min) + ',' + str(x_max) + ',' + str(y_max) + "\r\n")
  

def main():
   rospy.init_node('data_collection')
   rospy.Subscriber('/darknet_ros/detection_image', Image, image_callback)
   rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, bb_callback)
   rospy.spin()

if __name__ == '__main__':
    main()
