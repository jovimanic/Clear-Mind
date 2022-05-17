import psycopg2
from pymongo import MongoClient
import asset_alloc
from datetime import datetime
import temp
import asset_alloc
import json
import unrealised_profit

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
	if 'user_apikey' not in doc or 'created_at' not in doc:
		continue
	obj_id = str(doc['_id'])
	name = doc['name']
	email = doc['email']
	api = doc['user_apikey']
	api = temp.decrypt(api)
	sec = doc['user_secretkey']
	sec = temp.decrypt(api)
	exchange = doc['user_exchange']
	strategy = doc['user_strategy']
	
	asset_alloc_percent = json(asset_alloc.main(api,sec))
	
	today_price,quantity = asset_alloc.asset_allocation(api,sec)
	
	total_holding = {}	
	for i in quantity:
		total_holding[i] = quantity[i]*today_price[i]
		
	asset_alloc_amt = json(total_holding)
	
	unreal_profit_per_coin,total_unreal_profit,realised_profits_per_coin, total_realised_profit = unrealised_profit.main(api,sec)
	
	dt = datetime.now()
	date = str(dt)
	datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	month = datem.month
	day = datem.day
	
	real_profit_per_coin, total_real_profit = realised_profit.main(api,sec)
	
	
		
		
	command = "INSERT INTO master(email,user_apikey,user_secretkey,exchange,strategy,name,created_at,user_balance) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
	
	#record = (str(email),str(api),str(sec),str(exchange),str(strategy))
		
	cursor.execute(command,(email,api,sec,exchange,strategy,name,created_date,balance))
		
connection.commit()
		
#except Exception as e:
#	print(e)
	
#finally:
#	if connection:
#		cursor.close()
#		connection.close()
		
		
