#! /usr/bin/env python

from __future__ import print_function
import os
import argparse
import logging
import requests
import sys


from api_key import API_KEY
from cpi import *
from platforms import *
from gendata import *


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-key", required = False, default = API_KEY, help = "API Key provided by Giantbomb.com")
    parser.add_argument("--cpi-file", default = os.path.join(os.path.dirname(__file__), "CPI.txt"),
                        help = "Path to file containing the CPI data")
    parser.add_argument("--cpi-data-url", default = CPI_DATA_URL, help = "URL for CPI data")
    parser.add_argument("--debug", default = False, action = "store_true",
                        help = "Increase the output level")
    parser.add_argument("--csv-file", default = "Data.csv", required = False, help = "Path to csv file")
    parser.add_argument("--plot-file", default = "Data.png", required = False, help = "Path to PNG file")
    parser.add_argument("--limit", type = int, help = "Number of recent Platforms to be considered")
    opts = parser.parse_args()
    return opts

def main():
    """
    This function handles the actual logic of this script
    """

    #Commandline Options
    opts = parse_args()
    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cpi_data = CPIData()
    gb_api = GiantbombAPI(opts.api_key)

    print("Disclaimer: This script uses data provided by FRED({0})\n and Giantbomb({1})"
          .format(CPI_DATA_URL,"http://www.giantbomb.com/api"))




    # Grab CPI/Inflation data
    if os.path.exists(opts.cpi_file):
        with open(opts.cpi_file) as fp:
            cpi_data.load_from_file(fp)
    else:
        cpi_data.load_from_url(opts.cpi_data_url,save_as_file = opts.cpi_file)


    # Grab ABO/game platform data
    platforms = []
    counter = 0


    # Figure out current price of each platform
    # by looping though each game platform and
    # calculate the adjusted price based on the CPI data.
    gb_api_gen = gb_api.get_platforms(sort="release_date:desc",
                                      field_list=["release_date",
                                                  "original_price",
                                                  "name",
                                                  "abbreviation"])
    for platform in gb_api_gen:
        if not is_valid_dataset(platform):
            continue

        year = int(platform["release_date"].split("-")[0])
        price = platform["original_price"]
        adjusted_price = cpi_data.get_adjusted_price(price, year)
        platform["year"] = year
        platform["original_price"] = price
        platform["adjusted_price"] = adjusted_price
        platforms.append(platform)

        if opts.limit is not None and counter + 1 >= opts.limit:
            break
        counter += 1

        if opts.plot_file:
            generate_plot(platforms, opts.plot_file)

        if opts.csv_file:
            generate_csv(platforms, opts.csv_file)



if __name__ == '__main__':
   main()
