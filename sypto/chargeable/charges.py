import ccxt
from datetime import  datetime

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
	'apiKey' : '2Zuss4JKwsrMrq4DoG7Y8avsj9CA538S1NSd2sgT3JUE4LXO8gwKOV7IPUNjRb6z',
	'secret' : 'G4Eo2iGX1Nh1vIDMNRnAFEuBXFsHQem7Kq7XtRvU5G3BeKXSBTwmqeV2aSiL3Jff'
	})
	

symbols = ['BTC','ETH','XRP','ADA', 'SOL']
months = [[(),()]]*12
print(months)
for sym in symbols:
	s = sym+'/USDT'
	trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
	cp = 0
	for order in trades:
		timestamp = order['timestamp']
		dateandtime = datetime.fromtimestamp(timestamp//1000)
		date = str(dateandtime)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		month = datem.month
		
	break
	
	
		
		
	
	

