import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from numpy.core._multiarray_umath import array

from optimus.helpers.functions import ellipsis
from optimus.helpers.output import output_image, output_base64


def plot_scatterplot(column_data=None, output=None, path=None):
    """
    Boxplot
    :param column_data: column data in json format
    :param output: image or base64
    :param path:
    :return:
    """

    fig = plt.figure(figsize=(12, 5))
    plt.scatter(column_data["x"]["data"], column_data["y"]["data"], s=column_data["s"], alpha=0.5)
    plt.xlabel(column_data["x"]["name"])
    plt.ylabel(column_data["y"]["name"])

    # Tweak spacing to prevent clipping of tick-labels
    # plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.3)

    # Save as base64
    if output is "base64":
        return output_base64(fig)
    elif output is "image":
        return output_image(path)


def plot_boxplot(column_data=None, output=None, path=None):
    """
    Boxplot
    :param column_data: column data in json format
    :param output: image or base64
    :param path:
    :return:
    """
    for col_name, stats in column_data.items():
        fig, axes = plt.subplots(1, 1)

        bp = axes.bxp(stats, patch_artist=True)

        axes.set_title(col_name)
        plt.figure(figsize=(12, 5))

        # 'fliers', 'means', 'medians', 'caps'
        for element in ['boxes', 'whiskers']:
            plt.setp(bp[element], color='#1f77b4')

        for patch in bp['boxes']:
            patch.set(facecolor='white')

            # Tweak spacing to prevent clipping of tick-labels

        # Save as base64
        if output is "base64":
            return output_base64(fig)
        elif output is "image":
            return output_image(path)
        else:
            plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.3)


def plot_freq(column_data=None, output=None, path=None):
    """
    Frequency plot
    :param column_data: column data in json format
    :param output: image or base64
    :param path:
    :return:
    """
    for col_name, data in column_data.items():

        # Transform Optimus' format to matplotlib's format
        x = []
        h = []

        for d in data:
            x.append(ellipsis(d["value"]))
            h.append(d["count"])

        # Plot
        fig = plt.figure(figsize=(12, 5))

        # Need to to this to plot string labels on x
        x_i = range(len(x))
        plt.bar(x_i, h)
        plt.xticks(x_i, x)

        plt.title("Frequency '" + col_name + "'")

        plt.xticks(rotation=45, ha="right")

        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.3)

        # Save as base64
        if output is "base64":
            return output_base64(fig)
        elif output is "image":
            return output_image(path)


def plot_missing_values(column_data=None, output=None):
    """
    Plot missing values
    :param column_data:
    :param output: image o base64
    :return:
    """
    values = []
    columns = []
    labels = []
    for col_name, data in column_data["data"].items():
        values.append(data["missing"])
        columns.append(col_name)
        labels.append(data["%"])

    # Plot
    fig = plt.figure(figsize=(12, 5))
    plt.bar(columns, values)
    plt.xticks(columns, columns)

    # Highest limit
    highest = column_data["count"]
    plt.ylim(0, 1.05 * highest)
    plt.title("Missing Values")
    i = 0
    for label, val in zip(labels, values):
        plt.text(x=i - 0.5, y=val + (highest * 0.05), s="{}({})".format(val, label))
        i = i + 1

    plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.3)

    # Save as base64
    if output is "base64":
        return output_base64(fig)


def plot_hist(column_data=None, output=None, sub_title="", path=None):
    """
    Plot a histogram
    obj = {"col_name":[{'lower': -87.36666870117188, 'upper': -70.51333465576172, 'value': 0},
    {'lower': -70.51333465576172, 'upper': -53.66000061035157, 'value': 22094},
    {'lower': -53.66000061035157, 'upper': -36.80666656494141, 'value': 2},
    ...
    ]}
    :param column_data: column data in json format
    :param output: image or base64
    :param sub_title: plot subtitle
    :param path:
    :return: plot, image or base64
    """

    for col_name, data in column_data.items():
        bins = []
        for d in data:
            bins.append(d['lower'])

        last = data[len(data) - 1]["upper"]
        bins.append(last)

        # Transform hist Optimus format to matplot lib format
        hist = []
        for d in data:
            if d is not None:
                hist.append(d["count"])

        bins = array(bins)
        center = (bins[:-1] + bins[1:]) / 2
        width = 0.9 * (bins[1] - bins[0])

        # Plot
        fig = plt.figure(figsize=(12, 5))
        plt.bar(center, hist, width=width)
        plt.title("Histogram '" + col_name + "' " + sub_title)

        plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.3)

        # Save as base64
        if output is "base64":
            return output_base64(fig)
        elif output is "image":
            return output_image(path)


def plot_correlation(column_data, output=None, path=None):
    """
    Plot a correlation plot
    :param column_data:
    :return:
    """
    return sns.heatmap(column_data, mask=np.zeros_like(column_data, dtype=np.bool),
                       cmap=sns.diverging_palette(220, 10, as_cmap=True))