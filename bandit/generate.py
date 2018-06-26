# bandit.generate
# Create a graph from a specified topology.
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 25 11:08:25 2018 -0400
#
# ID: generate.py [] benjamin@bengfort.com $

"""
Create a graph from a specified topology.
"""

##########################################################################
## Imports
##########################################################################

import csv
import argparse
import networkx as nx

from .serialize import write_graph, CHOICES


def graph_from_latency(path):
    G = nx.DiGraph(name="Network Topology")
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {key: float(row[key]) for key in ('pull', 'push', 'sync')}

            G.add_edge(row['src'], row['dst'], weight=data['sync'], **data)

    return G


##########################################################################
## Main
##########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="generate network graph from results file"
    )

    parser.add_argument('-f', '--format', choices=CHOICES, default='json', help='graph serialization format')
    parser.add_argument('-o', '--outpath', default='topology.json', help='path to write graph to')
    parser.add_argument('latency', nargs=1, help='latency.csv file from results')

    args = parser.parse_args()
    G = graph_from_latency(args.latency[0])
    print(nx.info(G))

    write_graph(G, args.outpath, args.format)
    print("{} written to {}".format(args.format, args.outpath))
