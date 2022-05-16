import charges
from flask import Flask
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ravi0802:ravi1234@cluster0.c5w6y.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-dn7pog-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true')

db = client.myFirstDatabase
users = db.user


app = Flask(__name__)

@app.route('/get_user_charges/<email>')
def index(email):
	
	#i = users.find_one({'email':email})
	#print(i)
	#api = i['user_apikey']
	#sec = i['user_secretkey']
		
	L = charges.main('XdhYyBBtvTJqexhvJXmw8YQH4b8RpmWOxNoskT7reTcbAjsQ9vbfTczjZKsU1F3r','xytjBEzxmQHVUiworR0rcBlpSKpMvuBH8CYieEYpQdizXICzuAZr4nbQKjNIJLSD')

	return str(L)
	
	
if __name__ == '__main__':
	app.run()
