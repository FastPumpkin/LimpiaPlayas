#!/usr/bin/env python

import rospy
import cv2 as cv
import numpy as np 
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int32

# Se crean los Publicadores de las coordenadas del centroide del objeto a detectar
pubx = rospy.Publisher('coordenadas_x',Int32,queue_size=10)
puby = rospy.Publisher('coordenadas_y',Int32,queue_size=10)




def nothing(x):
    pass

def showImage(img):
    #Se definen los TrackBars que definen los limites de los parametros para el espacio de color HSV
    cv.namedWindow('image')
    cv.createTrackbar('Hue Minimo', 'image',0,255,nothing)
    cv.createTrackbar('Hue Maximo', 'image',0,255,nothing)
    cv.createTrackbar('Saturation Minimo', 'image',0,255,nothing)
    cv.createTrackbar('Saturation Maximo', 'image',0,255,nothing)
    cv.createTrackbar('Value Minimo', 'image',0,255,nothing)
    cv.createTrackbar('Value Maximo', 'image',0,255,nothing)
    

    hMin = cv.getTrackbarPos('Hue Minimo','image')
    hMax = cv.getTrackbarPos('Hue Maximo','image')
    sMin = cv.getTrackbarPos('Saturation Minimo','image')
    sMax = cv.getTrackbarPos('Saturation Maximo','image')
    vMin = cv.getTrackbarPos('Value Minimo','image')
    vMax = cv.getTrackbarPos('Value Maximo','image')
        
    lower = np.array([hMin,sMin,vMin])
    upper = np.array([hMax,sMax,vMax])
   
    
    #Convertir img de RGB -> HSV
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    #Mascara con pixeles dentro del rango de colores establecido
    mask = cv.inRange(hsv,lower,upper)
    kernel = np.ones((10,10),np.uint8)
    mask = cv.morphologyEx(mask,cv.MORPH_OPEN,kernel)
    mask = cv.morphologyEx(mask,cv.MORPH_CLOSE,kernel)

    #Deteccion de areas dentro de la mascara
    moments = cv.moments(mask)
    area = moments['m00']
    edged = cv.Canny(mask,35,125)
    image,cnt,hierarchy= cv.findContours(edged,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
  

    if(area > 20000):
        #Buscar centro x, y del objeto
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])


        #publicar e imprimir coordenadas
        pubx.publish(x)
        puby.publish(y)
        
        #Dibujar marca en el centro del objeto
        cv.rectangle(img,(x,y),(x+2,y+2),(0,0,255),2)
    
    cv.imshow('mask',mask)
    cv.imshow('image',img)
    #cv.imshow('edged',edged)
    cv.waitKey(1)

    

def callback(msg):
    try:
        #Se convierte la imagen adquirida en un formato soportado por OpenCv
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg,"bgr8")
            
        showImage(orig)

    except CvBridgeError as e:
        print(e)


rospy.init_node('camera_subs')
sub = rospy.Subscriber('rgb/image', Image, callback)
rospy.spin()