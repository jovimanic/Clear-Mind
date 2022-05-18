import ccxt
from datetime import  datetime
from datetime import timedelta
import asset_alloc
import test



def month_calc(timestamp):
		dateandtime = datetime.fromtimestamp(timestamp//1000)
		date = str(dateandtime)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		month = datem.month
		day = datem.day
		year = datem.year
		return day,month,year
			
def get_yesterday_date():
	now = datetime.now()
	yesterday = now - timedelta(days = 1)
	yesterday = str(yesterday)
	datem = datetime.strptime(yesterday, "%Y-%m-%d %H:%M:%S.%f")
	month = datem.month
	day = datem.day
	year = datem.year
	return day,month,year
	
def get_realised_profits(sorted_trades,coin,realised_profits):
	yest_day,yest_month,yest_year = get_yesterday_date()
		
	if len(sorted_trades) == 0:
		realised_profits[coin] = 0
		return
			
			
	for i in range(len(sorted_trades)):
		order = sorted_trades[i]
		
		if order[0] != yest_month or order[3] != yest_day or order[4] != yest_year:
			continue
		elif order[1] == 'buy':
			continue
		else:
			break
	if i == len(sorted_trades)-1:
		realised_profits[coin] = 0
		return
			
	i -= 1
	while i >= 0:
		if sorted_trades[i][1] == 'sell':
			break
		else:
			i -= 1
			
	i += 1
	
	sorted_trades = sorted_trades[i:]
	
	cp = 0
	sp = 0
	
	for i in sorted_trades:
		if order[1] == 'buy':
			cp += order[2]
			
		else:
		
			sp += order[2]
			
	realised_profits[coin] = sp-cp
	
				
def unreal_and_real_profit(api,sec,exchange1):
	today_price,quantity = asset_alloc.asset_allocation(api,sec,exchange1)
	
	coins = {'BTC':0,'ETH':1,'XRP':2,'ADA':3, 'SOL':4}	
	exchange_id = exchange1
	exchange_class = getattr(ccxt, exchange_id)
	exchange = exchange_class({
		'apiKey' : api,
		'secret' : sec
		})
			
	sorted_trades = []
	
	buying_price = {}
		
	realised_profits = {}
	print(exchange)
	for c in coins.keys():
		s = c+'/USDT'
		if exchange1 == 'binance':
			trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
		else:
			trades = test.get_wazirx_trades(api,sec)
			
		for orders in trades:
			timestamp = orders['timestamp']
			day,month,year = month_calc(timestamp)
			side = orders['side']
			coin = c
			amount = orders['cost']
			sorted_trades.append([month,side,amount,day,year])
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
		if len(sorted_trades) != 0:
			sorted_trades.append(order)
				
				
		buying_price[c] = buy
		sorted_trades = []
			
		get_realised_profits(sorted_trades,coin,realised_profits)
			
			
			
	diff = {}
	for i in today_price:
		if i == 'USDT':
			continue
		if i not in coins:
			continue
		diff[i] = today_price[i]-buying_price[i]
			
	unreal_profits = {}
	for i in quantity:
		if i == 'USDT':
			continue
		if i not in coins:
			continue
		unreal_profits[i] = quantity[i]*diff[i]
			
	total_profits = 0
	for i in unreal_profits:
		total_profits += unreal_profits[i]
			
	total_real = 0
	for i in realised_profits:
		total_real += realised_profits[i]
			
			
	return unreal_profits,total_profits,realised_profits,total_real
		
def main(api,sec,exchange):
	#api = 'aFCprSG0d4LZk5cLaFb9uxNLKZOEdqNdrTKUQx6q6IiKX6v6FPeSmAfqSugtgHdJ'
	#sec = 'ProO0feSKcClt0xcp13a0gK7RWFwcrNi6gZIhbHX6SIYmKkB2CS0juBie215v1dY'
	return unreal_and_real_profit(api,sec,exchange)
	
		
if __name__ ==  '__main__':
	main(api,sec)
#except Exception as e:
#	print(e)		
		
				
					 
	
	
