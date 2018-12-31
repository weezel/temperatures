# Temperatures

## Description
My preferred way to measure and graph temperatures.
Works for me (tm).

In this particular case, I use ESP8266 hardware with DS18B20s attached
temperature sensor.

Temperature values are logged in the text file and later a graph is generated
from that data.


## Setup
* Adafruit Feather Huzzah (ESP8266)
* Dallas Temperature sensors (DS18B20s)

Huzzah is running a web server and query returns a current temperature in
celsius.
Will publish the source at some point.

I'm using this ad-hoc oneliner script to collect data in to the text file:

	while true; do curl -s http://remote-temp-server |awk -v date="$(date +"%Y-%m-%d_%H:%M")" '/Temperature/ {print date, $2}' >>temperatures.txt; sleep 60; done

It's in my endless TODO list to substitute that with something more convenient.


## Rationale

* KISS (Keep It Simple Stupid)

* Avoid useless use of services (i.e. ELK)

* "One script to run it all"


## Requirements

* Something that generates data (here: temperatures)

* Python 2.7 (Some library didn't work with Python 3.x)


## Installation
Change file paths in `temperatures.py` (yes, I should parameterize those).
Execute:

	virtualenv temperatures

	cd temperatures && . bin/activate

	pip install -r requirements.txt

	./temperatures.py

