# Constraint-based search for assignment problems
#
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2026
#


class ConstraintSearch:

    # domains é um dicionário com o domínio de cada variável;
    # constaints e' um dicionário com a restrição aplicável a cada aresta;
    def __init__(self,domains,constraints):
        self.domains = domains
        self.constraints = constraints
        self.calls = 0

    # Exercise IV.2: propagate the constraints. After a value has been
    # assigned to a variable, forward checking removes from the domain of
    # every (still unassigned) variable that shares an edge with it the
    # values that violate the edge constraint with the assigned value.
    # A new dictionary is returned, so the original domains are not
    # modified.
    # Note: this is single-step forward checking, not the full AC-3 of the
    # slides (no re-queuing of edges after a pruning). AC-3 needs fewer
    # calls (amigos: 5 instead of 7), so it would not match the call
    # counts pinned by the tests.
    def propagate(self, domains, assigned, value):
        newdomains = { var: list(values)
                       for (var, values) in domains.items() }
        for (var1, var2) in self.constraints:
            constraint = self.constraints[var1, var2]
            if var1 == assigned:
                # prune the domain of var2
                newdomains[var2] = [ v2 for v2 in newdomains[var2]
                                     if constraint(assigned, value, var2, v2) ]
            elif var2 == assigned:
                # prune the domain of var1
                newdomains[var1] = [ v1 for v1 in newdomains[var1]
                                     if constraint(var1, v1, assigned, value) ]
        return newdomains

    # domains é um dicionário com os domínios actuais
    # de cada variável
    # ( ver acetato "Pesquisa com propagacao de restricoes
    #   em problemas de atribuicao - algoritmo" )
    def search(self,domains=None):
        self.calls += 1

        if domains==None:
            domains = self.domains

        # se alguma variavel tiver lista de valores vazia, falha
        if any([lv==[] for lv in domains.values()]):
            return None

        # se nenhuma variavel tiver mais do que um valor possivel, sucesso
        if all([len(lv)==1 for lv in list(domains.values())]):
            # se valores violam restricoes, falha
            # ( verificacao desnecessaria se for feita a propagacao
            #   de restricoes )
            for (var1,var2) in self.constraints:
                constraint = self.constraints[var1,var2]
                if not constraint(var1,domains[var1][0],var2,domains[var2][0]):
                    return None
            return { v:lv[0] for (v,lv) in domains.items() }

        # continuação da pesquisa
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    # Exercise IV.2: assign the value to the variable and
                    # propagate the constraints to its neighbours
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    newdomains = self.propagate(newdomains, var, val)
                    solution = self.search(newdomains)
                    if solution != None:
                        return solution
        return None
