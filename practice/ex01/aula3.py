"""Guide 1, part III: classes.

1. Arithmetic expressions (Const, Var, Soma, Produto).
2. Family relations and genealogy (Pai, Mae, Familia).
3. Binary trees (Arvore).

Class and method names follow the guide and slides (Portuguese);
documentation and comments are in English.
"""

from listutils import head_tail


# ---------------------------------------------------------------------------
# 1 - Arithmetic expressions
# Each expression type is a class with the same interface:
#   __str__()       text form            (1.1)
#   avaliar(v)      value for x = v      (1.2)
#   simplificar()   simpler equivalent   (1.3)
#   derivar()       derivative in x      (1.4)
# ---------------------------------------------------------------------------

class Const:
    """A numeric constant."""

    def __init__(self, valor):
        # The number this constant stands for.
        self.valor = valor

    def __str__(self):
        return str(self.valor)

    def avaliar(self, v):
        # A constant does not depend on the variable.
        return self.valor

    def simplificar(self):
        # A constant is already as simple as possible.
        return self

    def derivar(self):
        # d/dx c = 0
        return Const(0)


class Var:
    """An occurrence of the (single) variable x."""

    def __str__(self):
        return "x"

    def avaliar(self, v):
        # The value of x is the value given.
        return v

    def simplificar(self):
        # A variable is already as simple as possible.
        return self

    def derivar(self):
        # d/dx x = 1
        return Const(1)


def _e_const(e, valor):
    """True if expression e is the constant valor (used by simplification)."""
    return isinstance(e, Const) and e.valor == valor


class Soma:
    """The sum e1 + e2 of two expressions."""

    def __init__(self, e1, e2):
        self.arg1 = e1
        self.arg2 = e2

    def __str__(self):
        # A sum has the lowest precedence, so no parentheses are needed here.
        return str(self.arg1) + "+" + str(self.arg2)

    def avaliar(self, v):
        # Evaluate both operands and add.
        return self.arg1.avaliar(v) + self.arg2.avaliar(v)

    def simplificar(self):
        # Simplify the operands first (bottom-up).
        a = self.arg1.simplificar()
        b = self.arg2.simplificar()
        # 0 is the neutral element of addition: 0+e = e+0 = e.
        if _e_const(a, 0):
            return b
        if _e_const(b, 0):
            return a
        return Soma(a, b)

    def derivar(self):
        # (f+g)' = f' + g'
        return Soma(self.arg1.derivar(), self.arg2.derivar()).simplificar()


class Produto:
    """The product e1 * e2 of two expressions."""

    def __init__(self, e1, e2):
        self.arg1 = e1
        self.arg2 = e2

    def __str__(self):
        # A sum inside a product needs parentheses to keep its meaning.
        def fmt(e):
            return "(" + str(e) + ")" if isinstance(e, Soma) else str(e)
        return fmt(self.arg1) + "*" + fmt(self.arg2)

    def avaliar(self, v):
        # Evaluate both operands and multiply.
        return self.arg1.avaliar(v) * self.arg2.avaliar(v)

    def simplificar(self):
        # Simplify the operands first (bottom-up).
        a = self.arg1.simplificar()
        b = self.arg2.simplificar()
        # 0 is the absorbing element of multiplication: 0*e = e*0 = 0.
        if _e_const(a, 0) or _e_const(b, 0):
            return Const(0)
        # 1 is the neutral element of multiplication: 1*e = e*1 = e.
        if _e_const(a, 1):
            return b
        if _e_const(b, 1):
            return a
        return Produto(a, b)

    def derivar(self):
        # Product rule: (f*g)' = f'*g + f*g'
        f, g = self.arg1, self.arg2
        return Soma(Produto(f.derivar(), g),
                    Produto(f, g.derivar())).simplificar()


# ---------------------------------------------------------------------------
# 2 - Family relations and genealogy
# ---------------------------------------------------------------------------

class Pai:
    """Relation Pai(x, y): x is the father of y (2.1)."""

    def __init__(self, x, y):
        self.progenitor = x
        self.filho = y

    def __str__(self):
        return "Pai(" + str(self.progenitor) + "," + str(self.filho) + ")"


class Mae:
    """Relation Mae(x, y): x is the mother of y (2.1)."""

    def __init__(self, x, y):
        self.progenitor = x
        self.filho = y

    def __str__(self):
        return "Mae(" + str(self.progenitor) + "," + str(self.filho) + ")"


class Familia:
    """A genealogy: a collection of Pai/Mae relations (2.2)."""

    def __init__(self, relacoes):
        # Keep a copy so later changes to the caller's list do not leak in.
        self.relacoes = relacoes[:]

    def __str__(self):
        return "Familia([" + ", ".join(str(r) for r in self.relacoes) + "])"

    def pais(self, ind):
        """Return (father, mother) of ind; None marks an unknown parent (2.3)."""
        pai = [r.progenitor for r in self.relacoes
               if isinstance(r, Pai) and r.filho == ind]
        mae = [r.progenitor for r in self.relacoes
               if isinstance(r, Mae) and r.filho == ind]
        # Each list has at most one element in a consistent genealogy.
        return (pai[0] if pai else None, mae[0] if mae else None)

    def filhos(self, ind):
        """Return the list of children of ind (2.4)."""
        return [r.filho for r in self.relacoes if r.progenitor == ind]

    def progenitor(self, x, y):
        """Return True if x is a parent of y (2.5)."""
        # None marks an unknown parent in pais(), so it is never a progenitor.
        return x is not None and x in self.pais(y)

    def antepassado(self, x, y):
        """Return True if x is an ancestor of y (2.6)."""
        # Base case: a parent is an ancestor.
        if self.progenitor(x, y):
            return True
        # Recursive case: x is an ancestor of one of y's known parents.
        return any(self.antepassado(x, p) for p in self.pais(y) if p is not None)


# ---------------------------------------------------------------------------
# 3 - Binary trees
# A tree is an Arvore node with a value and two subtrees; the empty tree is
# None. Module-level helpers accept None, so the recursion needs no special
# cases for missing children. Methods delegate to them.
# ---------------------------------------------------------------------------

class Arvore:
    """A binary tree node: valor, left subtree esq, right subtree dir."""

    def __init__(self, valor, esq=None, dir=None):
        self.valor = valor
        self.esq = esq
        self.dir = dir

    def __str__(self):
        # Prefix notation: valor(left,right); the empty tree prints as "-".
        def fmt(a):
            return "-" if a is None else str(a)
        if self.esq is None and self.dir is None:
            return str(self.valor)
        return str(self.valor) + "(" + fmt(self.esq) + "," + fmt(self.dir) + ")"

    def membro(self, x):
        """3.1: True if x occurs in the tree."""
        return _membro(self, x)

    def isomorfica(self, outra):
        """3.2: True if both trees have the same shape (values ignored)."""
        return _isomorficas(self, outra)

    def sub_arvore(self, outra):
        """3.3: True if this tree occurs (shape and values) inside outra."""
        return _sub_arvore(self, outra)

    def filtrar(self, cond):
        """3.4: list of values that satisfy cond (in-order traversal)."""
        return _filtrar(self, cond)

    def copia(self):
        """3.5: a deep copy of the tree."""
        return _copia(self)

    def ordenada(self):
        """3.6: True if the tree is a binary search tree."""
        return _ordenada(_filtrar(self, lambda _: True))

    def inserir(self, valor):
        """3.7: a new ordered tree with valor inserted (self is not changed)."""
        return _inserir(self, valor)

    def caminho(self, folha):
        """3.8: values from the root to the leaf folha, or None if absent."""
        return _caminho(self, folha)


def _membro(a, x):
    # Empty tree: nothing occurs. Otherwise check the root and both subtrees.
    if a is None:
        return False
    return a.valor == x or _membro(a.esq, x) or _membro(a.dir, x)


def _isomorficas(a, b):
    # Both empty: same shape. Only one empty: different shape.
    if a is None or b is None:
        return a is None and b is None
    # Same shape when both pairs of subtrees have the same shape.
    return _isomorficas(a.esq, b.esq) and _isomorficas(a.dir, b.dir)


def _iguais(a, b):
    # Like _isomorficas, but the values must match too.
    if a is None or b is None:
        return a is None and b is None
    return (a.valor == b.valor and _iguais(a.esq, b.esq)
            and _iguais(a.dir, b.dir))


def _sub_arvore(a, b):
    # a is a subtree of b if it equals b or is a subtree of one of b's children.
    if b is None:
        return a is None
    return _iguais(a, b) or _sub_arvore(a, b.esq) or _sub_arvore(a, b.dir)


def _filtrar(a, cond):
    # In-order: left subtree, root, right subtree.
    if a is None:
        return []
    raiz = [a.valor] if cond(a.valor) else []
    return _filtrar(a.esq, cond) + raiz + _filtrar(a.dir, cond)


def _copia(a):
    # Copy the root and, recursively, both subtrees.
    if a is None:
        return None
    return Arvore(a.valor, _copia(a.esq), _copia(a.dir))


def _ordenada(valores):
    # A tree is ordered when its in-order values are non-decreasing.
    # Checked recursively on the list with the head/tail helpers.
    if len(valores) < 2:
        return True
    h, t = head_tail(valores)
    return h <= t[0] and _ordenada(t)


def _inserir(a, valor):
    # Empty tree: the new value becomes a leaf.
    if a is None:
        return Arvore(valor)
    # Descend left or right; untouched subtrees are copied.
    if valor < a.valor:
        return Arvore(a.valor, _inserir(a.esq, valor), _copia(a.dir))
    return Arvore(a.valor, _copia(a.esq), _inserir(a.dir, valor))


def _caminho(a, folha):
    # Empty tree: no path.
    if a is None:
        return None
    # A leaf with the wanted value ends the path.
    if a.esq is None and a.dir is None:
        return [a.valor] if a.valor == folha else None
    # Try the left subtree, then the right one; prepend the root on success.
    for sub in (a.esq, a.dir):
        c = _caminho(sub, folha)
        if c is not None:
            return [a.valor] + c
    return None
