import pandas as pd

def get_csv_data():

	df = pd.read_csv('api_db.csv')

	#print(df.to_string())

	emails = df['Email'].to_list()
	apis = df['API Key'].to_list()
	secs = df['API Secret'].to_list()
	names = df['Name'].to_list()
	exchanges = df['Exchange'].to_list()
	strategy = df['Strategy'].to_list()


	return emails,apis,secs,names,exchanges,strategy
	
	
