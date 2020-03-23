#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Fetch covid-19 data from the SH server (see URL below).
Version: 1.1
Python 3.7+
Date created: 20.03.2020

Fetch SH Geo Data with:
(area["ISO3166-2"="DE-SH"];)->.sh;
rel["boundary"="administrative"]["admin_level"="6"](area.sh)->.landkreise;
node(r.landkreise);
out;
.landkreise out;

"""

# import re
# import urllib.request
# import demjson
import json
import requests
from bs4 import BeautifulSoup

URL = 'https://www.schleswig-holstein.de/DE/Landesregierung/I/Presse/_documents/Corona-Liste_Kreise.html'
# URL = 'http://192.168.170.4/sh-example.html'  # testing only

with open('sh_data.json', 'r') as fd:
    counties = json.load(fd)

# Fetch and parse website data
req_url_sh = requests.get(URL).content
soup_url_sh = BeautifulSoup(req_url_sh, 'html.parser')
data = soup_url_sh.select_one('div[class="bodyText"]')

# Find the date
table_head = data.find('thead')

timestamp = None

for row in table_head:
    cells = row.findAll('th')
    timestamp = cells[2].get_text()

# Find table cells
table_body = data.find('tbody')
rows = table_body.findAll('tr')

cells = None

areas = []
changes = []
values = []

for row in rows:
    cells = row.findAll('td')
    areas.append(cells[0].get_text())
    changes.append(cells[1].get_text())
    values.append(cells[2].get_text())

sick_sum = values[-1]

area_values = dict(zip(areas, values))
# print(area_values)

container = []

for county in counties['counties']:
    props = county['properties']
    # print(props)  # -> logging

    infection = 0
    names = []

    # Add counties to the names list
    names.append(props['name'])

    county_name = props['name']
    if county_name in area_values:
        infection += int(area_values[county_name])

    pos = props['coordinates']
    # print(pos)

    container.append({
        "name": " & ".join(names),
        "sick": infection,
        "lng": pos[0],
        "lat": pos[1]
    })

sh_data = {
    "source": URL,
    "timestamp": timestamp,
    "infection_sum": sick_sum,
    "entries": container
}

with open("data.json", "w+") as fd:
    json.dump(sh_data, fd, indent=2)
