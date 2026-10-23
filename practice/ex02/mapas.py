# Exercise IV.1a: colouring a map
#
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2026
#

from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

# The five regions are arranged in a ring: each region borders the two
# regions next to it. Two bordering regions cannot have the same colour.
edges = [ ('A','B'), ('B','C'), ('C','E'), ('E','D'), ('D','A') ]

def no_same_color(X, cx, Y, cy):
    """Two neighbouring regions must have different colours."""
    return cx != cy

def make_domains():
    return { r: list(colors) for r in region }

def make_constraints():
    return { (X,Y): no_same_color for (X,Y) in edges }

cs = ConstraintSearch(make_domains(), make_constraints())

print(cs.search())
