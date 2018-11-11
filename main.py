import bs4
import requests as req
import re
import pandas as pd

prelink = "https://en.wikipedia.org"
features = ['cruise_speed', 'stall_speed', 'roll_rate', 'rate_of_climb', 'max_g_load', 'empty_weight', 'loaded_weight',
            'hp']
features_re = [r'Cruise speed: .*', r'Stall speed: .*', r'Roll rate: .*', r'Rate of climb: .*',
               r'Maximum g-load: .*|g limits: .*', r'Empty weight: .*', r'Loaded weight: .*']


def get_airplanes():
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

	data = pd.DataFrame({'name': airplanes_names, 'link': airplanes_links, 'built': airplanes_dates})
	data = data.sort_values(by=['built', 'name'], ascending=[True, True])
	data = data[data.built >= 1970]
	data = data.reset_index(drop=True)

	return data


def add_parameters(params: list, frame: pd.DataFrame):
	for arg in params:
		frame[arg] = None


def advanced_re(patterns: list, string: str):
	for pat in patterns:
		if re.search(pat, string) is not None:
			return re.search(pat, string)

	return None


airplanes = get_airplanes()
add_parameters(features, airplanes)

for ind in airplanes.index:
	url = prelink + airplanes['link'][ind]
	r = req.get(url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')
	for li in soup.find_all('li'):
		li = str(li)

