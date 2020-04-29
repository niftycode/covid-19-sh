# covid-19-sh

**Update**: The website showing the infections in [Schleswig-Holstein](https://en.wikipedia.org/wiki/Schleswig-Holstein) is no longer available. So, this script will stop with a Traceback. But anyone interested in [web scraping](https://en.wikipedia.org/wiki/Web_scraping) might this code useful.

Visualize Covid-19 infections in the German State of Schleswig-Holstein, inspired by the [Hackerspace Pfaffenhofen](https://github.com/hopfenspace/corona.bayern).

~~Website: https://xern.de/covid-19-schleswig-holstein/~~

## Requirements

* Python 3
* requests
* beautifulsoup4

Use

    $ pip3 install -r requirements.txt

to install these packages.

## About

Run the script with:

    $ python3 prepare_data.py

This will fetch the number of infections in [Schleswig-Holstein](https://en.wikipedia.org/wiki/Schleswig-Holstein) ~~from [this website](https://www.schleswig-holstein.de/DE/Landesregierung/I/Presse/_documents/Corona-Liste_Kreise.html)~~.
