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
text in superscript text. It uses loc.gov and rupertshepherd tables"""

import requests
from bs4 import BeautifulSoup
from json import dump

# extracting the table from loc.gov after looking their html structure.
scrape = requests.get(r'https://www.loc.gov/marc/specifications/codetables/Superscripts.html')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.find('table',{'summary':'marc code tables'}).find('tbody').find_all('tr')

# extracting the data from the table into a dictionary that will be saved in
# an external file.
super = dict(
    zip(
        '()+-0123456789',
        map(
            lambda el: (el.find_all('td')[3].text),
            table[1:]
        )
    )
)

# extracting the table from loc.gov after looking their html structure.
scrape = requests.get(r'https://rupertshepherd.info/resource_pages/superscript-letters-in-unicode')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.find('table').find('tbody').find_all('tr')

# extracting the data from the table into the same dictionary that will be saved in
# an external file. Some greek characters are added manually.
super.update(
    {
        row.contents[0].next.text:row.contents[2].text.strip()
        for row in table
        if row.contents[2].text.strip()
    }
)
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
    r'\chi'
)
super.update(zip(gkey,greek))

with open('super.json','w',encoding='utf-8') as f:
    dump(super,f,indent=2)