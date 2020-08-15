#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import sys
import time

import requests

import external


def retrieve_values(url: str, room: str) -> dict:
    logging.info(f"Retrieving stats for {room}")
    try:
        values = requests.get(url)
        doc = values.content.decode("utf-8").split("\n")
        temp_degC, humidity, pressure = \
            [i.split(";") for i in doc if "degC" in i][0]
        temp_degC = float(temp_degC.split(" ")[0])
        humidity = float(humidity.rstrip("%"))
        pressure = float(pressure.split(" ")[0])

        room_stats = f"{room}: " \
                     f"{temp_degC}degC " \
                     f"{humidity}% " \
                     f"{pressure}hPa"
        logging.info(room_stats)

        return {
            room: {
                "temperature": temp_degC,
                "humidity": humidity,
                "pressure": pressure
            }
        }
    except Exception as e:
        logging.error(f"Couldn't retrieve temperature for {room}: {e}")


def time_now():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())


def create_db_schema(cur: sqlite3.Cursor, room_name: str):
    c = f"CREATE TABLE IF NOT EXISTS {room_name} (" \
        "datetime TEXT," \
        "temperature REAL," \
        "humidity REAL," \
        "pressure REAL);"
    cur.execute(c)


def main(argv: list) -> None:
    conf_abs_path = os.path.abspath(argv[1])
    if not os.path.exists(conf_abs_path):
        logging.error("Failed to load config file")
        sys.exit(1)
    app_dir = os.path.dirname(conf_abs_path)

    logging.basicConfig(filename=os.path.join(app_dir, "temperatures.log"),
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(asctime)s %(levelname)s: %(message)s",
                        level=logging.INFO)

    config = external.read_config_file(conf_abs_path)

    configured_rooms = config["rooms"]

    with sqlite3.connect(os.path.join(app_dir, "temperatures.db")) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        for room, url in configured_rooms.items():
            room_stats = retrieve_values(url, room)

            room_name = " ".join(room_stats.keys()).rstrip(" ")
            create_db_schema(cur, room_name)
            conn.commit()

            q = f"INSERT OR IGNORE INTO {room_name} " \
                "(datetime, temperature, humidity, pressure) " \
                "VALUES (?, ?, ?, ?);"
            logging.info("Adding values to DB")
            cur.execute(q, [time_now(),
                            room_stats[room_name]["temperature"],
                            room_stats[room_name]["humidity"],
                            room_stats[room_name]["pressure"]])
            logging.info("Done")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"ERROR: {sys.argv[0]}: give configuration as an argument")
        sys.exit(1)

    main(sys.argv)
