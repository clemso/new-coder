class GiantbombAPT(object):
    # we want to get platform data, this is the url specified by API
    base_url = "http://www.giantbomb.com/api/platforms/"

    def __init__(self, api_key):
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
