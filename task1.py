import requests
from bs4 import BeautifulSoup

url = 'https://github.com/google'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')