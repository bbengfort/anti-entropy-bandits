# bandit.bilateral
# Draws a figure showing simulated bilateral anti-entropy performance.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 25 14:28:41 2018 -0400
#
# ID: bilateral.py [] benjamin@bengfort.com $

"""
Draws a figure showing simulated bilateral anti-entropy performance.
"""

##########################################################################
## Imports
##########################################################################

import csv
import math
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')
sns.set_context('notebook')


def draw_bilateral_anti_entropy(path, ax=None, interval=125):
    if ax is None:
        _, ax = plt.subplots(figsize=(9,6))


    # Draw simulated synchronization latency
    x, ym, ys = load_visibility_latency(path)
    ax.plot(x, ym, marker="o", markersize=4, label="observed synchronization", color='#3A539B')
    ax.fill_between(x, ym-ys, ym+ys, color='#3A539B', alpha=0.2)

    # Draw ideal synchronization latency
    z = interval * np.array([math.log(xi, 3) for xi in x])
    ax.plot(x, z, label="ideal synchronization", color='#26A65B')

    ax.grid(True)
    ax.set_xlim(2, 45)
    ax.legend(frameon=True, loc='upper left')
    ax.set_xlabel("system size (number of replicas)")
    ax.set_ylabel("visibility latency (milliseconds)")
    ax.set_title("Bilateral Anti-Entropy every {} milliseconds".format(interval))
    return ax


def load_visibility_latency(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        size, mean, std = [], [], []

        for row in reader:
            size.append(int(row['size']))
            mean.append(float(row['visibility latency mean']))
            std.append(float(row['visibility latency stddev']))

        return np.array(size), np.array(mean), np.array(std)


##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="draw bilateral anti-entropy performance"
    )

    parser.add_argument('-i', '--interval', type=int, default=125, help='anti-entropy delay in milliseconds')
    parser.add_argument('results', nargs=1, help='visibility latency results csv')

    args = parser.parse_args()
    draw_bilateral_anti_entropy(args.results[0], interval=args.interval)

    plt.show()
