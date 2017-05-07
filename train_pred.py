import pandas as pd
import numpy as np
import pickle
import os
import json


def get_json(coin):
    lines = [line.rstrip('\n') for line in open('price_data/' + coin + '.json')]
    df = pd.DataFrame()
    row = -1
    for line in lines:
        row = row + 1
        data = json.loads(line)
        for key in data["result"][0].keys():
            df.loc[row, key] = data["result"][0][key]
    return df


def read_data(data):
    data.columns = data.columns.str.lower()
    data['timestamp'] = pd.to_datetime(data.timestamp)
    data['created'] = pd.to_datetime(data.created)
    data.set_index('timestamp', inplace=True)
    return data.sort_index(ascending=False)


def make_smas(data):
    data = data.sort_index()
    data['time'] = data.index.hour
    data['sma_5'] = data['ask'].rolling(5).mean()
    data['sma_10'] = data['ask'].rolling(10).mean()
    data['sma_20'] = data['ask'].rolling(20).mean()
    data.dropna(inplace=True)
    data['pc_ch_5'] = data.sma_5.pct_change()
    data['pc_ch_10'] = data.sma_10.pct_change()
    data['pc_ch_20'] = data.sma_20.pct_change()
    data['sma5_ask_diff'] = (data.sma_5 - data.ask)
    data['sma10_ask_diff'] = (data.sma_10 - data.ask)
    data['sma20_ask_diff'] = (data.sma_20 - data.ask)
    data['spread'] = data.high - data.low
    return data.sort_index(ascending=False)


def clean_data(data):
    data.dropna(inplace=True)
    to_drop = ['prevday', 'opensellorders', 'last', 'created',
               'bid', 'openbuyorders', 'marketname', 'low', 'high', 'basevolume', 'sma_5', 'sma_10', 'sma_20']
    data.drop(to_drop, axis=1, inplace=True)
    data.dropna(inplace=True)
    return data.sort_index(ascending=False)


def file_exists(coin):
    files = [i.split('.')[0] for i in os.listdir('price_data/')]
    if coin in files:
        return True
    else:
        return False


def load_model(coin):
    with open('models/' + coin + '.pickle', 'rb') as mod:
        return pickle.load(mod)


def print_to_user(model, last_point):
    down = model.predict_proba(last_point)[0][0]
    up = model.predict_proba(last_point)[0][1]
    print('The probability of UP is {} and the probability of DOWN is {}'.format(up, down))


if __name__ == '__main__':
    coin = input('>>> coin name: '.lower())
    do_exist = file_exists(coin)
    if do_exist:
        data = get_json(coin)
        data = read_data(data)
        data = make_smas(data)
        data = clean_data(data)
        data = data[['volume',
                     'ask',
                     'pc_ch_5',
                     'pc_ch_10',
                     'pc_ch_20',
                     'sma5_ask_diff',
                     'sma10_ask_diff',
                     'sma20_ask_diff',
                     'spread',
                     'time']]
        X = data.head(1)
        last_point = X.values

        model = load_model(coin)
        print_to_user(model, last_point)
    else:
        print(coin + ' does not exist in the price_data folder')
