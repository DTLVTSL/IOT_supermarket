#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import *
import paho.mqtt.client as mqtt
import json
import datetime
import urllib2
import time
import random
import math
from weight import chart_weight
from firebase import firebase
firebase = firebase.FirebaseApplication('https://smarkt-bac7b.firebaseio.com', None)
d=[]
ipBroker = "192.168.1.143"
portBroker = 1883
#Trolley number 1

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("$SMARKT/sensor")

def on_message(client, userdata, msg):
	#verify wich user is logged
	user_logged = (firebase.get('/trolley/1', None)).values()[0]
	print user_logged
	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	print msg.payload
	dict = json.loads(str(msg.payload))
	d.append(str(msg.payload))
	
	if dict["id"]=="trolley1":
		if dict["sensor"]=="weight":
			weight=dict["reading"]
			time1=str(dict["time"])
			hora = datetime.datetime.now()
			hora_s=hora.strftime ('%Y-%m-%dT%H:%M:%S+0100')
			j_temp = '{"id":"trolley1","weight":"'+str(weight)+'","time":"'+hora_s+'"}'
			resW= firebase.patch('/sales/foo/lista/',{'totalweight':weight,'time':str(hora)})

		if dict["sensor"]=="scanner":
			scan=dict["reading"]
			scanner=str(scan)
			time1=str(dict["time"])
			hora = datetime.datetime.now()
			timestamp = str(int(time.time()))
			hora_s=hora.strftime ('%Y-%m-%dT%H:%M:%S+0100')
			j_temp = '{"id":"trolley1","scan":"'+str(scanner)+'", "time":"'+hora_s+'"}'
			print j_temp
			produtos = firebase.get('/products', None)
			prod_names = produtos.keys()
			#verify if the product exists
			for n in range(len(produtos.keys())):
					if scanner == prod_names[n]:
						print "produto existente na lista de produtos"
						#verify the total quantity of product
						lista_usuario = firebase.get('/sales/foo/lista/produtos', None)
						print lista_usuario
						res = None
						if lista_usuario==None:
							print timestamp
							unit_price = produtos.values()[n]['price']
							res= firebase.patch('/sales/foo/lista/produtos/'+timestamp,{'prod':scanner,'qty':1,'total_price':unit_price})
						else:
							
							lista_usuarioval = lista_usuario.values()
							for j in range (len(lista_usuario.keys())):
								if (scanner == (lista_usuarioval[j]['prod'])):
									quantity = lista_usuarioval[j]['qty'] +1
									unit_price = produtos.values()[n]['price']
									total_price = unit_price * quantity
									print quantity
									res= firebase.patch('/sales/foo/lista/produtos/'+ lista_usuario.keys()[j],{'prod':scanner,'qty':quantity,'total_price':total_price})
									print res
							if res== None :
								unit_price = produtos.values()[n]['price']
								res = firebase.patch('/sales/foo/lista/produtos/'+timestamp,{'prod':scanner,'qty':1,'total_price':unit_price})

def on_publish(self, attuatorControl, obj, mid):
	print("mid: "+str(mid))
	topic = "$SMARKT/control"
	self.client.publish(topic,'aaa')

def on_subscribe(self, attuatorControl, obj, mid, granted_qos):
	print "Subscribed"
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(self, attuatorControl, obj, level, string):
	print(string)

def run(self,ip,port):
	self.client.connect(ipBroker,portBroker,60)
	print "entrou no run"
	self.client.subscribe("$SMARKT/sensor", qos=2)
	rc=0
	while rc == 0:
		rc = self.client.loop()
		print"loop"
	return rc


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ipBroker,portBroker,60)
client.loop_forever()
