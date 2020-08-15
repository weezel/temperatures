# Temperatures plotter

## Description
My preferred way to measure and graph temperatures.
Works for me (tm).

In this particular case, I use ESP8266 hardware with DS18B20s attached
temperature sensor.

Temperature values are logged in the database and plotted from that data.

### Hardware
* Adafruit Feather Huzzah (ESP8266)
* Dallas Temperature sensors (DS18B20s)

Huzzah is running a web server and query returns a current temperature in
celsius.


## Rationale

* KISS (Keep It Simple Stupid)

* ELK and Prometheus + Grafana are a tad overkill for my needs

* Easy to deploy (what's easy then, eh?)


## Requirements

* Something that generates data (here: temperature sensor)

* Python 3

* Moreover, see `requirements.txt`


## Installation and configuration

	mkdir -p $HOME/apps/temperatures && python3 -m venv $HOME/apps/temperatures

	cd $_ && . bin/activate

	pip3 install -r requirements.txt

	./plotting.py temperatures.conf

## Caveats

Graph colors are a bit turdy.
I really wanted to have all the plots in the same figure and only occasionally
give attention to air pressure.
That's why air pressure has so diluted color.

