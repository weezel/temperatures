#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import os.path
import sqlite3
import sys

import matplotlib
matplotlib.use('Agg')  # Fixes console run
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import external


class DateTemp(object):
    def __init__(self, date, temperature, humidity, pressure):
        self.date = self.parse_date(date)
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def __repr__(self) -> str:
        return "%s %s %s %s" % \
                (self.date,
                 self.temperature,
                 self.humidity,
                 self.pressure)

    @staticmethod
    def parse_date(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")


def plot_n_days(date_values: list, fileout: str, days_to_plot=1):
    if len(date_values) < 1:
        logging.error("Zero length date_value_list in n_days() function")
        return

    # TODO Use relative timedelta
    minus_days = datetime.datetime.now() - datetime.timedelta(days=days_to_plot)
    n_day_items = [val for i, val in enumerate(date_values)
                   if val.date >= minus_days]
    logging.info(f"Plotting begins from day {minus_days}")
    n1date = mdates.date2num([i.date for i in n_day_items])

    temperature_color = "tab:red"
    fig, temp_ax = plt.subplots()
    temp_ax.set_xlabel("Time")
    temp_ax.set_ylabel("Temperature", color=temperature_color)
    temp_ax.set_facecolor('#c6c6c6')
    my_date = mdates.DateFormatter("%H:%M %d-%m")
    temp_ax.xaxis.set_major_formatter(my_date)
    temp_ax.plot(n1date,
                 [i.temperature for i in n_day_items],
                 color=temperature_color)
    temp_ax.tick_params(axis="y", labelcolor=temperature_color)

    humidity_color = "#10c4e8"
    hum_ax = temp_ax.twinx()
    hum_ax.set_ylabel("Humidity", color=humidity_color)
    hum_ax.yaxis.set_label_coords(1.1, 0.25)
    hum_ax.plot(n1date,
                [i.humidity for i in n_day_items],
                color=humidity_color)
    hum_ax.tick_params(axis="y", labelcolor=humidity_color)

    pressure_color = "#b2e810"
    press_ax = temp_ax.twinx()
    press_ax.set_ylabel("Pressure", color=pressure_color)
    press_ax.yaxis.set_label_coords(1.1, 0.75)
    press_ax.plot(n1date,
                  [i.pressure for i in n_day_items],
                  color=pressure_color)
    press_ax.tick_params(axis="y", labelcolor=pressure_color)

    fig.autofmt_xdate()
    fig.tight_layout()

    plt.margins(0.2)
    plt.xticks(rotation="vertical")
    plt.grid()

    plt.savefig(fileout)
    logging.info(f"Wrote plotting out in file {fileout}")


def get_values_for(room_name: str, cwd: str) -> list:
    db_path = os.path.join(cwd, "temperatures.db")

    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        date_temp_list = list()

        q = f"SELECT datetime, temperature, humidity, pressure FROM {room_name};"
        for row in cur.execute(q):
            dt = DateTemp(row["datetime"],
                          row["temperature"],
                          row["humidity"],
                          row["pressure"])
            date_temp_list.append(dt)

    return date_temp_list


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"ERROR: {sys.argv[0]}: give configuration as an argument")
        sys.exit(1)

    conf_abs_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(conf_abs_path):
        logging.error("Failed to load config file")
        sys.exit(1)
    app_dir = os.path.dirname(conf_abs_path)

    logging.basicConfig(filename=os.path.join(app_dir, "plotting.log"),
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(asctime)s %(levelname)s: %(message)s",
                        level=logging.INFO)

    bedroom_data = get_values_for("bedroom", app_dir)

    loaded_config = external.read_config_file(conf_abs_path)

    store_directory = loaded_config["general"]["store_directory"]


    # Past two days
    plot_n_days(bedroom_data,
                os.path.join(store_directory, "days.png"),
                2)

    # Past week
    plot_n_days(bedroom_data,
                os.path.join(store_directory, "week.png"),
                7)
