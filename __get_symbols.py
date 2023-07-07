import requests
from bs4 import BeautifulSoup
from json import dump

scrape = requests.get(r'https://www.mathworks.com/help/matlab/creating_plots/greek-letters-and-special-characters-in-graph-text.html')

soup = BeautifulSoup(scrape.content, 'html.parser')

table = soup.findAll('table',{'class':'table table-condensed'})[-1].find('tbody')

sym = {row.contents[i].text:row.contents[i+1].text for row in table for i in range(0,len(row.contents),2)}
sym[r'\varphi'] = "\u03c6"
sym[r'\inf'] = '\u221e'
with open('symbols.json','w',encoding='utf-8') as f:
    dump(sym,f,indent=2)