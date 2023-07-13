# This file is part of TelegramText2Latex.

# TelegramText2Latex is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TelegramText2Latex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with TelegramText2Latex.  If not, see <http://www.gnu.org/licenses/>.
"""This file is used to extract automatically the needed character to change
text in subscript text. It uses loc.gov table"""

import requests
from bs4 import BeautifulSoup
from json import dump

# extracting the table from loc.gov after looking their html structure.
scrape = requests.get(r'https://www.loc.gov/marc/specifications/codetables/Subscripts.html')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.find('table',{'summary':'marc code tables'}).find('tbody').find_all('tr')

# extracting the data from the table into a dictionary that will be saved in
# an external file. Some alphabet and greek characters are added manually.
sub = dict(
    zip(
        '()+-0123456789',
        map(
            lambda el: (el.find_all('td')[3].text),
            table[1:]
        )
    )
)
val = 'ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓᵦᵧᵨᵩᵪ'
key = (
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
    'x',
    r'\beta',
    r'\gamma',
    r'\rho',
    r'\psi',
    r'\chi'
)
sub.update(zip(key,val))
with open('sub.json','w',encoding='utf-8') as f:
    dump(sub,f,indent=2)