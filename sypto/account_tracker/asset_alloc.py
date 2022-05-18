import ccxt

def asset_allocation(api,sec,exchange1):
	binance = ccxt.binance()
	wazirx = ccxt.wazirx()
	exchange_id = exchange1
	exchange_class = getattr(ccxt, exchange_id)
	exchange = exchange_class({
		'apiKey' : api,
		'secret' : sec,
		'enableRateLimit': True
		})
	
	available = exchange.fetch_balance()
	total = available['total']
	quantity = {}
	for i in total:
		if i == 'INR':
			continue
		if total[i] != 0.0:
			quantity[i] = total[i]
		
	price = {}
	for i in quantity:
		val = i+'/USDT'
		if i == 'USDT':
			price[i] = 1.0
			continue
		if exchange1 == 'binance':
			price[i] = binance.fetch_ticker(val)['close']
		else:
			price[i] = wazirx.fetch_ticker(val)['close']
		
	return price,quantity
	
def find_total(price,quantity):

	total_holding = {}	
	for i in quantity:
		total_holding[i] = quantity[i]*price[i]
	
	total_USDT = 0.0
	for i in total_holding:
		total_USDT += total_holding[i]
	
	for i in total_holding:
		total_holding[i] = total_holding[i]/total_USDT*100
	
	return total_holding
	
def main(api,sec,exchange):
	#api = '2Zuss4JKwsrMrq4DoG7Y8avsj9CA538S1NSd2sgT3JUE4LXO8gwKOV7IPUNjRb6z'
	#sec = 'G4Eo2iGX1Nh1vIDMNRnAFEuBXFsHQem7Kq7XtRvU5G3BeKXSBTwmqeV2aSiL3Jff'
	price,quantity = asset_allocation(api,sec,exchange)
	total = find_total(price,quantity)
	
	return total
	
if __name__ == '__main__':
	main(api,sec)
