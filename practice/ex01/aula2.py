"""Guide 1, sections 4-5: lambda expressions, higher-order functions, sorting.

Recursive solutions split lists with the head/tail helpers from listutils.
Function names follow the guide (and the provided tests), so they stay in
Portuguese; documentation and comments are in English.
No function modifies the lists it receives.
"""

import math
from functools import reduce

from listutils import head_tail


# ---------------------------------------------------------------------------
# Section 4 - Lambda expressions and higher-order functions
# ---------------------------------------------------------------------------

# Exercise 4.1: True if the integer n is odd.
impar = lambda n: n % 2 != 0  # noqa: E731

# Exercise 4.2: True if the number n is positive (strictly greater than 0).
positivo = lambda n: n > 0  # noqa: E731

# Exercise 4.3: True if |x| < |y|.
comparar_modulo = lambda x, y: abs(x) < abs(y)  # noqa: E731

# Exercise 4.4: cartesian (x, y) to polar (r, theta).
# hypot gives the distance to the origin; atan2 gives the angle in the
# correct quadrant (plain atan(y/x) fails for x == 0 and for x < 0).
cart2pol = lambda x, y: (math.hypot(x, y), math.atan2(y, x))  # noqa: E731

# Exercise 4.5: given f, g, h (two inputs each), build the three-input
# function (x, y, z) -> h(f(x, y), g(y, z)). The outer lambda returns
# the inner one, so ex5 is a function that produces functions.
ex5 = lambda f, g, h: lambda x, y, z: h(f(x, y), g(y, z))  # noqa: E731


# Exercise 4.6
def quantificador_universal(lista, f):
    """Return True if f(x) is True for every x in lista (for all)."""
    # Base case: "for all" holds vacuously on the empty list.
    if lista == []:
        return True
    # Recursive case: the head must satisfy f, and so must the tail.
    h, t = head_tail(lista)
    return f(h) and quantificador_universal(t, f)


# Exercise 4.7
def quantificador_existencial(lista, f):
    """Return True if f(x) is True for at least one x in lista (exists)."""
    # Base case: nothing exists in the empty list.
    if lista == []:
        return False
    # Recursive case: the head satisfies f, or some element of the tail does.
    h, t = head_tail(lista)
    return f(h) or quantificador_existencial(t, f)


# Exercise 4.8
def subconjunto(lista1, lista2):
    """Return True if every element of lista1 also occurs in lista2."""
    # A subset is a universal quantification: every x of lista1 is in lista2.
    return quantificador_universal(lista1, lambda x: x in lista2)


# Exercise 4.9
def menor_ordem(lista, f):
    """Return the smallest element of a non-empty lista according to f.

    f(a, b) is an order relation: True means a comes before b.
    """
    h, t = head_tail(lista)
    # Base case: a single element is the smallest.
    if t == []:
        return h
    # Recursive case: compare the head with the smallest of the tail.
    m = menor_ordem(t, f)
    return h if f(h, m) else m


# Exercise 4.10
def menor_e_resto_ordem(lista, f):
    """Return (smallest according to f, list of the others); lista not empty."""
    h, t = head_tail(lista)
    # Base case: a single element is the smallest and nothing remains.
    if t == []:
        return (h, [])
    # Recursive case: solve for the tail and compare with the head.
    m, resto = menor_e_resto_ordem(t, f)
    # "not f(m, h)" lets the head win ties, which keeps the sort stable.
    if not f(m, h):
        # The head wins: the whole tail is the rest.
        return (h, t)
    # The tail minimum wins: the head joins the rest.
    return (m, [h] + resto)


# Exercise 4.11
def dois_menores_e_resto_ordem(lista, f):
    """Return (smallest, second smallest, others) according to f.

    lista must have at least two elements.
    """
    # Extract the minimum twice, reusing exercise 4.10.
    m1, r1 = menor_e_resto_ordem(lista, f)
    m2, r2 = menor_e_resto_ordem(r1, f)
    return (m1, m2, r2)


# Exercise 4.12
def cart2pol_lista(lista):
    """Convert a list of cartesian pairs (x, y) to polar pairs (r, theta)."""
    # map applies cart2pol (4.4) to each pair; the star unpacks (x, y).
    return list(map(lambda p: cart2pol(*p), lista))


# Exercise 4.13
def fusao_ordenada_ordem(lista1, lista2, f):
    """Merge two lists sorted by f into one list sorted by f (keeps repeats)."""
    # Base cases: if one list is exhausted, the other one is the rest.
    if lista1 == []:
        return lista2[:]
    if lista2 == []:
        return lista1[:]
    # Recursive case: the head that comes first goes first.
    h1, t1 = head_tail(lista1)
    h2, t2 = head_tail(lista2)
    # "not f(h2, h1)" keeps the merge stable: on ties lista1 goes first.
    if not f(h2, h1):
        return [h1] + fusao_ordenada_ordem(t1, lista2, f)
    return [h2] + fusao_ordenada_ordem(lista1, t2, f)


# Exercise 4.14
def conc_aplic(listas, f):
    """Apply f to every element of every inner list and concatenate."""
    # Nested list comprehension: outer loop over lists, inner over elements.
    return [f(x) for lista in listas for x in lista]


# Exercise 4.15
def aplic_combin(par, f):
    """Given ([a1..an], [b1..bn]) return [f(a1, b1), ..., f(an, bn)].

    Returns None if the two lists have different lengths.
    """
    l1, l2 = par
    # Base cases: both empty ends the recursion; one empty means mismatch.
    if l1 == [] and l2 == []:
        return []
    if l1 == [] or l2 == []:
        return None
    # Recursive case: combine the heads, then the tails.
    h1, t1 = head_tail(l1)
    h2, t2 = head_tail(l2)
    resto = aplic_combin((t1, t2), f)
    # Propagate a length mismatch found deeper in the recursion.
    if resto is None:
        return None
    return [f(h1, h2)] + resto


# Exercise 4.16
def reduzir_listas(listas, f, neutro):
    """Reduce each inner list with f starting from neutro; return the results."""
    # functools.reduce folds one list; the comprehension does it for each list.
    return [reduce(f, lista, neutro) for lista in listas]


# ---------------------------------------------------------------------------
# Section 5 - Sorting
# Exercise 5.1 (numbers) and 5.2 (any order relation) share one function per
# algorithm: the default order "x < y" solves 5.1, a custom one solves 5.2.
# ---------------------------------------------------------------------------

# Default order relation: ascending numeric order.
_ascendente = lambda x, y: x < y  # noqa: E731


# Exercise 5.1a / 5.2a
def ordenar_seleccao(lista, ordem=_ascendente):
    """Selection sort: repeatedly select the smallest element."""
    # Base case: the empty list is already sorted.
    if lista == []:
        return []
    # Recursive case: the smallest goes first, then sort the rest.
    m, resto = menor_e_resto_ordem(lista, ordem)
    return [m] + ordenar_seleccao(resto, ordem)


def _borbulhar(lista, ordem):
    """One bubble sort pass: the largest element ends at the last position."""
    # Base case: fewer than two elements, nothing to swap.
    if len(lista) < 2:
        return lista[:]
    # Compare the first two elements and keep the larger one moving right.
    a, t = head_tail(lista)
    b, t2 = head_tail(t)
    if ordem(b, a):
        return [b] + _borbulhar([a] + t2, ordem)
    return [a] + _borbulhar([b] + t2, ordem)


# Exercise 5.1b / 5.2b
def ordenar_borbulhamento(lista, ordem=_ascendente):
    """Bubble sort: each pass moves the largest element to the end."""
    # Base case: lists with fewer than two elements are sorted.
    if len(lista) < 2:
        return lista[:]
    # One pass fixes the last element; sort the others recursively.
    passo = _borbulhar(lista, ordem)
    return ordenar_borbulhamento(passo[:-1], ordem) + [passo[-1]]


# Exercise 5.1c / 5.2c
def ordenar_rapida(lista, ordem=_ascendente):
    """Quick sort: partition around the head (pivot) and sort each part."""
    # Base case: the empty list is already sorted.
    if lista == []:
        return []
    # The head is the pivot; split the tail into "before" and "not before".
    pivo, t = head_tail(lista)
    antes = [x for x in t if ordem(x, pivo)]
    depois = [x for x in t if not ordem(x, pivo)]
    # Sorted "before" part, then the pivot, then the sorted "after" part.
    return ordenar_rapida(antes, ordem) + [pivo] + ordenar_rapida(depois, ordem)
