from __future__ import print_function
import requests
import sys
from api_key import API_KEY

CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'

class CPIData(object):
    """
    Abstraction of the CPI data provided by FRED.
    Storing one Value per year.
    """

    def __init__(self):
        self.year_cpi = {}
        self.last_year = None
        self.first_year = None


    def load_from_url(self, url, save_as_file = None):
        """
        Loads Data from give URL. Data ca be saved with save as Parameter to a file.

        """
        # The file is not loaded at once into Memory, because we don't know how big it wil be
        stream = requests.get(url, stream=True, headers={"Accept-Encoding": None}).raw


        if save_as_file is None:
            # Pass raw Data Object
            return self.load_from_file(stream)
        else:
            # Save data to file
            with open(save_as_file, "w") as out:
                # Byteweise reading from stream
                while True:
                    buffer = stream.read(81920)
                    if not buffer:
                        break
                    out.write(buffer)
            # Pass file Object from disk
            with open(save_as_file) as f:
                return self.load_from_file(f)




    def load_from_file(self, fp):
        """
        Loads CPI data from a given file-like object
        """
        last_year = None
        year_cpi = []
        reached_dataset = False
        for line in fp:
            # find beginning of data

            # skip until the line after "DATE"
            if line.startswith("DATE "):
                reached_dataset = True
                continue

            if reached_dataset:
                # extract data
                data = line.rstrip().split()
                year = int(data[0].split("-")[0])
                cpi = float(data[1])


                if last_year != year:
                    # we reached a new year
                    if last_year is not None:
                        # we are not in the first round, save the average for the last year
                        self.year_cpi[last_year] = sum(year_cpi) / len(year_cpi)
                    # update which one was the last year
                    last_year = year
                    # reset our year cpi
                    year_cpi = []

                # same year as last year, collect cpi data
                year_cpi.append(cpi)

                # set first year in first round
                if self.first_year is None:
                    self.first_year = year

                # last year always carries the current year
                self.last_year = year

            # save the average of the last year we didnt catch in the loop
            if last_year is not None and last_year not in self.year_cpi:
                self.year_cpi[last_year] = sum(year_cpi) / len(year_cpi)


    def get_adjusted_price(self, price, year, current_year = None):
        """
        Returns the adapted price from a given year compared to what current year has been specified.
        """
        if current_year is None or current_year > 2014:
            # sys.stderr.write("There is no Data for above 2014, adjusting to 2014")
            current_year = 2014
        if year < self.first_year:
            year = self.first_year
        elif year > self.last_year:
            year = self.last_year
        year_cpi = self.year_cpi[year]
        current_cpi = self.year[current_year]
        # calculate how the current cpi has changed to the given year cpi
        adjustment = float(current_cpi) / float(year_cpi)
        # price which an item would have at current year
        return float(price) * adjustment

class GiatnbombAPT(object):
    base_url = "http://www.giantbomb.com/api"


def main():
    """
    This function handles the actual logic of this script
    """
    # Grab CPI/Inflation data


    # Grab ABO/game platform data

    # Figure out current price of each platform
    # by looping though each game platform and
    # calculate the adjusted price based on the CPI data.
    # Vaildate Data in the loop too.

    # Generate a Plot for the adjusted Price

    # Save Data to CSV file
