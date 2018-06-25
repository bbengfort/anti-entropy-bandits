# bandit.draw
# Draws the graph for the associated topology
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 25 11:21:14 2018 -0400
#
# ID: draw.py [] benjamin@bengfort.com $

"""
Draws the graph for the associated topology
"""

##########################################################################
## Imports
##########################################################################

import argparse
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing import layout
from matplotlib.colors import to_rgba
from .serialize import read_graph, CHOICES


# Drawing Constants
LOCATION_COLORS  = {
    'Oregon': '#000000',
    'California': '#7e008f',
    'Ohio': '#1800a7',
    'Virginia': '#001cdd',
    'Canada': '#0090dd',
    'Sao Paulo': '#00aaa5',
    'Ireland': '#00a13d',
    'London': '#00bc00',
    'Paris': '#00ec00',
    'Frankfurt': '#a1ff00',
    'Mumbai': '#f3e500',
    'Singapore': '#ffa500',
    'Seoul': '#f90000',
    'Tokyo': '#d30000',
    'Sydney': '#cccccc'
}

LOCATION_CODES = {
    "Virginia": "VA",
    "Ohio": "OH",
    "California": "CA",
    "Sao Paulo": "BR",
    "London": "GB",
    "Frankfurt": "DE",
    "Seoul": "KR",
    "Sydney": "AU",
    "Tokyo": "JP",
    "Mumbai": "IN",
    "Singapore": "SG",
    "Canada": "QC",
    "Ireland": "IE",
    "Paris": "FR",
    "Oregon": "OR",
}


def font_color(node_color, dark_color='k', light_color='white', coef_choice=0):
    #Coefficients:
        # option 0: http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
        # option 1: http://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
    coef_options = [np.array((.241, .691, .068, 0)),
                    np.array((.299, .587, .114, 0))
                    ]

    coefs= coef_options[coef_choice]
    rgb = np.array(to_rgba(node_color)) * 255
    brightness = np.sqrt(np.dot(coefs, rgb**2))

    # Threshold from option 0 link; determined by trial and error.
    if brightness > 130:
        return dark_color
    return light_color


def draw_graph(G, ax=None, circular=True):
    if ax is None:
        _, ax = plt.subplots(figsize=(9,9))

    # Compute the position of the vertices
    if circular:
        pos = layout.circular_layout(G)
    else:
        pos = layout.kamada_kawai_layout(G, weight='weight')

    # Get the node data to draw nodes on
    node_sizes = []
    node_labels = {}
    label_colors = {}
    node_colors = []
    linewidths = []
    edgecolors = []

    for v, data in G.nodes(data=True):
        node_sizes.append(data.get('size', 900))
        node_labels[v] = data.get('label', LOCATION_CODES[v])

        node_color = data.get('color', LOCATION_COLORS[v])
        node_colors.append(node_color)
        label_colors[v] = font_color(node_color)

        if data.get('halo', False):
            linewidths.append(8.0)
            edgecolors.append(data.get('halo_color', '#F4D03F'))
        else:
            linewidths.append(1.0)
            edgecolors.append(node_color)

    # Draw nodes with above properties
    nx.draw_networkx_nodes(
        G, pos=pos, ax=ax, node_size=node_sizes, node_color=node_colors,
        linewidths=linewidths, edgecolors=edgecolors,
    )

    # Draw node labels by light and dark color
    for color in set(label_colors.values()):
        labels = {
            v: node_labels[v] for v, c in label_colors.items() if c==color
        }
        nx.draw_networkx_labels(
            G, pos=pos, labels=labels, font_color=color, font_size=10,
        )

    # Get edge properties to draw edges on
    edge_widths = []
    edge_colors = []

    for src, dst, data in G.edges(data=True):
        edge_widths.append(data.get('size', 1.0))
        edge_colors.append(data.get('color', 'k'))

    nx.draw_networkx_edges(
        G, pos=pos, ax=ax, width=edge_widths, edge_color=edge_colors
    )


    # Remove grid and axes
    ax.grid(False)
    ax.axis('off')

    return ax


##########################################################################
## Main
##########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="draw a graph from a topology file"
    )

    parser.add_argument('-f', '--format', choices=CHOICES, default='json', help='graph serialization format')
    parser.add_argument('topology', nargs=1, help='serialized network topology')

    # Parse args and load the graph
    args = parser.parse_args()
    G = read_graph(args.topology[0])

    ax = draw_graph(G)
    plt.show()
