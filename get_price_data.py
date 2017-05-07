import requests as r
import time
import os


def make_request(coins, time_frame_in_min):
    """ writs json files containing price data for each element in the coins list """
    while True:
        for i in coins:
            a = r.get('https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-{}'.format(i)).text
            with open('price_data/' + str(i) + '.json', 'a') as f:
                f.write('{}\n'.format(a))

            time.sleep(60 * time_frame_in_min)


if __name__ == '__main__':
    if not os.path.exists('price_data'):
        os.makedirs('price_data')

    # if you added a coming to the list corresponding json file will be created and populated

    coins = ['etc', 'xrp', 'pivx', 'xem']
    time_frame_in_min = 15
    make_request(coins, time_frame_in_min)
