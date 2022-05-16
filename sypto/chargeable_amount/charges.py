import ccxt
from datetime import  datetime
import sys
try:
	reccur = [0]
	coins = {'BTC':0,'ETH':1,'XRP':2,'ADA':3, 'SOL':4}


	def month_calc(timestamp):
		dateandtime = datetime.fromtimestamp(timestamp//1000)
		date = str(dateandtime)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		month = datem.month
		return month
	
	def get_sorted_trades(api,sec):
		exchange_id = 'binance'
		exchange_class = getattr(ccxt, exchange_id)
		exchange = exchange_class({
			'apiKey' : api,
			'secret' : sec
			})
		
		sorted_trades = [] 
		
		for c in coins.keys():
			s = c+'/USDT'
			trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
			for orders in trades:
				timestamp = orders['timestamp']
				month = month_calc(timestamp)
				side = orders['side']
				coin = c
				amount = orders['cost']
				sorted_trades.append([timestamp,month,coin,side,amount])
			
		return sorted(sorted_trades, key = lambda a: a[0])
	
	def profit_and_loss(sorted_trades):
		monthly_coin_status = []
		profits = []
		flag = -1
		for i in range(12):
			monthly_coin_status.append([0,0,0,0,0])
			profits.append([0,0,0,0,0])
		
		for orders in sorted_trades:
			coin = orders[2]
			side = orders[3]
			month = orders[1]
			month -= 1
			amount = orders[4]
			for i in range(5):
				if month != flag:
					monthly_coin_status[month][i] = monthly_coin_status[month-1][i]
					
			if side == 'buy':
				monthly_coin_status[month][coins[coin]] += amount
			else:
				profits[month][coins[coin]] += (amount - monthly_coin_status[month][coins[coin]])
				monthly_coin_status[month][coins[coin]] = 0
			flag = month
			
		return monthly_coin_status,profits
	
	def chargeable_amount(mcs,p):
		c = []
		for i in range(12):
			c.append(0)
		for month in range(12):
			profit = 0
			for i in p[month]:
				profit += i
			reccur[0] -= profit
				
			if reccur[0] < 0:
				c[month] = -0.1*reccur[0]
				reccur[0] = 0
			
		return c


	def main(api,sec):
		#api = 'aFCprSG0d4LZk5cLaFb9uxNLKZOEdqNdrTKUQx6q6IiKX6v6FPeSmAfqSugtgHdJ'
		#sec = 'ProO0feSKcClt0xcp13a0gK7RWFwcrNi6gZIhbHX6SIYmKkB2CS0juBie215v1dY'
		sorted_trades = get_sorted_trades(api,sec)
		monthly_coin_status,profits = profit_and_loss(sorted_trades)
		charge = chargeable_amount(monthly_coin_status,profits)
		print(charges)
	if __name__ == '__main__':
		main(api,sec)
		
		
except Exception as e:
	if str(e) == 'binance {"code":-1022,"msg":"Signature for this request is not valid."}':
		print('The API, SECRET KEY for this request is not valid')
	else:
		print(e)
		
	
