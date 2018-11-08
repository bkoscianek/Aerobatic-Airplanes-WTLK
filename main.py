import bs4
import requests as req
import re
import pandas as pd

reg = r'[( ][0-9]{4}'
r = req.get("https://en.wikipedia.org/wiki/List_of_aerobatic_aircraft")

soup = bs4.BeautifulSoup(r.content, 'html.parser')
airplanes_names = []
airplanes_links = []
airplanes_dates = []

soup = soup.find('div', class_="mw-parser-output")
for airplane in soup.find_all('li'):
	airplane = airplane.contents
	name = airplane[0].string

	date = ""
	if len(airplane) != 1:
		date = airplane[1]
		date = str(date)
	date = re.search(reg, date)

	if date is not None:
		airplanes_names.append(name)
		airplanes_links.append(airplane[0].get('href'))
		d = date[0]
		airplanes_dates.append(int(d[1:len(d)]))


data = pd.DataFrame({'names': airplanes_names, 'links': airplanes_links, 'built': airplanes_dates})
data = data.sort_values(by=['built'], ascending=True)
data = data[data.built >= 1970]

print(data)