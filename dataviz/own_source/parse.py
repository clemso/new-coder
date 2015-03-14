import csv

MY_FILE = "../data/sample_sfpd_incident_all.csv"


def parse(raw_file, delimiter):
    """
    Parse a raw CSV file to a JSON-line object
    """
    # Open CSV File
    with open(raw_file) as f:
        # Read CSV File
        csv_data = csv.reader(f, delimiter=delimiter)
        # Close CSV File

        # Build data Structure for parsed_data
        parsed_data = []

        fields = csv_data.next()
        for row in csv_data:
            parsed_data.append(dict(zip(fields, row)))

    return parsed_data


def main():
    new_data = parse(MY_FILE, ",")


main()
