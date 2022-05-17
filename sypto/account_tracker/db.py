import psycopg2
from pymongo import MongoClient
import asset_alloc
from datetime import datetime

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

command = "CREATE TABLE master ( id SERIAL PRIMARY KEY, email VARCHAR NOT NULL, user_apikey VARCHAR NOT NULL, user_secretkey VARCHAR NOT NULL, exchange VARCHAR(255) NOT NULL, strategy VARCHAR NOT NULL, name VARCHAR NOT NULL, created_at DATE, user_balance INT)"

cursor.execute(command)
for doc in users.find():
	if 'user_apikey' not in doc or 'created_at' not in doc:
		continue
	name = doc['name']
	email = doc['email']
	api = doc['user_apikey']
	sec = doc['user_secretkey']
	exchange = doc['user_exchange']
	strategy = doc['user_strategy']
	created_date = doc['created_at']
	balance = doc['user_balance']
	
	dt = datetime.now()
	timestamp = datetime.timestamp(dt)
		
		
	command = " INSERT INTO master(email,user_apikey,user_secretkey,exchange,strategy,name,created_at,user_balance) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
	
	#record = (str(email),str(api),str(sec),str(exchange),str(strategy))
		
	cursor.execute(command,(email,api,sec,exchange,strategy,name,created_date,balance))
		
connection.commit()
		
#except Exception as e:
#	print(e)
	
#finally:
#	if connection:
#		cursor.close()
#		connection.close()
		
		
