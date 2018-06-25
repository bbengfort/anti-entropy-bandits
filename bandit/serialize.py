# bandit.serialize
# Graph serialization helper functions
#
# Author:  Benjamin Bengfort <benjamin@bengfort.com>
# Created: Mon Jun 25 11:23:40 2018 -0400
#
# ID: serialize.py [] benjamin@bengfort.com $

"""
Graph serialization helper functions
"""

##########################################################################
## Imports
##########################################################################

import json

from networkx.readwrite import json_graph


##########################################################################
## Helper Functions
##########################################################################

CHOICES = ('json', 'graphml',)


def read_graph(path, format="json"):
    if format not in CHOICES:
        raise ValueError("cannot deserialize graph format '{}'".format(format))

    if format == 'json':
        with open(path, 'r') as f:
            return json_graph.node_link_graph(json.load(f))

    if fomat == 'graphml':
        return nx.read_graphml(path)


def write_graph(G, path, format="json"):
    if format not in CHOICES:
        raise ValueError("cannot serialize graph format '{}'".format(format))

    if format == 'json':
        data = json_graph.node_link_data(G)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return

    if format == 'graphml':
        nx.write_graphml(G, path)
        return
