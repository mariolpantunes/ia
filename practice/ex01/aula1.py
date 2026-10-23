"""Guide 1, sections 1-3: recursive list and tuple processing.

Every solution is recursive and splits the list with the head/tail helpers
from listutils. Function names follow the guide (and the provided tests),
so they stay in Portuguese; documentation and comments are in English.
No function modifies the lists it receives.
"""

from listutils import head, tail, head_tail


# ---------------------------------------------------------------------------
# Section 1 - Recursive functions for list processing
# ---------------------------------------------------------------------------

# Exercise 1.1
def comprimento(lista):
    """Return the length of lista."""
    # Base case: the empty list has length 0.
    if lista == []:
        return 0
    # Recursive case: one element (the head) plus the length of the tail.
    return 1 + comprimento(tail(lista))


# Exercise 1.2
def soma(lista):
    """Return the sum of a list of numbers."""
    # Base case: 0 is the neutral element of addition.
    if lista == []:
        return 0
    # Recursive case: head plus the sum of the tail.
    h, t = head_tail(lista)
    return h + soma(t)


# Exercise 1.3
def existe(lista, elem):
    """Return True if elem occurs in lista, False otherwise."""
    # Base case: nothing occurs in the empty list.
    if lista == []:
        return False
    # Recursive case: found at the head, or somewhere in the tail.
    # "or" short-circuits, so the recursion stops at the first match.
    h, t = head_tail(lista)
    return h == elem or existe(t, elem)


# Exercise 1.4
def concat(l1, l2):
    """Return the concatenation of l1 and l2."""
    # Base case: concatenating the empty list with l2 gives (a copy of) l2.
    if l1 == []:
        return l2[:]
    # Recursive case: the head of l1 goes in front of concat(tail, l2).
    h, t = head_tail(l1)
    return [h] + concat(t, l2)


# Exercise 1.5
def inverte(lista):
    """Return lista in reverse order."""
    # Base case: the empty list is its own reverse.
    if lista == []:
        return []
    # Recursive case: reverse the tail, then append the head at the end.
    h, t = head_tail(lista)
    return inverte(t) + [h]


# Exercise 1.6
def capicua(lista):
    """Return True if lista reads the same in both directions (palindrome)."""
    # Base case: lists with 0 or 1 elements are always palindromes.
    if len(lista) <= 1:
        return True
    # Recursive case: first and last must match, and the middle part too.
    return head(lista) == lista[-1] and capicua(tail(lista)[:-1])


# Exercise 1.7
def concat_listas(lista):
    """Return the concatenation of a list of lists."""
    # Base case: concatenating no lists gives the empty list.
    if lista == []:
        return []
    # Recursive case: the first inner list followed by the rest, flattened.
    h, t = head_tail(lista)
    return h + concat_listas(t)


# Exercise 1.8
def substitui(lista, original, novo):
    """Return a copy of lista where every occurrence of original is novo."""
    # Base case: nothing to replace in the empty list.
    if lista == []:
        return []
    # Recursive case: replace the head if needed, then process the tail.
    h, t = head_tail(lista)
    return [novo if h == original else h] + substitui(t, original, novo)


# Exercise 1.9
def fusao_ordenada(lista1, lista2):
    """Merge two sorted lists of numbers into one sorted list (keeps repeats)."""
    # Base cases: if one list is exhausted, the other one is the rest.
    if lista1 == []:
        return lista2[:]
    if lista2 == []:
        return lista1[:]
    # Recursive case: the smaller head goes first, then merge what remains.
    h1, t1 = head_tail(lista1)
    h2, t2 = head_tail(lista2)
    if h1 <= h2:
        return [h1] + fusao_ordenada(t1, lista2)
    return [h2] + fusao_ordenada(lista1, t2)


# Exercise 1.10
def lista_subconjuntos(lista):
    """Return the list of all subsets of a set given as a list."""
    # Base case: the empty set has exactly one subset, itself.
    if lista == []:
        return [[]]
    # Recursive case: every subset of the tail appears twice,
    # once without the head and once with the head added.
    h, t = head_tail(lista)
    subs = lista_subconjuntos(t)
    return subs + [[h] + s for s in subs]


# ---------------------------------------------------------------------------
# Section 2 - Functions for list and tuple processing
# ---------------------------------------------------------------------------

# Exercise 2.1
def separar(lista):
    """Turn [(a1, b1), ..., (an, bn)] into ([a1, ..., an], [b1, ..., bn])."""
    # Base case: no pairs gives two empty lists.
    if lista == []:
        return ([], [])
    # Recursive case: unpack the head pair and prepend each part.
    (a, b), t = head_tail(lista)
    la, lb = separar(t)
    return ([a] + la, [b] + lb)


# Exercise 2.2
def remove_e_conta(lista, elem):
    """Return (lista without elem, number of occurrences of elem)."""
    # Base case: the empty list has no occurrences.
    if lista == []:
        return ([], 0)
    # Recursive case: solve for the tail, then account for the head.
    h, t = head_tail(lista)
    resto, n = remove_e_conta(t, elem)
    if h == elem:
        return (resto, n + 1)
    return ([h] + resto, n)


# Exercise 2.3
def contar_ocorrencias(lista):
    """Return a list of pairs (element, count) for each distinct element."""
    # Base case: no elements, no counts.
    if lista == []:
        return []
    # Recursive case: count the head in the tail (and remove it from there),
    # then count the remaining distinct elements.
    h, t = head_tail(lista)
    resto, n = remove_e_conta(t, h)
    return [(h, n + 1)] + contar_ocorrencias(resto)


# ---------------------------------------------------------------------------
# Section 3 - Functions that return None
# ---------------------------------------------------------------------------

# Exercise 3.1
def cabeca(lista):
    """Return the head of lista, or None if it is empty."""
    # Direct use of the auxiliary helper.
    return head(lista)


# Exercise 3.2
def cauda(lista):
    """Return the tail of lista, or None if it is empty."""
    # Direct use of the auxiliary helper.
    return tail(lista)


# Exercise 3.3
def juntar(l1, l2):
    """Zip two lists of equal length into a list of pairs; None otherwise."""
    # Base cases: both empty is a valid end, only one empty means
    # the lengths differ.
    if l1 == [] and l2 == []:
        return []
    if l1 == [] or l2 == []:
        return None
    # Recursive case: pair the heads and zip the tails.
    h1, t1 = head_tail(l1)
    h2, t2 = head_tail(l2)
    resto = juntar(t1, t2)
    # Propagate the failure found deeper in the recursion.
    if resto is None:
        return None
    return [(h1, h2)] + resto


# Exercise 3.4
def menor(lista):
    """Return the smallest element of a list of numbers; None if empty."""
    # Base case: the empty list has no minimum.
    if lista == []:
        return None
    # Recursive case: compare the head with the minimum of the tail.
    h, t = head_tail(lista)
    m = menor(t)
    # A None minimum means the tail was empty, so the head is the minimum.
    if m is None or h < m:
        return h
    return m


# Exercise 3.5
def menor_e_resto(lista):
    """Return (smallest element, list of the others); None if empty."""
    # Base case: the empty list has no minimum.
    if lista == []:
        return None
    # Recursive case: solve for the tail first.
    h, t = head_tail(lista)
    r = menor_e_resto(t)
    # Single-element list: the head is the minimum and nothing remains.
    if r is None:
        return (h, [])
    m, resto = r
    # The head wins: all the tail is the rest.
    if h <= m:
        return (h, t)
    # The tail minimum wins: the head joins the rest.
    return (m, [h] + resto)


# Exercise 3.6
def max_min(lista):
    """Return (maximum, minimum) of a list of numbers; None if empty."""
    # Base case: the empty list has no extremes.
    if lista == []:
        return None
    # Recursive case: combine the head with the extremes of the tail.
    h, t = head_tail(lista)
    r = max_min(t)
    # Single-element list: the head is both maximum and minimum.
    if r is None:
        return (h, h)
    mx, mn = r
    return (max(h, mx), min(h, mn))


# Exercise 3.7
def dois_menores_e_resto(lista):
    """Return (smallest, second smallest, others); None if fewer than 2."""
    # At least two elements are needed.
    if comprimento(lista) < 2:
        return None
    # Extract the minimum twice, reusing exercise 3.5.
    m1, r1 = menor_e_resto(lista)
    m2, r2 = menor_e_resto(r1)
    return (m1, m2, r2)


# Exercise 3.8
def media_mediana(lista):
    """Return (mean, median) of a sorted list of numbers; None if empty."""
    # The mean and the median of an empty list are undefined.
    if lista == []:
        return None
    n = comprimento(lista)
    media = soma(lista) / n
    meio = n // 2
    # Odd length: the middle element; even length: mean of the two middles.
    if n % 2 == 1:
        mediana = lista[meio]
    else:
        mediana = (lista[meio - 1] + lista[meio]) / 2
    return (media, mediana)
