import requests
from bs4 import BeautifulSoup
import datetime

def get_date():
    date = datetime.datetime.now().strftime("%d%m%Y")
    date = date[:4]+date[6:]
    return date

def collect_news_data():
    url = 'https://economictimes.indiatimes.com/markets/indexsummary/indexid-13602,exchange-50.cms'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='syn')
    texts = [div.text for div in divs]
    return texts

def get_csv():
    url = 'https://www1.nseindia.com/archives/equities/corpbond/corpbond'+get_date()+'.csv'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

get_csv()