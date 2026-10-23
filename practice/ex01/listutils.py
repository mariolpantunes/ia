"""Auxiliary functions to decompose a list into head and tail.

They follow the examples in the theory slides ("cabeca" and
"cabeca_e_cauda", slide 35): each one returns None when the list is empty,
so a recursive solution can split any non-empty list in a single step.
None of them modifies the input list: slices always produce copies.
"""


def head(lst):
    """Return the first element of lst, or None if lst is empty."""
    # An empty list has no head.
    if lst == []:
        return None
    # The head is the element at position 0.
    return lst[0]


def tail(lst):
    """Return all elements of lst except the first, or None if lst is empty."""
    # An empty list has no tail.
    if lst == []:
        return None
    # The slice [1:] is a new list, so the caller's list stays untouched.
    return lst[1:]


def head_tail(lst):
    """Return the pair (head, tail) of lst, or None if lst is empty.

    Typical use in a recursive function, after handling the base case:
        h, t = head_tail(lst)
    """
    # An empty list cannot be decomposed.
    if lst == []:
        return None
    # Reuse the two helpers above so the definitions stay in one place.
    return (head(lst), tail(lst))
