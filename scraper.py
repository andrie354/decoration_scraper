import requests
from bs4 import BeautifulSoup
import codecs
import pandas as pd
import time

product_info = []
url = 'https://www.ruparupa.com/informastore/aksesoris-dan-dekorasi.html?size=48&from='
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

for x in range(0,100):
    page = int(x) * 48

    def get_data(url, headers=headers):
        r = requests.get(url+str(page), headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        #f = open('./local.html', 'wb')
        #f.write(r.content)
        #f.close()
        #file = codecs.open('local.html', 'r', 'utf-8')
        #info = file.read()
        #soup = BeautifulSoup(info, 'html.parser')
        return soup

    def parse(soup, product_info):
        results = soup.find_all('div', {'class': 'col-xs-3'})
        for result in results:
            try:
                title = result.find('h3', {'class': 'title limit-name'}).text.replace('\n', '')
                price = result.find('span', {'class': 'price'}).text.replace('Rp ', '').replace('\n', ''). \
                    replace('Rp                                                        ', '')
                promo = result.find('div', {'class': 'promotion'}).text.replace('\n', '')

                product = {
                    'title': title,
                    'price': price,
                    'promo': promo,

                }
                product_info.append(product)
                print('products found: ', len(product_info))
                time.sleep(3)
            except:
                print('-')
        return product_info

    def output(product_info):
        itempd = pd.DataFrame(product_info)
        #print(itempd.head())
        itempd.to_csv('output.csv')
        #print('Saved to CSV....')
        return


    soup = get_data(url, headers=headers)
    product_info = parse(soup, product_info)
    output(product_info)

