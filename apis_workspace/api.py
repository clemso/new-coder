from __future__ import print_function
import os
import argparse
import logging
import requests
import sys
import matplotlib.pyplot as plt
import numpy as np
import tablib

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
    parser.add_argument("--plot-file", dedaul = "Data.png", required = False, help = "Path to PNG file")
    parser.add_argument("--limit", type = int, help = "Number of recent Platforms to be considered")
    opts = parser.parse_args()
    return opts

def main():
    """
    This function handles the actual logic of this script
    """
    # Grab CPI/Inflation data
    pass

    # Grab ABO/game platform data

    # Figure out current price of each platform
    # by looping though each game platform and
    # calculate the adjusted price based on the CPI data.
    # Vaildate Data in the loop too.

    # Generate a Plot for the adjusted Price

    # Save Data to CSV file
