from bs4 import BeautifulSoup
import requests
import unicodedata

url = "https://juvenes.fi/newton/"
data = requests.get(url)

html = BeautifulSoup(data.text, 'html.parser')
info = html.select('div.aukiolo-rivi')

text = []
for i in info:
    i = unicodedata.normalize('NFKD', i.get_text())
    breakpoint()
    text.append(i)
print(text)
