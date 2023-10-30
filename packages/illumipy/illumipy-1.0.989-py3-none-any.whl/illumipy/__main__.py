#!/usr/bin/env python3
"""
__main__ module for running from cli
"""

import logging
import argparse
import sys
from sys import stderr
from .data import light_data
from .defaults import CITY_DEFAULT, COUNTRY_DEFAULT, API_KEY_DEFAULT

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(
        description='General-purpose solar brightness calculator.'
        )
    argParser.add_argument(
        "-t", "--time",
        default=None,
        help="Time of the day in hours (0-24, e.g. 4 or 12). \
            Defaults to current time if not specified."
        )
    argParser.add_argument(
        "-d",
        "--date",
        default=None,
        help="Date as YYYY-MM-DD (e. g. 2023-06-01). \
            Defaults to current date if not specified."
        )
    argParser.add_argument(
        "-c", "--city",
        default=CITY_DEFAULT,
        help="City name (e. g. Berlin). \
            Defaults to {CITY_DEFAULT} if not specified."
        )
    argParser.add_argument(
        "-C",
        "--Country",
        default=COUNTRY_DEFAULT,
        help="Country name (e. g. Germany). \
            Defaults to {COUNTRY_DEFAULT} if not specified."
        )
    argParser.add_argument(
        "-a",
        "--api",
        default=API_KEY_DEFAULT,
        help="OpeWeather API-Key (required). \
            Alternatively, a default API key can be defined in main.py"
        )
    argParser.add_argument(
        "-o",
        "--output",
        default=['Illuminance'],
        help="Define the parameters to be returned. \
            Defaults to 'Illuminance' if not specified.\
                    To see available values try illumipy\
                        [-o|--output] [-h|--help]",
        nargs='+',
        )
    argParser.add_argument(
        '-D', '--debug',
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    argParser.add_argument(
        '-v',
        '--verbose',
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    argParser.add_argument(
        "-A",
        "--all",
        help="Print out entire dataset. Default is just the Illuminance in Lux",
        action="store_true",
        default=False,
        )

    args = argParser.parse_args()

    LOG_FORMAT = '[%(levelname)s]:  \t%(module)s.%(funcName)s() \
        (Ln. %(lineno)d):\n\t\t\t>>> %(message)s\n'
    logging.basicConfig(level=args.loglevel, format=LOG_FORMAT)

    time_arg = args.time
    date_arg = args.date
    city_arg = args.city
    country_arg = args.Country
    api_arg = args.api
    print_all = args.all
    output_arg = args.output
  
    args_debug = f"time={time_arg}, date={date_arg}, city={city_arg},\
        country={country_arg}, api_key={api_arg}"
    logging.info('Calling main function in main.py')
    logging.debug('Using these args: %s', args_debug)

    try:
        brightness = light_data(time=time_arg,
                        date=date_arg,
                        city=city_arg,
                        country=country_arg,
                        api_key=api_arg)
        if print_all is True:
            dataset = brightness.keys()
        else:
            dataset = output_arg._get_kwargs()
        for item in dataset
                print(f"{item}: {brightness[item]}\n")
            
        else:
            dataset = brightness['illuminance']
        print(dataset)
    except KeyboardInterrupt:
        stderr.write("Interrupted by User, exiting...\n")
        sys.exit(1)
