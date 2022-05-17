from binance.client import Client

client = Client('XdhYyBBtvTJqexhvJXmw8YQH4b8RpmWOxNoskT7reTcbAjsQ9vbfTczjZKsU1F3r','xytjBEzxmQHVUiworR0rcBlpSKpMvuBH8CYieEYpQdizXICzuAZr4nbQKjNIJLSD')



#print(client.get_withdraw_history())
#deposits = client.get_deposit_history(startTime = 10)
#print(deposits)
print(client.get_account())

