"""Tests for the helpers and the guide exercises not covered by the
provided test_aula1.py / test_aula2.py."""

import math

from listutils import head, tail, head_tail
from aula1 import (contar_ocorrencias, menor_e_resto, dois_menores_e_resto,
                   media_mediana, inverte, fusao_ordenada)
from aula2 import (quantificador_existencial, dois_menores_e_resto_ordem,
                   cart2pol_lista, fusao_ordenada_ordem, conc_aplic,
                   aplic_combin, reduzir_listas, ordenar_seleccao,
                   ordenar_borbulhamento, ordenar_rapida)
from aula3 import Const, Var, Soma, Produto, Pai, Mae, Familia, Arvore

ASC = lambda x, y: x < y  # noqa: E731
DESC = lambda x, y: x > y  # noqa: E731


# Auxiliary head/tail helpers
def test_helpers():
    assert head([1, 2, 3]) == 1 and head([]) is None
    assert tail([1, 2, 3]) == [2, 3] and tail([1]) == [] and tail([]) is None
    assert head_tail([1, 2]) == (1, [2]) and head_tail([]) is None


# Inputs must never be modified
def test_no_side_effects():
    a, b = [3, 1, 2], [0, 4]
    inverte(a); fusao_ordenada(a, b); ordenar_rapida(a); ordenar_seleccao(a)
    ordenar_borbulhamento(a)
    assert a == [3, 1, 2] and b == [0, 4]


# Section 2
def test_contar_ocorrencias():
    assert contar_ocorrencias([1, 2, 1, 3, 2, 1]) == [(1, 3), (2, 2), (3, 1)]
    assert contar_ocorrencias([]) == []


# Section 3
def test_menor_e_resto():
    m, r = menor_e_resto([3, 1, 2])
    assert m == 1 and sorted(r) == [2, 3]
    assert menor_e_resto([]) is None


def test_dois_menores_e_resto():
    m1, m2, r = dois_menores_e_resto([5, 1, 4, 2])
    assert (m1, m2) == (1, 2) and sorted(r) == [4, 5]
    assert dois_menores_e_resto([1]) is None


def test_media_mediana():
    assert media_mediana([1, 2, 3]) == (2, 2)
    assert media_mediana([1, 2, 3, 6]) == (3, 2.5)
    assert media_mediana([]) is None


# Section 4
def test_quantificador_existencial():
    assert quantificador_existencial([1, 2, 3], lambda n: n > 2)
    assert not quantificador_existencial([1, 2, 3], lambda n: n > 3)


def test_dois_menores_e_resto_ordem():
    m1, m2, r = dois_menores_e_resto_ordem([5, 1, 4, 2], DESC)
    assert (m1, m2) == (5, 4) and sorted(r) == [1, 2]


def test_cart2pol_lista():
    r = cart2pol_lista([(0, 1), (1, 0)])
    assert r == [(1.0, math.pi / 2), (1.0, 0.0)]


def test_fusao_ordenada_ordem():
    assert fusao_ordenada_ordem([4, 2, 1], [5, 2, 0], DESC) == [5, 4, 2, 2, 1, 0]


def test_conc_aplic():
    assert conc_aplic([[1, 2], [3], []], lambda x: x * 10) == [10, 20, 30]


def test_aplic_combin():
    assert aplic_combin(([1, 2], [3, 4]), lambda a, b: a + b) == [4, 6]
    assert aplic_combin(([1, 2], [3]), lambda a, b: a + b) is None


def test_reduzir_listas():
    assert reduzir_listas([[1, 2, 3], [], [4]], lambda a, b: a + b, 0) == [6, 0, 4]


# Section 5
def test_ordenacao():
    lista = [3, -1, 4, 1, 5, 9, 2, 6, 5]
    for ordenar in (ordenar_seleccao, ordenar_borbulhamento, ordenar_rapida):
        assert ordenar(lista) == sorted(lista)
        assert ordenar(lista, DESC) == sorted(lista, reverse=True)
        assert ordenar(["b", "c", "a"], ASC) == ["a", "b", "c"]
        assert ordenar([]) == []


# Sorting by a key relation must keep equal elements in input order
def test_ordenacao_estavel():
    dados = [(1, "a"), (0, "x"), (1, "b"), (0, "y")]
    esperado = [(0, "x"), (0, "y"), (1, "a"), (1, "b")]
    por_chave = lambda p, q: p[0] < q[0]  # noqa: E731
    for ordenar in (ordenar_seleccao, ordenar_borbulhamento, ordenar_rapida):
        assert ordenar(dados, por_chave) == esperado


# Part III.1 - arithmetic expressions
def test_expressoes():
    # 2*x+1
    e = Soma(Produto(Const(2), Var()), Const(1))
    assert str(e) == "2*x+1"
    assert e.avaliar(3) == 7
    assert str(e.derivar()) == "2"
    # 2+x*(x+1)
    e2 = Soma(Const(2), Produto(Var(), Soma(Var(), Const(1))))
    assert str(e2) == "2+x*(x+1)"
    assert e2.avaliar(2) == 8
    assert str(e2.derivar()) == "x+1+x"
    # Neutral and absorbing elements.
    assert str(Soma(Const(0), Produto(Const(1), Var())).simplificar()) == "x"
    assert str(Produto(Var(), Const(0)).simplificar()) == "0"


# Part III.2 - genealogy
def test_familia():
    f = Familia([Pai("rui", "ana"), Mae("eva", "ana"), Pai("ze", "rui"),
                 Mae("ana", "tó")])
    assert str(f).startswith("Familia([Pai(rui,ana)")
    assert f.pais("ana") == ("rui", "eva")
    assert f.pais("tó") == (None, "ana")
    assert f.filhos("rui") == ["ana"]
    assert f.progenitor("eva", "ana") and not f.progenitor("ze", "ana")
    assert f.antepassado("ze", "tó") and not f.antepassado("tó", "ze")
    # an unknown parent (None) is nobody's progenitor
    assert not f.progenitor(None, "tó")


# Part III.3 - binary trees
def test_arvore():
    a = Arvore(5, Arvore(3, Arvore(1)), Arvore(8, None, Arvore(9)))
    assert str(a) == "5(3(1,-),8(-,9))"
    assert a.membro(9) and not a.membro(4)
    assert a.isomorfica(Arvore(0, Arvore(0, Arvore(0)), Arvore(0, None, Arvore(0))))
    assert not a.isomorfica(Arvore(0))
    assert Arvore(8, None, Arvore(9)).sub_arvore(a)
    assert not Arvore(8).sub_arvore(a)
    assert a.filtrar(lambda v: v > 4) == [5, 8, 9]
    c = a.copia()
    assert c is not a and str(c) == str(a)
    assert a.ordenada()
    assert not Arvore(5, Arvore(7)).ordenada()
    b = a.inserir(4)
    assert b.ordenada() and b.membro(4) and not a.membro(4)
    assert a.caminho(9) == [5, 8, 9]
    assert a.caminho(8) is None
