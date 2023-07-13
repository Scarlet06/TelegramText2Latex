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
special commands into the special characters. It uses Mathworks table"""

import requests
from bs4 import BeautifulSoup
from json import dump

# extracting the table from mathworks after looking their html structure.
scrape = requests.get(r'https://www.mathworks.com/help/matlab/creating_plots/greek-letters-and-special-characters-in-graph-text.html')
soup = BeautifulSoup(scrape.content, 'html.parser')
table = soup.findAll('table',{'class':'table table-condensed'})[-1].find('tbody')

# extracting the data from the table into a dictionary that will be saved in
# an external file. Two special characters are added manually.
sym = {
    row.contents[i].text: row.contents[i+1].text
    for row in table
    for i in range(0, len(row.contents), 2)
    }
sym[r'\varphi'] = "\u03c6"
sym[r'\inf'] = '\u221e'
with open('symbols.json','w',encoding='utf-8') as f:
    dump(sym,f,indent=2)