from PyQt5.Qt import *
from pickle import TRUE
import requests
from bs4 import BeautifulSoup



class ThreadS(QThread):
    stepChanged = pyqtSignal(int, int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, url, file, HEADERS):
        super().__init__()
        self.url = url
        self.file = file
        self.HEADERS = HEADERS


    def run(self):        
        self.parseS()
        
    def parseS(self):

        html = self.get_html()
        if not html:
            if html != False:
                self.error.emit(
                    f'Error: status_code={html.status_code}'
                )
            return
        
        if html.status_code == 200:
            products = []
            pages_count = self.get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                self.stepChanged.emit(page, pages_count)
                
                html = self.get_html(params={'page': page})
                products.extend(self.get_content(html.text))
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
        pagination = soup.select('div.pages-list a')
        if pagination:
            return int(pagination[-1].get_text().replace('\n', ''))
        else:
            return 1

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all("li", class_="tile-container")
        
        products = []
        for item in items:
            old_price = item.find('div', class_='old-price')
            price = item.find('span', class_='hidden', text='Цена:')
            if old_price:
                old_price = old_price.get_text().replace('₸', '')
            else:
                old_price = 'Скидки нет'
            if price:
                price = price.find_next('span').get_text().replace('₸', '')
            else:
                price = 'Нет в наличии'
            products.append({
                'title': item.find('h3', class_='title').get_text(strip=TRUE).replace('\n', ''),
                'price': price,
                'old price' : old_price,
            })    
        return products