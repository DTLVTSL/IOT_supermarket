#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
import datetime
import time
import sys
import imp
global data
ipBroker = "192.168.1.143"
portBroker = 1883
class chart_weight:

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

    def weight(self, topic):
		
        #ins = open("weight.txt","r").read()
        ins=1200
        print ins
        if ins is not None:
            hora = datetime.datetime.now()
            hora_s=hora.strftime ('%Y-%m-%dT%H:%M:%S+0100')
            j_temp = '{"id":"trolley1","sensor": "weight","reading":"'+str(ins)+'", "time":"'+hora_s+'"}'
            self.client.publish(topic, j_temp)
            print j_temp

topic = "$SMARKT/sensor"
weightSensor = chart_weight(1,"sensor","sensor/")
weightSensor.connection(ipBroker, portBroker)
weightSensor.weight(topic)


