
import time
import os
import sys
import json
import requests
import yfinance as yf

path_file_dict_symbol_info = 'dict_symbol_info.json'
path_file_dict_symbol_history = 'dict_symbol_history.json'

if os.path.isfile(path_file_dict_symbol_info):
    with open(path_file_dict_symbol_info, 'r') as file:
        dict_symbol_info = json.load(file)
else: 
    dict_symbol_info = {}
    url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    text = requests.get(url).text
    list_line = text.split('\r\n')
    list_symbol = ''
    for line in list_line[1:]:
        list_part = line.split(',')
        if len(list_part) == 1:
            continue
        symbol_info = {}
        symbol_info['symbol'] = 'NDQ:' + list_part[0]
        symbol_info['company_name'] = list_part[1]
        symbol_info['securety_name'] = list_part[2]
        symbol_info['market_category'] = list_part[3]
        symbol_info['test_issue'] = list_part[4]
        symbol_info['financial_status'] = list_part[5]
        symbol_info['round_lot_size'] = list_part[6]

        dict_symbol_info[symbol_info['symbol']] = symbol_info
    with open(path_file_dict_symbol_info, 'w') as file:
        json.dump(dict_symbol_info, file)


print(len(dict_symbol_info))


if os.path.isfile(path_file_dict_symbol_history):
    with open(path_file_dict_symbol_history, 'r') as file:
        dict_symbol_history = json.load(file)
else:
    dict_symbol_history = {}
    for i, symbol in enumerate(dict_symbol_info):
        print(i)
        print(len(dict_symbol_info['nasdaq']))
        ticker_symbol = yf.Ticker(symbol.split(':')[1])

        # get stock info
        # msft.info
        # print(msft.info)
        # get historical market data
        hist = ticker_symbol.history(period="max")
        sys.stdout.flush()
        dict_symbol_history[symbol] = json.loads(hist.to_json(orient = "records"))

    with open(path_file_dict_symbol_history, 'w') as file:
        json.dump(dict_symbol_history, file)


#NYSE:ALB,

ticker_symbol= yf.Ticker('ALB')
dict_symbol_history['NYSE:ALB'] = {}
dict_symbol_history['NYSE:ALB']['symbol'] = 'NYSE:ALB'
dict_symbol_history['NYSE:ALB']['list_candle'] = json.loads(ticker_symbol.history(period="max").to_json(orient = "records"))


from matplotlib import pyplot as plt
plt.figure()
list_symbol = ['NYSE:ALB', 'NDQ:GOOGL', 'NDQ:AAPL', 'NDQ:FB', 'NDQ:MSFT']
for i, symbol in enumerate(list_symbol):
    list_candle = dict_symbol_history[symbol]['list_candle']
    list_close_30 = [float(candle['Close']) for candle in list_candle[-60:-1]]
    plt.subplot(len(list_symbol), 1, i + 1)
    plt.plot(list_close_30, label=symbol)
    plt.legend()
plt.show()
