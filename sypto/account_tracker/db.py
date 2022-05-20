import psycopg2
from pymongo import MongoClient
import asset_alloc
from datetime import datetime
from datetime import date
import decode
import asset_alloc
import json
import unrealised_and_realised_profit
import initial_cumulative_data
import exctract_csv_data

#try:

connection = psycopg2.connect(user = "postgres",
						password = "root$456",
						host = "117.248.111.132",
						port = "8080",
						database = "account_tracker")
							
cursor = connection.cursor()

#USE THIS ONCE THE DATABASE IS COMPLETED
#client = MongoClient('mongodb+srv://ravi0802:ravi1234@cluster0.c5w6y.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-dn7pog-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true')

#db = client.myFirstDatabase
#users = db.user

yester_day,yester_month,yester_year = unrealised_and_realised_profit.get_yesterday_date()
yesterday = date(yester_year,yester_month,yester_day)

email_data,api_data,sec_data,name_data,exchange_data,strategy_data = exctract_csv_data.get_csv_data()

for user_num in range(len(email_data)):
	try:
		#if 'user_apikey' not in doc or 'user_secretkey' not in doc:
		#	continue
		#obj_id = str(doc['_id'])
		#name = doc['name']
		name = name_data[user_num]
		#email = doc['email']
		email = email_data[user_num]
		#api = doc['user_apikey']
		#api = decode.decrypt(api)
		#api = 'hdS5tzGbTsrjsdllDn2w4yMyhC8kZOYyDRCFiRSjQlXMfUzJnoCe8heeLZHhHYUl'
		api = api_data[user_num]
		#sec = doc['user_secretkey']
		#sec = decode.decrypt(sec)
		#sec = 'z1AKxUZxLeBxxl7UHUdx80j6Xcuyv3WSXlmqN1AX'
		sec = sec_data[user_num]
		exchange = exchange_data[user_num]
		exchange = exchange.lower()
		#exchange = doc['user_exchange']
#		strategy = doc['user_strategy']
		strategy = strategy_data[user_num]
		
		today_price,quantity = asset_alloc.asset_allocation(api,sec,exchange)
			
		asset_alloc_percent = json.dumps(asset_alloc.find_total(today_price,quantity))
			
			
		total_holding = {}
		for i in quantity:
			total_holding[i] = quantity[i]*today_price[i]
				
		asset_alloc_amt = json.dumps(total_holding)
		
		unreal_profit_per_coin,total_unreal_profit,realised_profits_per_coin, total_realised_profit = unrealised_and_realised_profit.main(api,sec,exchange,today_price,quantity)
			
		unreal_profit_per_coin = json.dumps(unreal_profit_per_coin)
			
		realised_profits_per_coin = json.dumps(realised_profits_per_coin)
		
		#DO THIS ONLY INITIALLY
		#initial_cumulative_profits = 0.0
		
		#after initial cumulative updation do this
		command = f"SELECT cummulative_pnl FROM all_user_data WHERE email = '{email}' AND date = '{yesterday}'"
		cursor.execute(command)
		result = cursor.fetchall()
		cummulative_pnl_today = 0
		if result != []:
			cummulative_pnl_till_yesterday = result[0][0]
			cummulative_pnl_today = total_realised_profit + cummulative_pnl_till_yesterday
		else:
			cummulative_pnl_today = 0.0
			
		#print('cpnl')
		#print(cummulative_pnl_today)
		
		
		
		
		
			
		dt = datetime.now()
		date = str(dt)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
		month = datem.month
		day = datem.day
			
		command = "INSERT INTO all_user_data(email,name,strategy,exchange,asset_allocation_amount,asset_alloc_percent,unrealised_profit_total,unrealised_profit_per_coin,realised_profit_total,realised_profit_per_coin,date,cummulative_pnl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			
		cursor.execute(command,(email,name,strategy,exchange,asset_alloc_amt,asset_alloc_percent,total_unreal_profit,unreal_profit_per_coin,total_realised_profit,realised_profits_per_coin,date,cummulative_pnl_today))
			
		print("USER INSERTED INTO MASTER")
		
		connection.commit()
			
			
		#print(email,"	",name,"	",strategy,"	",exchange,"	",asset_alloc_percent,"	",asset_alloc_amt,"		",unreal_profit_per_coin,"	",total_unreal_profit,"		",realised_profits_per_coin,"		",total_realised_profit,"	",date, initial_cumulative_profits,"\n")		
	
	
	except Exception as e:
		print(name)
		print(e)
		
		
connection.close()
cursor.close()
	
	
	
		
		
