

from PyQt5.Qt import *
from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import json



class ThreadM(QThread):
    stepChanged = pyqtSignal(int, int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, url, file, HEADERS):
        super().__init__()
        self.url = url
        self.file = file
        self.HEADERS = HEADERS


    def run(self):        
        self.parseM()
        
    def parseM(self):

        html = self.get_html()
        if not html:
            if html != False:
                self.error.emit(
                    f'Error: status_code={html.status_code}'
                )
            return
        
        if html.status_code == 200:
            products = []
            section = self.url.split('/')[4]
            pages_count = self.get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                self.stepChanged.emit(page, pages_count)
                products.extend(self.get_content(page, section))
                self.msleep(50)
                
            self.finished.emit(products)

        else: 
            self.error.emit(f'Error: status_code={html.status_code}')

    def get_html(self, params=None):
        try:
            r = requests.get(self.url, headers=self.HEADERS, params=params)
            return r 
        except:
            self.error.emit(f'Error: Что-то пошло не так.')
            return False

    def get_pages_count(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.select('span.block')
        if pagination:
            return int(pagination[-1].get_text().replace('\n', ''))
        else:
            return 1

    def get_content(self, page, section):
        url = f'https://www.mechta.kz/api/new/catalog?properties=&page={page}&section={section}'
        rl = requests.get(url)
        data = []
        for j in rl.json()['data']['items']:
            title = j['title']
            ids = j['id']
            data.append({
                'product_ids': ids,
                'title': title
            })
        
        data = sorted(data, key=lambda x: x['product_ids'])
        res = {'product_ids': ','.join(str(i.get('product_ids')) for i in data)}

        rs = requests.post('https://www.mechta.kz/api/new/mindbox/actions/catalog', data=res).json()['data']

        data2 = []
        for item, k in rs.items():
            price = k['prices']['discounted_price']
            old_price = k['prices']['base_price']
            if old_price == price:
                old_price = 'Скидки нет'

            data2.append({
                'price': price,
                'old price': old_price
            })

        return [{**x, **y} for x, y in zip(data, data2)]