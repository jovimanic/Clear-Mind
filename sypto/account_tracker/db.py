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
	if 'user_apikey' not in doc or 'user_secretkey' not in doc:
		continue
	obj_id = str(doc['_id'])
	name = doc['name']
	email = doc['email']
	api = doc['user_apikey']
	#print(api, name)
	api = decode.decrypt(api)
	api = '0la61y5gXanIWM4pBKHUkP3unDyyKQaqzsAF10KExjugrdNCOI18T62HJjp7kJKr'
	sec = doc['user_secretkey']
	sec = decode.decrypt(sec)
	sec = 'a2OtTFEKCBFKWReJqt8VJj7QJOa7Vj5WOMahZJQm'
	exchange = doc['user_exchange']
	exchange = 'wazirx'
	strategy = doc['user_strategy']
		
	asset_alloc_percent = json.dumps(asset_alloc.main(api,sec,exchange))
		
	today_price,quantity = asset_alloc.asset_allocation(api,sec,exchange)
		
	total_holding = {}	
	for i in quantity:
		total_holding[i] = quantity[i]*today_price[i]
			
	asset_alloc_amt = json.dumps(total_holding)
	
	unreal_profit_per_coin,total_unreal_profit,realised_profits_per_coin, total_realised_profit = unrealised_and_realised_profit.main(api,sec,exchange)
		
	unreal_profit_per_coin = json.dumps(unreal_profit_per_coin)
		
	realised_profits_per_coin = json.dumps(realised_profits_per_coin)
		
	dt = datetime.now()
	date = str(dt)
	datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
	month = datem.month
	day = datem.day
		
		#command = "INSERT INTO master(id,email,name,strategy,exchange,asset_allocation_amount,asset_alloc_percent,unrealised_profit_total,unrealised_profit_per_coin,realised_profit_total,realised_profit_per_coin,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		
		#cursor.execute(command,(obj_id,email,name,strategy,exchange,asset_alloc_amt,asset_alloc_percent,total_unreal_profit,unreal_profit_per_coin,total_realised_profit,realised_profits_per_coin,date))
		
		
		
		
	print(email,"	",name,"	",strategy,"	",exchange,"	",asset_alloc_percent,"	",asset_alloc_amt,"		",unreal_profit_per_coin,"	",total_unreal_profit,"		",realised_profits_per_coin,"		",total_realised_profit,"	",date,"\n")		
	
	
	#record = (str(email),str(api),str(sec),str(exchange),str(strategy))
		
	#cursor.execute(command,(email,api,sec,exchange,strategy,name,created_date,balance))
		
#connection.commit()
		
#except Exception as e:
#	print(e)
	
#finally:
#	if connection:
#		cursor.close()
#		connection.close()
		
		
