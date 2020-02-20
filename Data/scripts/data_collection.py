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


ic = ImageConverter()
path = '/home/yadav/Data_collection/' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
if os.path.exists(path):
  print('path fucking exists')
else:
  os.makedirs(path)

x_min = 0
y_min = 0 
x_max = 0
y_max = 0


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
  image = cv2.resize(crop_img, (18, 64))
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
  cv2.imwrite(str(path) + str(time_stamp) + '.jpg', image)
  

def main():
   rospy.init_node('data_collection')
   rospy.Subscriber('/darknet_ros/detection_image', Image, image_callback)
   rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, bb_callback)
   rospy.spin()

if __name__ == '__main__':
    main()
