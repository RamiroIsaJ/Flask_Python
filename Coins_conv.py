from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

coins_conv = ['EURUSD', 'USDCLP', 'USDPEN']
values_conv = list()


def real_val():
    # procedure to obtain value coin of present day
    for coins_c in coins_conv:
        url = 'https://es-us.finanzas.yahoo.com/quote/'+coins_c+'=X/'
        web = requests.get(url)
        b_soup = BeautifulSoup(web.content, 'html.parser')

        info = b_soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        coin = [float(info.text)]
        values_conv.append(coin)
    df = pd.DataFrame({'EUR/USD': values_conv[0], 'CLP/USD': values_conv[1], 'PEN/USD': values_conv[2]})
    df['CLP/USD'] = 1 / df['CLP/USD']
    df['PEN/USD'] = 1 / df['PEN/USD']
    return values_conv, df


def reals_val():
    # procedure to obtain history values of past 5 days
    for coins_c in coins_conv:
        url = 'https://finance.yahoo.com/quote/' + coins_c + '%3DX/history?p=' + coins_c + '%3DX'
        web = requests.get(url)
        b_soup = BeautifulSoup(web.text, 'lxml')
        i = 55
        cad = list()
        for k in range(5):
            head = b_soup.find('span', attrs={"data-reactid": str(i)}).text
            i += 14
            cad.append(float(head))
        values_conv.append(cad)

    df = pd.DataFrame({'EUR/USD': values_conv[0], 'CLP/USD': values_conv[1], 'PEN/USD': values_conv[2]})
    df['CLP/USD'] = 1 / df['CLP/USD']
    df['PEN/USD'] = 1 / df['PEN/USD']
    return df


def mockup_val():
    # procedure to generate mockup data base on present value coin
    data, v = real_val()
    new_list = []
    for i in data:
        new_n = np.random.uniform(-0.5, 1.5, 5)
        new_n.tolist()
        new_list.append(new_n+i[0])

    df = pd.DataFrame({'EUR/USD': new_list[0], 'CLP/USD': new_list[1], 'PEN/USD': new_list[2]})
    df['CLP/USD'] = 1 / df['CLP/USD']
    df['PEN/USD'] = 1 / df['PEN/USD']

    return df


def webhook(data):
    webhook_url = 'https://webhook.site/e1c8e1e6-e06c-4e1c-8a2c-176eb1a4f634'
    print(data)

    response = requests.post(webhook_url, data=data, headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s'
                         % (response.status_code, response.text))
    else:
        print('Message have send to webhook successfully')




