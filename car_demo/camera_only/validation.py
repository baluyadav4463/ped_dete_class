#!/usr/bin/env python

import cv2
import os
import sys
import datetime

import pandas as pd

from drive_run import DriveRun
from config import Config
from image_process import ImageProcess


csv_header = ['image_name', 'class', 'prediction']
csv_path = '/home/yadav/Data_collection/classification_validation/out.csv'
csv_path_2 = '/home/yadav/Data_collection/classification_validation'
csv_path_out = '/home/yadav/Desktop/validation.csv'
model_path = '/home/yadav/Data_collection/classification/trained models/3cnn/final'
measurements = []

def main():
        drive_run = DriveRun(model_path)
	config = Config()
	image_process = ImageProcess()
	df = pd.read_csv(csv_path, names=csv_header, index_col=False)
	#df = df.values
	#print(len(df))
	image_names = df['image_name']
	#print(image_names)
        drive_run = DriveRun(model_path)
	for i in image_names:
		image = cv2.imread(csv_path_2 + '/' + i)
		#print(i)
		image = cv2.resize(image, (config.image_size[0], config.image_size[1]))
		image = image_process.process(image) 
		measurement = drive_run.run(image)
		measurement = measurement[0]
		if measurement[0] == max(measurement):
			measurements.append('away')
		elif measurement[1] == max(measurement):
			measurements.append('standing')
		elif measurement[2] == max(measurement):
			measurements.append('talking')
		else:
			measurements.append('towards')
		#print(measurement)
	
	#print(measurements)
	df['prediction'] = [i for i in measurements]
	export_csv = df.to_csv(csv_path_out, index=False)

if __name__=='__main__':
	main()
