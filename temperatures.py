#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = '/home/weezel/apps/temperatures/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import datetime
from itertools import groupby
from collections import OrderedDict

import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator


class DateTemp(object):
    def __init__(self, date, temperature):
        self.date = date
        self.temperature = temperature

    def __repr__(self):
        return "%s %s°C" % (self.date, self.temperature)

def parse_date(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d_%H:%M")

def all_time(date_temp_list=[]):
    if len(date_temp_list) < 1:
        print("Zero length date_temp_list in all_time() function")
        return

    days_avg = groupby(date_temp_list, \
            key=lambda x: x.date.strftime("%Y-%m-%d"))
    d = OrderedDict()
    for i in days_avg:
        day_all = [t.temperature for t in i[1]]
        day_avg = round(sum(day_all) / float(len(day_all)), 2)
        d[i[0]] = day_avg

    days = mdates.date2num([datetime.datetime.strptime(i, "%Y-%m-%d") \
                            for i in d.keys()])
    plt.figure(1)
    plt.plot_date(days, d.values(), fmt="r-", tz=None, xdate=True)
    plt.xticks(rotation="vertical")
    plt.tight_layout()
    plt.grid()
    plt.savefig("/var/www/htdocs/temperature/all_days.png")

def n_days(date_temp_list=[], default_days=1):
    if len(date_temp_list) < 1:
        print("Zero length date_temp_list in n_days() function")
        return

    minus_days = datetime.datetime.now() - datetime.timedelta(days=default_days)
    n_day_items = [val for i, val in enumerate(date_temp_list) if val.date >= minus_days and i % 10 == 0]
    n1date = mdates.date2num([i.date for i in n_day_items])
    plt.figure(2)
    plt.plot_date(n1date, [i.temperature for i in n_day_items], fmt="r-", tz=None, xdate=True)
    plt.xticks(rotation="vertical")
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=30))
    plt.tight_layout()
    plt.grid()
    plt.savefig("/var/www/htdocs/temperature/ndays.png")

def init():
    with open("/home/weezel/temperatures.txt", "r") as f:
        date_temp_list = list()

        for line in f.readlines():
            splt = line.rstrip("\n").split(" ")

            date = parse_date(splt[0])
            temperature = float(splt[1])
            dt = DateTemp(date, temperature)
            date_temp_list.append(dt)
        return date_temp_list

if __name__ == '__main__':
    date_temps = init()

    n_days(date_temps, 3)
    all_time(date_temps)
