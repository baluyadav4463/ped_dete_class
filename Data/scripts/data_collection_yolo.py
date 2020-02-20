#!/usr/bin/env python

import rospy
import cv2
import os
import datetime
import time


from sensor_msgs.msg import Image
from image_converter import ImageConverter 


ic = ImageConverter()
path = '/home/yadav/Data_collection/' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/')
if os.path.exists(path):
  print('path fucking exists')
else:
  os.makedirs(path)

x_min = 200
y_min = 380 
x_max = 800
y_max = 600


def image_callback(data):
  img = ic.imgmsg_to_opencv(data)
  #crop_img = img[y_min:y_max, x_min:x_max]
  image = cv2.resize(img, (320, 320))
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
  cv2.imwrite(str(path) + str(time_stamp) + '.jpg', image)
  

def main():
   rospy.init_node('data_collection_yolo')
   rospy.Subscriber('/sensors/camera/image_raw', Image, image_callback)
   rospy.spin()

if __name__ == '__main__':
    main()
