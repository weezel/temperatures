import configparser
import logging


def read_config_file(filename: str) -> configparser.ConfigParser:
    confparser = configparser.ConfigParser()
    must_contain = ["general", "rooms"]

    confparser.read(filename)

    if not all(section in must_contain
               for section in confparser.sections()):
        logmsg = f"Failed to load config. Sections found: {confparser.sections()}" \
                    "Must have sections: {}".format(" ".join(must_contain))
        logging.info(logmsg)
        print(logmsg)
    return confparser
