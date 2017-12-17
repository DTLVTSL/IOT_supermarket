import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import json
from firebase import firebase
import pyrebase
firebase = firebase.FirebaseApplication('https://smarkt-bac7b.firebaseio.com', None)

config = {
	"apiKey": "AIzaSyCZJPQxO69Jo96XqIEWtSN2CXnca5oMaJo",
	"authDomain": "smarkt-bac7b.firebaseapp.com",
	"databaseURL": "https://smarkt-bac7b.firebaseio.com",
	"storageBucket": "smarkt-bac7b.appspot.com",
	"serviceAccount": "smarkt-bac7b-firebase-adminsdk-lpndi-3cf4cb9c91.json"
}

firebasee = pyrebase.initialize_app(config)


products=["Asparagus",
"Baked stuffed portabello mushrooms",
"Baking cake",
"Basil",
"Beet juice",
"Breakfast with cottage",
"Breakfast with muesli",
"Brown eggs",
"Caprese salad",
"Cherry",
"Corn",
"Cranberry juice",
"Cuban sandwiche",
"French fries",
"Fresh blueberries",
"Fresh pears",
"Fresh stawberry",
"Fresh tomato" ,
"Fresh-squeezed orange juice",
"Fruits bouquet" ,
"Granola" ,
"Grapefruit juice",
"Green beans" ,
"Green smoothie" ,
"Ground beef meat burger",
"Hazelnut in black ceramic bowl",
"Healthy breakfast" ,
"Homemade bread" ,
"Honey" ,
"Italian ciabatta" ,
"Legums",
"Lemon and salt",
"Oranges",
"Peaches on branch",
"Pears juice",
"Pesto with basil",
"Pineapple juice",
"Plums",
"Pomegranate juice",
"Raw asparagus",
"Raw legums",
"Ricotta",
"Rustic breakfast" ,
"Sandwich with salad" ,
"Sliced lemons" ,
"Smashed avocado" ,
"Smoothie with chia seeds",
"Strawberries",
"Strawberry and mint",
"Strawberry jelly" ,
"Strawberry smoothie",
"Sugarcane juice",
"Sweet fresh stawberry" ,
"Tomatoes",
"Vegan",
"Vegan food",
"Wheatgrass juice",
"Yogurt"]

dayweek=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
dayweeky=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day=[]
produc=[]
timest=[]
qty=[]
dates = []
dates1=[]
prices = []
i=0
j=0
def get_data():
	
	dayweek[0] = firebase.get('/statistics/Monday', None)
	dayweek[1] = firebase.get('/statistics/Tuesday', None)
	dayweek[2] = firebase.get('/statistics/Wednesday', None)
	dayweek[3] = firebase.get('/statistics/Thursday', None)
	dayweek[4] = firebase.get('/statistics/Friday', None)
	
	for i in range(4):
		for j in range(55):
			if i==0:
				if j==0:
					price = dayweek[i].values()[j]
					prices =price.values()
					a=0
					for a in range (len(prices)):
						dates.append(a)
					print prices
					print dates
					name = str( dayweeky[i]+ "_" + products[j])
					predict_next = len(prices)-1
					print predict_next
					predicted_price = predict_price(name,dates, prices,predict_next)
			if i==1:
				if j==0:
					price = dayweek[i].values()[j]
					prices =price.values()
					a=0
					for a in range (len(prices)):
						dates1.append(a)
					print prices
					print dates1
					name = str( dayweeky[i]+ "_" + products[j])
					predict_next = len(prices)-1
					print predict_next
					predicted_price = predict_price(name,dates1, prices,predict_next)


	return

def predict_price(name,dates, prices, x):
	salv =str(name+".png")
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models
	svr_rbf.fit(dates, prices) # fitting the data points in the models
	plt.scatter(dates, prices, color= 'black', label= 'Data') # plotting the initial datapoints 
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'Products acquired') # plotting the line made by the RBF kernel
	plt.xlabel('Date')
	plt.ylabel('Products acquired')
	plt.title(name)
	plt.legend()
	plt.savefig(salv)   # save the figure to file
	plt.show()
	storage = firebasee.storage()
	storage.child(salv).put(salv)
	print svr_rbf.predict(x)[0]
	paycheck=firebase.patch('/statistics/'+name+'/',{'next':int(round(svr_rbf.predict(x)[0]))})
	#plt.close(fig) 
	

get_data() # calling get_data method by passing the csv file to it

#predicted_price = predict_price(dates, prices, 29)


