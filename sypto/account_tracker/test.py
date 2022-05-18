import ccxt

def get_wazirx_trades(api,sec):

	exchange_id = 'wazirx'

	exchange_class = getattr(ccxt, exchange_id)
	exchange = exchange_class({
		'apiKey' : api,
		'secret' : sec
		})
	
	return exchange.fetch_orders('ETH/USDT')
	
