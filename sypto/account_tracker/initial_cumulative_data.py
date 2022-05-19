import ccxt
from datetime import  datetime
import wazirx_trades
import time

coins = {'BTC':0,'ETH':1,'XRP':2,'ADA':3, 'SOL':4}

def month_calc(timestamp):
		dateandtime = datetime.fromtimestamp(timestamp//1000)
		date = str(dateandtime)
		datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		month = datem.month
		return month
		
def get_sorted_trades(api,sec,exchange1):
		if exchange1 == 'binance':
			exchange_id = 'binance'
			exchange_class = getattr(ccxt, exchange_id)
			exchange = exchange_class({
				'apiKey' : api,
				'secret' : sec
				})
		
		sorted_trades = []
		
		for c in coins.keys():
			s = c+'/USDT'
			if exchange1 == 'binance':
				trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
			else:
				time.sleep(1)
				trades = wazirx_trades.get_wazirx_trades(api,sec,s)
				
			for orders in trades:
				timestamp = orders['timestamp']
				month = month_calc(timestamp)
				side = orders['side']
				coin = c
				amount = orders['cost']
				sorted_trades.append([month,coin,side,amount])
			
		return sorted(sorted_trades, key = lambda a: a[0])
		
def profit_and_loss(sorted_trades):
		monthly_coin_status = []
		profits = []
		flag = -1
		for i in range(12):
			monthly_coin_status.append([0,0,0,0,0])
			profits.append([0,0,0,0,0])
		
		for orders in sorted_trades:
			coin = orders[1]
			side = orders[2]
			month = orders[0]
			month -= 1
			amount = orders[3]
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
		
def main(api,sec,exchange1):
	sorted_trades = get_sorted_trades(api,sec,exchange1)
	#print('im here')
	mcs,profits = profit_and_loss(sorted_trades)
	cumulative_profits = 0
	for coin_profit in profits:
		for i in coin_profit:
			cumulative_profits += i
			
		
	return cumulative_profits
