#!/usr/bin/env python

import rospy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# Se define el dispositivo aa utilizar
cap = cv.VideoCapture(1)

#La funcion obtiene la imagen proveniente de la camara
def get_Image():
    ret,img = cap.read()
    array = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    return img

#Configuracion de nodo y publicador
rospy.init_node('camara')
pub = rospy.Publisher('rgb/image',Image,queue_size=100)
bridge = CvBridge()
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    try:

        frame = get_Image()
        cv.imshow('frame',frame)
        cv.waitKey(1)
        frame = np.uint8(frame)
        #e convierte la imagen a un formato soportado por ROS
        image_msg = bridge.cv2_to_imgmsg(frame,encoding="bgr8")
        pub.publish(image_msg)
        rate.sleep()
        
    except TypeError:
        continue