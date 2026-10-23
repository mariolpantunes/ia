# Exercise IV.1b: three friends, bikes and hats
#
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2026
#

from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

# two friends cannot ride the same bike or wear the same hat
def distinct(X, x, Y, y):
    return x[0] != y[0] and x[1] != y[1]

def make_domains():
    # the unary constraints (no one takes his own bike or hat, and
    # whoever wears Claudio's hat must ride Bernardo's bike) are
    # enforced here by pre-processing the domains.
    domains = {}
    for amigo in amigos:
        values = []
        for bike in amigos:
            for hat in amigos:
                if bike == amigo:
                    continue
                if hat == amigo:
                    continue
                if hat == "Claudio" and bike != "Bernardo":
                    continue
                values.append((bike, hat))
        domains[amigo] = values
    return domains

def make_constraints():
    return { (X, Y): distinct
             for X in amigos for Y in amigos if X != Y }

cs = ConstraintSearch(make_domains(), make_constraints())

print(cs.search())
