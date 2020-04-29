#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Fetch covid-19 data from the SH server (see URL below).
Version: 1.2
Python 3.7+
Date created: 20.03.2020
Website: https://xern.de/covid-19-schleswig-holstein/

Fetch SH Geo Data by running the following query
on overpass-turbo.eu and export the result as GeoJSON:

(area["ISO3166-2"="DE-SH"];)->.sh;
rel["boundary"="administrative"]["admin_level"="6"](area.sh)->.landkreise;
node(r.landkreise);
out;
.landkreise out;

"""

import logging
import sys
import json
import requests
from bs4 import BeautifulSoup

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename='info.log', level=logging.DEBUG, format=LOG_FORMAT)

logger = logging.getLogger()
logger.info("logger messages")

URL = 'https://www.schleswig-holstein.de/DE/Landesregierung/I/Presse/_documents/Corona-Liste_Kreise.html'

try:
    with open('sh_data.json', 'r') as fd:
        counties = json.load(fd)
except OSError as e:
    print(e)
    sys.exit("Quit the script!")

# Fetch and parse website data
req_url_sh = requests.get(URL).content
soup_url_sh = BeautifulSoup(req_url_sh, 'html.parser')
data = soup_url_sh.select_one('div[class="bodyText"]')

# Find the date
table_head = data.find('thead')

timestamp = None

for row in table_head:
    cells = row.findAll('th')
    logger.debug(cells)
    timestamp = cells[1].get_text()

logger.debug(timestamp)

# Find table cells (counties, changes, infections)
table_body = data.find('tbody')
rows = table_body.findAll('tr')
logger.debug(rows)

cells = None

areas = []
changes = []
values = []

for row in rows:
    cells = row.findAll('td')
    areas.append(cells[0].get_text())
    # changes.append(cells[1].get_text())
    values.append(cells[1].get_text())

sick_sum = values[-1]

area_values = dict(zip(areas, values))
logger.debug(area_values)

container = []

for county in counties['counties']:
    props = county['properties']
    logger.debug(props)

    infection = 0
    names = []

    # Add counties to the names list
    names.append(props['name'])

    county_name = props['name']
    if county_name in area_values:
        infection += int(area_values[county_name])

    pos = props['coordinates']

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

try:
    with open("data.json", "w+") as fd:
        json.dump(sh_data, fd, indent=2)
except OSError as e:
    print(e)
    sys.exit("Quit the script!")
