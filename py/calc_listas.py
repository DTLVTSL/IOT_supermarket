#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
import datetime
import time
import sys
from firebase import firebase
import json
import string
global dict

daa = []
weight=[]
price=[]
qty_unit=[]
prov_weight=[]
prov_price=[]
timeconf_hist=[]
timelog_hist=[]
firebase = firebase.FirebaseApplication('https://smarkt-bac7b.firebaseio.com', None)
timestamp = str(int(time.time()))
##########################################################################################################

# SALES / check usuario/ checar lista / checar timeconf
#
##########################################################################################################
#timelog = firebase.get('/sales/teste/lista', 'timelogin')
#timeconf = firebase.get('/sales/teste/lista/timeconf', 'timeconf')

while True:
	
	#timelog check vector
	users_lista = firebase.get('/sales', None)
	users=users_lista.keys()
	for j in range (len(users)):
		label = '/sales/'+users[j]+'/lista'
		timelog = firebase.get('/sales/'+users[j]+'/lista', 'timelogin')
		timeconf = firebase.get('/sales/'+users[j]+'/lista/timeconf', 'timeconf')
		if timeconf in timeconf_hist:
			print("Existent valor")
		else:
			timeconf_hist.append(timeconf)
			print timeconf_hist
			if timeconf != 'none':
				produtos = firebase.get('/products', None)
				produtos_lista = firebase.get('/sales/'+users[j]+'/lista/produtos', None)
				#produtos_lista = firebase.get('/sales/teste/lista/produtos', None)
				prod_names = produtos.keys()
				prod_lsta = produtos_lista.values()
				#print prod_lsta
				d= json.dumps(prod_lsta)
				dict = json.loads(str(d))
				#print len(dict)
				#print len(produtos.keys())
			for i in range(len(dict)):
				A=str(dict[i]['prod'])
				daa.append(A)
				for n in range(len(produtos.keys())):
					if daa[i] == prod_names[n]:
						weight.append(produtos[daa[i]]['weight'])
						price.append(produtos[daa[i]]['price'])
						for h in range (len(produtos_lista.keys())):
							if daa[i] == dict[h]['prod']:
								qty_unit.append(dict[h]['qty'])
				prov_weight.append(weight[i] * qty_unit[i])
				prov_price.append(price[i] * qty_unit[i])
				print prov_weight[i]
				print prov_price[i]
			WEIGHTT= sum(prov_weight)
			PRICET=  sum(prov_price)	
			WP=firebase.patch('/sales/'+users[j]+'/lista',{'totalweight':WEIGHTT,'totalprice':PRICET,'paymentFLAG':0})
			LP=firebase.patch('/statistics/'+users[j]+'/'+timestamp,{'totalweight':WEIGHTT,'totalprice': PRICET,'listprodc': daa, 'qtties':qty_unit})
			
	time.sleep(5)
