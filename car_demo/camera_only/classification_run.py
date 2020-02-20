#!/usr/bin/env python

import rospy
import cv2
import os
import sys
import datetime


from sensor_msgs.msg import Image
from image_converter import ImageConverter
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess

from mirvehicle_msgs.msg import Control
from darknet_ros_msgs.msg import BoundingBox
from darknet_ros_msgs.msg import BoundingBoxes 


x_min = 0
y_min = 0
x_max = 0
y_max = 0


class Classifier:
    def __init__(self):
        rospy.init_node('chauffer')
        self.config = Config()
        self.ic = ImageConverter()
        self.image_process = ImageProcess()
        self.rate = rospy.Rate(10)
        self.drive = DriveRun(sys.argv[1])
        rospy.Subscriber('/darknet_ros/detection_image', Image, image_callback)
        rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, bb_callback)
        self.image = None
        self.image_processed = False


    def bb_callback(self, data):
        bb_points = data.bounding_boxes
        global x_min, y_min, x_max, y_max
        x_min = bb_points[0].xmin
        y_min = bb_points[0].ymin
        x_max = bb_points[0].xmax
        y_max = bb_points[0].ymax

    def image_callback(self, image):
        img = self.ic.imgmsg_to_opencv(image)
        crop_img = img[y_min:y_max, x_min:x_max]
        img = cv2.resize(crop_img, (self.config.image_size[0], self.config.image_size[1]))
        self.image = self.image_process.process(img)
        self.image_processed = True


if __name__=="__main__":
    try:
        classifier = Classifier()
        while not rospy.is_shutdown():
            global prediction
            if classifier.image_processed == True:
                prediction = classifier.drive.run(classifier.image)
                prediction = prediction[0]
                if max(prediction) == prediction[0]:
                    prediction = "away"
                elif max(prediction) == prediction[1]:
                    prediction = "standing"
                elif max(prediction) == prediction[2]:
                    prediction = "talking"
                else:
                    prediction = "towards"
        print(prediction)
        joy_pub = rospy.Publisher('bolt', Control, queue_size = 10)
        rate = rospy.Rate(10)

        controller = Control()
        if prediction == "away":
            controller.throttle = 0.1
        elif prediction == "standing":
            controller.throttle = 0.1
        elif prediction == "talking":
            controller.throttle = 0.1
        else:
            controller.throttle = 0.0

        joy_pub.publish(controller)
        print(controller.throttle)
        classifier.image_processed = False
        classifier.rate.sleep()

    except KeyboardInterrupt:
        print('\nShutdown requested. Exiting...')