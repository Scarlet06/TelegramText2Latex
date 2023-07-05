import requests
from bs4 import BeautifulSoup
from json import dump

scrape = requests.get(r'https://www.loc.gov/marc/specifications/codetables/Subscripts.html')

soup = BeautifulSoup(scrape.content, 'html.parser')

table = soup.find('table',{'summary':'marc code tables'}).find('tbody').find_all('tr')
zipped = zip()
sub = {}
sub.update(dict(zip('()+-0123456789',map(lambda el: (el.find_all('td')[3].text),table[1:]))))

greek = 'ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓᵦᵧᵨᵩᵪ'
gkey = (
    'a',
    'e',
    'h',
    'i',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'r',
    's',
    't',
    'u',
    'v',
    'x'
    r'\beta',
    r'\gamma',
    r'\rho',
    r'\psi',
    r'\chi',
)
sub.update(dict(zip(gkey,greek)))

with open('sub.json','w',encoding='utf-8') as f:
    dump(sub,f,indent=2)