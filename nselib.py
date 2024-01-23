url1 ='https://www.google.com/finance/quote/INFY:NSE'
import requests
from bs4 import BeautifulSoup
import time
response =requests.get(url1)
soup =BeautifulSoup(response.text, 'html.parser')
class1="YMlKec fxKbKc"
#soup=soup.find(class_=class1).text
price=soup.find(class_=class1).text.strip()[1:].replace(",","")

print(price)