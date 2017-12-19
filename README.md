# SMARKT Supermarket
Smarkt is a system to reduce time on the payment because all users can use
the trolleys to scan and send your shop list to a database connected to 
a cashier. All trolleys have a barcode scanner and a weight sensor to 
check the real weight of products.

		The authetication of users using Firebase Auth, is a google
	service that can authenticate users using only client-side code.
		The Realtime Database based on Firebase provides a realtime database 
	and backend as a service.
		The Firebase Storage provides secure file uploads and downloads for
	Firebase apps,on this project is used to upload some statistical predictions 
	graphs for charging on the freeboard dashboard.

		On the electronic Trolley the hardware is composed by Raspberry Pi 
		+LCD Display+Weight sensor+barcode Scanner. 
		On software side we have:
			+ Control.py
				Broker of the trolley system subscribe messages of weight and
				Scanner sensor, create a timestamp of the user create a new 
				shop list, verify if the product exist on the user list, if 
				exist add quantity or delete message or create new on the list.
				Send a message with actual weight measured by a sensor.
				Each Trolley has has a fixed number.
			+ scanner.py
				Using OpenCV library, get image from webcam and remove from a
				barcode image the code, send the message by MQTT to control.py
				Message Topic:j_temp = '{"id":"trolley#","sensor":
				"scanner","reading":"'+str(codigo)+'", "time":"'+hora_s+'"}'
			+weight.py
				Measure the weight of total amount of purchased products of the
				client, senf message to control.py
				Message Topic: j_temp = '{"id":"trolley#","sensor":
				"weight","reading":"'+str(ins)+'", "time":"'+hora_s+'"}'

		On the supermarket payment control the hardware is a Raspberry Pi
		equiped with scanner 
		The code is:
			+payment_check.py
				Scan the trolley, verify if the weight measured by
				trolley sensor has the same value of the database
				value, if the user pay the purchase , send a
				message to control passage authorizing the passage
				to the user.
				
		There are a manager for list calculation the code is:
			+calc_listas.py
				Controll all information in the firebase, calc the total
				ammount of each user,and the total weight of each purchase.
				
		The dashboard show the statistics about future prediction of piurchases:
			+prediction.py
				Verify the statistics about purchases of the products on the
				history,quantity of each product buyied in specific week day,
				play a regression and predict the future purchase,
				generate a image and sent to the firebase.
			
		For the interface the user can:
			+register a new user 
			+login
			+Scan a Barcode
			+Confirm a shop list
		
		
	
	
	

