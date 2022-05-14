import ccxt
from datetime import  datetime
reccur = [0]


def get_buy_sell():
	exchange_id = 'binance'
	exchange_class = getattr(ccxt, exchange_id)
	exchange = exchange_class({
		'apiKey' : '2Zuss4JKwsrMrq4DoG7Y8avsj9CA538S1NSd2sgT3JUE4LXO8gwKOV7IPUNjRb6z',
		'secret' : 'G4Eo2iGX1Nh1vIDMNRnAFEuBXFsHQem7Kq7XtRvU5G3BeKXSBTwmqeV2aSiL3Jff'
		})
	

	symbols = ['BTC','ETH','XRP','ADA', 'SOL']
	months = []
	for i in range(12):
		months.append([0,0])
	for sym in symbols:
		s = sym+'/USDT'
		trades = exchange.fetch_my_trades(symbol=s, since=None, limit=None, params={})
		for order in trades:
			timestamp = order['timestamp']
			dateandtime = datetime.fromtimestamp(timestamp//1000)
			date = str(dateandtime)
			datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
			month = datem.month
			month -= 1
			if order['side'] == 'buy':
				months[month][0] += order['cost']
			elif order['side'] == 'sell':
				months[month][1] += order['cost']
	return months	
		
		
def calc_PNL(months):
	pnl = []
	for i in range(12):
		pnl.append(0)
		
	for i in range(12):
		cp = months[i][0]
		sp = months[i][1]
		pnl[i] = sp-cp
		
	return pnl
	
def chargeable(pnl):
	c = []
	for i in range(12):
		c.append(0)
		
	for i in range(12):
		t = pnl[i]
		if t<0:
			reccur[0] += -t
		else:
			reccur[0] -= t
			
		if reccur[0] < 0:
			c[i] = -0.1*reccur[0]
			reccur[0] = 0
			
	return c
			
		
		
	
	
	
		
		
		
		
	
	




if __name__ == '__main__':
	m = get_buy_sell()
	pnl = calc_PNL(m)
	c = chargeable(pnl)
	print(c)
