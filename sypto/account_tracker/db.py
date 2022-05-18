import psycopg2
from pymongo import MongoClient
import asset_alloc
from datetime import datetime
import decode
import asset_alloc
import json
import unrealised_and_realised_profit

#try:

connection = psycopg2.connect(user = "postgres",
						password = "root$456",
						host = "117.248.111.132",
						port = "8080",
						database = "account_tracker")
							
cursor = connection.cursor()

client = MongoClient('mongodb+srv://ravi0802:ravi1234@cluster0.c5w6y.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-dn7pog-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true')

db = client.myFirstDatabase
users = db.user


for doc in users.find():
	try:
		if 'user_apikey' not in doc or 'user_secretkey' not in doc:
			continue
		obj_id = str(doc['_id'])
		name = doc['name']
		email = doc['email']
		api = doc['user_apikey']
		#print(api, name)
		api = decode.decrypt(api)
		#api = 'aFCprSG0d4LZk5cLaFb9uxNLKZOEdqNdrTKUQx6q6IiKX6v6FPeSmAfqSugtgHdJ'
		sec = doc['user_secretkey']
		sec = decode.decrypt(sec)
		#sec = 'ProO0feSKcClt0xcp13a0gK7RWFwcrNi6gZIhbHX6SIYmKkB2CS0juBie215v1dY'
		exchange = doc['user_exchange']
		strategy = doc['user_strategy']
		
		asset_alloc_percent = json.dumps(asset_alloc.main(api,sec))
		
		today_price,quantity = asset_alloc.asset_allocation(api,sec)
		
		total_holding = {}	
		for i in quantity:
			total_holding[i] = quantity[i]*today_price[i]
			
		asset_alloc_amt = json.dumps(total_holding)
		
		unreal_profit_per_coin,total_unreal_profit,realised_profits_per_coin, total_realised_profit = unrealised_and_realised_profit.main(api,sec)
		
		dt = datetime.now()
		date = str(dt)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
		month = datem.month
		day = datem.day
		
		
		print(email,"	",name,"	",strategy,"	",exchange,"	",asset_alloc_percent,"	",asset_alloc_amt,"		",unreal_profit_per_coin,"	",total_unreal_profit,"		",realised_profits_per_coin,"		",total_realised_profit,"	",date,"\n")		
	
	except Exception as e:
		print(e)
		print(api,sec)
		print(name)
		continue
	
		
		
	command = "INSERT INTO master(email,name,strategy) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
	
	#record = (str(email),str(api),str(sec),str(exchange),str(strategy))
		
	#cursor.execute(command,(email,api,sec,exchange,strategy,name,created_date,balance))
		
#connection.commit()
		
#except Exception as e:
#	print(e)
	
#finally:
#	if connection:
#		cursor.close()
#		connection.close()
		
		
