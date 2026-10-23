import pytest
from cidades import SearchProblem, SearchTree, cidades_portugal

@pytest.fixture
def braga_faro():
    return SearchProblem(cidades_portugal,'Braga','Faro')

def test_exercicio1(braga_faro):
    t = SearchTree(braga_faro,'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']

def test_exercicio2(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.open_nodes[-1].depth == 0
    t.search()
    assert t.solution.depth == 11

def test_exercicio3(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    t.search()

    assert t.length == 11

def test_exercicio4(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search(limit=9) == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Santarem', 'Lisboa', 'Beja', 'Faro']

    assert t.length <= 9

def test_exercicio5(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']
    assert t.terminals == 19
    assert t.non_terminals == 11

    t = SearchTree(braga_faro, 'depth')

    assert t.search(limit=9) == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Santarem', 'Lisboa', 'Beja', 'Faro']
    assert t.terminals == 12
    assert t.non_terminals == 58 

def test_exercicio6(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']
    assert round(t.avg_branching,2) == round((19+11-1)/11,2)


def test_search_is_rerunnable(braga_faro):
    # a second search() on the same tree starts from scratch
    t = SearchTree(braga_faro, 'depth')
    first = t.search(limit=9)
    assert t.search(limit=9) == first
    assert t.search() != first
    assert t.length == 11
    # a failing search must not keep the previous solution
    assert t.search(limit=2) is None
    assert t.solution is None and t.plan is None
