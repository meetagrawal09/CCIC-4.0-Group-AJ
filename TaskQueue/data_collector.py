import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php')

soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.find_all(class_='data-element')

for element in elements:
    print(element.text)