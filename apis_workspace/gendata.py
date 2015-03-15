import numpy as np
import matplotlib.pyplot as plt
import tablib


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
    plt.close()


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
