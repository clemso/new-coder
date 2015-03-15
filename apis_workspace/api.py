from __future__ import print_function
import logging
import requests
import sys
import matplotlib.pyplot as plt
import numpy as np
from api_key import API_KEY
import tablib


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

class GiantbombAPT(object):
    # we want to get platform data, this is the url specified by API
    base_url = "http://www.giantbomb.com/api/platforms/"

    def __init__(self, api_key = None):
        if api_key is None:
            self.api_key = API_KEY
        else:
            self.api_key = api_key

    def get_platforms(self, sort=None, filter=None, field_list = None):
        # constructing the params dict for get request
        # depending which arguments are given
        params = {}
        # the keys are the field names of the API for /platforms
        # the values have to be constructed like in the docs
        # http://www.giantbomb.com/api/documentation
        if sort is not None:
            params["sort"] = sort
        if field_list is not None:
            params["field_list"] = ",".join(field_list)
        if filter is not None:
            parsed_filters = []
            for key, val in filter.iteritems():
                parsed_filters.append("{0}:{1}".format(key, val))
            params["filter"] = ",".join(parsed_filters)

        params["api_key"] = self.api_key
        params["format"] = "json"

        all_fetched = False
        num_total_results = None
        num_fetched_results = 0
        counter = 0

        while not all_fetched:
            # request limit is 100 so we have to cycle through the data,starting after our already fetched results
            params["offset"] = num_fetched_results
            # request just takes a params dict and url encode it properly
            result = requests.get(self.base_url, params = params)
            # request can transform json to python objects
            result = result.json()

            if num_total_results is None:
                # get the total number of results
                num_total_results = int(result["number_of_total_results"])
            # save the results we fetched
            num_fetched_results += int(result["number_of_page_results"])

            if num_fetched_results >= num_total_results:
                # we have reached the end of the dataset, break the loop
                all_fetched = True


            for result in result["results"]:
                # Give some information about process
                logging.debug("Yielding platform {0} of {1}".format(
                    counter + 1,
                    num_total_results
                ))
                counter += 1

                # convert the prices to floats
                if "original_price" in result and result["original_price"]:
                    result["original_price"] = float(result["original_price"])

                # we make it a generator so stopping is possible from outside
                yield result


def is_valid_dataset(platform):
    """
    Filter the dataset, which may have invalid data. We make sure all field we want to user are present
    """
    # For every field check if its there and if it contains data at all
    if 'name' not in platform or not platform['name']:
        logging.warn(u"No platform name found for given dataset")
        return False
    if "release_date" not in platform or not platform["release_date"]:
        logging.warn(u"{0} has no release date".format(platform["name"]))
        return False
    if 'original_price' not in platform or not platform['original_price']:
        logging.warn(u"{0} has no original price".format(platform['name']))
        return False
    if 'abbreviation' not in platform or not platform['abbreviation']:
        logging.warn(u"{0} has no abbreviation".format(platform['name']))
        return False

    return True


def generate_plot(platforms, output_file):
    """
    Creates a Bar Chart file for Platforms
    """
    labels = []
    values = []
    for platform in platforms:
        name = platform["name"]
        adapted_price = platform["adjusted_price"]
        price = platform["original_price"]
        if price > 2000:
            continue

        if len(name) > 15:
            name = platform["abbreviation"]

        labels.insert(0, u"{0}\n$ {1}\n$ {2}".format(name, price, round(adapted_price, 2)))
        values.insert(0, adapted_price)

    width = 0.3
    ind = np.arange(len(values))
    fig = plt.figure(figsize=(len(labels) * 1.8, 10))

    ax = fig.add_subplot(1, 1, 1)
    ax.bar(ind, values, width, align="center")

    plt.ylabel("Adjusted price")
    plt.xlabel("Year / Console")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()
    plt.grid(True)
    plt.savefig(output_file, dpi = 72)


def generate_csv(platforms, output_file):
    """
    Writes Platforms Data to CSV  output_file
    """
    dataset = tablib.Dataset(headers=["Abbreviation", "Name", "Year", "Price", "Adjusted price"])

    for p in platforms:
        dataset.append([p['abbreviation'], p['name'], p['year'],
                        p['original_price'], p['adjusted_price']])
        if isinstance(output_file, basestring):
            with open(output_file, 'w+') as fp:
                fp.write(dataset.csv)
        else:
            output_file.write(dataset.csv)



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
