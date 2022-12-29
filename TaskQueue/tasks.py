import requests
from bs4 import BeautifulSoup
import datetime

def collect_news_data():
    url = 'https://economictimes.indiatimes.com/markets/indexsummary/indexid-13602,exchange-50.cms'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='syn')
    texts = [div.text for div in divs]
    return texts

############################################################################################################

def get_date_csv():
    date = datetime.datetime.now().strftime("%d%m%Y")
    date = date[:4]+date[6:]
    return date

def get_date_xls():
    date = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%B")
    year = datetime.datetime.now().strftime("%Y")
    print(date+'-'+month[:3]+'-'+year)
    return date

def get_csv(url_name, file_name):
    url = url_name+get_date_csv()+'.csv'
    response = requests.get(url)
    url_content = response.content
    csv_file = open('./data/'+file_name, 'wb')
    csv_file.write(url_content)
    csv_file.close()

def get_xls(url_name, file_name):
    url = url_name+get_date_xls()+'.xls'
    response = requests.get(url)
    url_content = response.content
    xls_file = open('./data/'+file_name, 'wb')
    xls_file.write(url_content)
    xls_file.close()

# get_csv('https://www1.nseindia.com/archives/equities/corpbond/corpbond', 'corpbond.csv')