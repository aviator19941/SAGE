import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil import rrule
from datetime import datetime

website_url = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight').text

soup = BeautifulSoup(website_url,'lxml')

my_table = soup.find('table', {'class': 'wikitable collapsible'})

rows = my_table.find_all('tr')


dates = []
orbital_dict = {}
# init dict with 365 days in ISO 8601 format year 2019

a = '20190101+0000'
b = '20191231+0000'

for dt in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(a, '%Y%m%d%z'), until=datetime.strptime(b, '%Y%m%d%z')):
	date = dt.isoformat()
	if date not in orbital_dict:
   		orbital_dict[date] = 0

for row_num in range(len(rows)):
	cols=rows[row_num].find_all('td')
	cols=[x.text.strip() for x in cols]
	if len(cols) == 5:
		full_date = cols[0]
		date_without_time = "".join(re.findall(r'\d+\s[A-Za-z]*', full_date)) + ' 2019+0000'
		date = datetime.strptime(date_without_time, '%d %B %Y%z').isoformat()
	if len(cols) == 6 and date:
		cols.append(date)
		if cols[5] == 'Successful' or cols[5] == 'Operational' or cols[5] == 'En Route':
			orbital_dict[date] += 1

# dump dict into csv
import csv
csv_file = "test.csv"
try:
	with open(csv_file, 'w') as f:
		f.write("date, value\n")
		for key in orbital_dict.keys():
			f.write("%s, %s\n"%(key,orbital_dict[key]))
except IOError:
	print("I/O error")
