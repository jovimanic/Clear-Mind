import ccxt
from datetime import  datetime
import asset_alloc

def month_calc(timestamp):
		dateandtime = datetime.fromtimestamp(timestamp//1000)
		date = str(dateandtime)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		month = datem.month
		return month

def unreal_profit(api,sec):
	today_price,quantity = asset_alloc.asset_allocation(api,sec)
	
	
	coins = {'BTC':0,'ETH':1,'XRP':2,'ADA':3, 'SOL':4}	
	exchange_id = 'binance'
	exchange_class = getattr(ccxt, exchange_id)
	exchange = exchange_class({
		'apiKey' : api,
		'secret' : sec
		})
		
	sorted_trades = [] 
	
	buying_price = {}	
	
	for c in coins.keys():
		s = c+'/USDT'
		trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
		for orders in trades:
			timestamp = orders['timestamp']
			month = month_calc(timestamp)
			side = orders['side']
			coin = c
			amount = orders['cost']
			sorted_trades.append([month,side,amount])
			
		sorted_trades = sorted(sorted_trades, key = lambda a: a[0])
		buy = 0
		while True:
			if len(sorted_trades) == 0:
				break
			order = sorted_trades.pop()
				
			if order[1] == 'buy':
				buy += order[2]
			else:
				break
					
				
		buying_price[c] = buy
		sorted_trades = []
		
		
	diff = {}
	for i in today_price:
		if i == 'USDT':
			continue
		diff[i] = today_price[i]-buying_price[i]
		
	unreal_profits = {}
	for i in quantity:
		if i == 'USDT':
			continue
		unreal_profits[i] = quantity[i]*diff[i]
		
	total_profits = 0
	for i in unreal_profits:
		total_profits += unreal_profits[i]
		
		
	return unreal_profits,total_profits
	
def main(api,sec):
	#api = 'aFCprSG0d4LZk5cLaFb9uxNLKZOEdqNdrTKUQx6q6IiKX6v6FPeSmAfqSugtgHdJ'
	#sec = 'ProO0feSKcClt0xcp13a0gK7RWFwcrNi6gZIhbHX6SIYmKkB2CS0juBie215v1dY'
	print(unreal_profit(api,sec))
	
if __name__ ==  '__main__':
	main(api,sec)
	
	
			
				 
	
	
