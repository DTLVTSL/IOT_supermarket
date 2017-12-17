#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
import datetime
import time
import sys
import cv2.cv as cv #Use OpenCV-2.4.3
import zbar

class chart_scanner:

    def __init__(self, sid,name,s_type):
        self.name = name
        self.id = sid
        self.s_type = s_type

    def connection(self, ip, port):
        def myOnConnect(self, userdata, flags, rc):
            print ("Connected to message broker with result code:"+str(rc))
        self.client = PahoMQTT.Client()
        self.client.on_connect = myOnConnect
        self.client.connect(ip,port, 60)
        self.client.loop(1)

    def scan(self, topic):
        if codigo is not None:
            hora = datetime.datetime.now()
            hora_s=hora.strftime ('%Y-%m-%dT%H:%M:%S+0100')
            j_temp = '{"id":"trolley1","sensor": "scanner","reading":"'+str(codigo)+'", "time":"'+hora_s+'"}'
            if codigo != 0:
				self.client.publish(topic, j_temp)
				print j_temp
            
    def scanner_procces(self,frame,set_zbar):
		codigo=0    
		set_width = 100.0 / 100
		set_height = 90.0 / 100
		coord_x = int(frame.width * (1 - set_width)/2)
		coord_y = int(frame.height * (1 - set_height)/2)
		width = int(frame.width * set_width)
		height = int(frame.height * set_height)
		get_sub = cv.GetSubRect(frame, (coord_x+1, coord_y+1, width-1, height-1))
		cv.Rectangle(frame, (coord_x, coord_y), (coord_x + width, coord_y + height), (255,0,0))
		cm_im = cv.CreateImage((get_sub.width, get_sub.height), cv.IPL_DEPTH_8U, 1)
		cv.ConvertImage(get_sub, cm_im)
		image = zbar.Image(cm_im.width, cm_im.height, 'Y800', cm_im.tostring())
		set_zbar.scan(image)
		for symbol in image:
				print '\033[1;32mResult : %s symbol "%s" \033[1;m' % (symbol.type,symbol.data)
				global codigo
				codigo = symbol.data
		cv.ShowImage("webcame", frame)
		#cv.ShowImage("webcame2", get_sub)
		cv.WaitKey(500)
		return codigo
		
if __name__ == "__main__":
	#set up our stuff
	cv.NamedWindow("webcame", cv.CV_WINDOW_AUTOSIZE)
	capture = cv.CaptureFromCAM(-1)
	set_zbar = zbar.ImageScanner()
	topic = "$SMARKT/sensor"
	scannerSensor = chart_scanner(1,"sensor","scannerSensor/")
	scannerSensor.connection('192.168.1.143', 1883)
	frame = cv.QueryFrame(capture)
	scannerSensor.scanner_procces(frame,set_zbar)
	scannerSensor.scan(topic)

