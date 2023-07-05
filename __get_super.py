import requests
from bs4 import BeautifulSoup
from json import dump

#numbers
scrape = requests.get(r'https://www.loc.gov/marc/specifications/codetables/Superscripts.html')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.find('table',{'summary':'marc code tables'}).find('tbody').find_all('tr')

super = dict(zip('()+-0123456789',map(lambda el: (el.find_all('td')[3].text),table[1:])))

#letters
scrape = requests.get(r'https://rupertshepherd.info/resource_pages/superscript-letters-in-unicode')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.find('table').find('tbody').find_all('tr')

super.update({row.contents[0].next.text:row.contents[2].text.strip() for row in table if row.contents[2].text.strip()})
#manual check to solve errors
greek = 'ᵅᵝᵞᵟᵋᶿᶥᶲᵠᵡ'
gkey = (
    r'\alpha',
    r'\beta',
    r'\gamma',
    r'\delta',
    r'\epsilon',
    r'\theta',
    r'\iota',
    r'\psi',
    r'\varpsi',
    r'\chi',
)
super.update(dict(zip(gkey,greek)))

with open('super.json','w',encoding='utf-8') as f:
    dump(super,f,indent=2)