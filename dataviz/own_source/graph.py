from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from parse import *


def visulize_days(parsed_data):
    """
    Visualize data by day of week
    """
    counter = Counter(item["DayOfWeek"] for item in parsed_data)
    data_list = [
        counter["Monday"],
        counter["Tuesday"],
        counter["Wednesday"],
        counter["Thursday"],
        counter["Friday"],
        counter["Saturday"],
        counter["Sunday"]
    ]
    labels = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    # y-axis data
    plt.plot(data_list)
    # tell plt how many ticks to place and how to label them
    plt.xticks(range(len(labels)), labels)
    plt.savefig("Days.png")
    plt.clf()


def visulize_type(parsed_data):
    """
    Visulize data by category in a bar graph
    """
    counter = Counter(item["Category"] for item in parsed_data)

    labels = counter.keys()

    # width of each bar
    width = 0.5
    xlocations = np.arange(len(labels)) + width

    # The location of the Bars left edges
    plt.bar(xlocations, counter.values(), width = width)

    # the labels should be at the half of each bar
    plt.xticks(xlocations + width / 2, labels, rotation = 90)

    plt.subplots_adjust(bottom=0.4)

    # plt.rcParams['figure.figsize'] = 12, 20
    plt.savefig("Type.png")
    plt.clf()



def main():
    data = parse(MY_FILE, ",")
    visulize_days(data)
    visulize_type(data)


if __name__ == '__main__':
    main()





