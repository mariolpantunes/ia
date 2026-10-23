
# Module: tree_search
#
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2020,
#  Inteligência Artificial, 2014-2026

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, action=None, depth=0, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        # Exercise II.2: depth of the node in the tree (root is depth 0)
        self.depth = depth
        # Exercise II.8: accumulated cost of the path root -> node
        self.cost = cost
        # Exercise II.12: heuristic estimate of the cost node -> goal
        self.heuristic = heuristic
        # Exercise III.2: the action that led from the parent to this node
        self.action = action
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'):
        self.problem = problem
        root = SearchNode(problem.initial, None)
        # Exercise II.12: record the root heuristic (root -> goal)
        root.heuristic = self.problem.domain.heuristic(problem.initial, problem.goal)
        self._root = root
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        # Exercise II.5: counters for the tree statistics
        self.terminals = 0
        self.non_terminals = 0
        # Exercise III.2: the sequence of actions of the solution
        self.plan = None
        # Exercise II.15: node(s) with the higher accumulated cost
        self.highest_cost_nodes = []
        # book-keeping for the tree statistics (exercises II.15/II.16)
        self._all_nodes = []
        self._maxcost = -1

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # Exercise II.3: length of the solution (number of state transitions)
    @property
    def length(self):
        if self.solution == None:
            return 0
        return self.solution.depth

    # Exercise II.6: average branching factor
    @property
    def avg_branching(self):
        # number of child nodes (all except the root) / number of
        # parent nodes (the expanded / non-terminal nodes)
        if self.non_terminals == 0:
            return 0
        return (self.terminals + self.non_terminals - 1) / self.non_terminals

    # Exercise II.9: total cost of the solution found
    @property
    def cost(self):
        if self.solution == None:
            return 0
        return self.solution.cost

    # Exercise II.16: average depth of the nodes in the generated tree
    @property
    def average_depth(self):
        # average of the depth of every node that was created
        if self._all_nodes == []:
            return 0
        return sum(n.depth for n in self._all_nodes) / len(self._all_nodes)

    # Exercise II.15 helper: register a node in the tree book-keeping
    def _record_node(self,node):
        self._all_nodes.append(node)
        if node.cost > self._maxcost:
            self._maxcost = node.cost
            self.highest_cost_nodes = [node]
        elif node.cost == self._maxcost:
            self.highest_cost_nodes.append(node)

    # procurar a solucao
    def search(self, limit=None):
        # Exercise II.4: a depth limit for depth-limited search
        # start from a fresh tree so that search() can be called again
        # (e.g. with another limit) on the same SearchTree
        self.open_nodes = [self._root]
        self.solution = None
        self.plan = None
        self._all_nodes = []
        self._maxcost = -1
        self.highest_cost_nodes = []
        # the root is part of the tree
        self._record_node(self.open_nodes[0])
        self.terminals = 0
        self.non_terminals = 0
        while self.open_nodes != []:
            # Exercise II.10/II.13/II.14: pick the node according to strategy
            if self.strategy == 'uniform':
                self.open_nodes.sort(key=lambda n: n.cost)
                node = self.open_nodes.pop(0)
            elif self.strategy == 'greedy':
                self.open_nodes.sort(key=lambda n: n.heuristic)
                node = self.open_nodes.pop(0)
            elif self.strategy == 'a*':
                self.open_nodes.sort(key=lambda n: n.cost + n.heuristic)
                node = self.open_nodes.pop(0)
            else:
                node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.plan = self.get_actions(node)
                # Exercise II.5: a terminal node is any node that was
                # never expanded (still open or never reached)
                self.terminals = len(self._all_nodes) - self.non_terminals
                return self.get_path(node)
            # Exercise II.5: a non-terminal (expanded) node, even if
            # without children (as happens at the depth limit)
            self.non_terminals += 1
            # Exercise II.4: depth-limited search does not generate
            # children at or beyond the limit
            if limit != None and node.depth >= limit:
                continue
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                # Exercise II.1: avoid branches with loops - do not
                # create a node whose state is already on the path
                # (an ancestor) of the current node.
                newstate = self.problem.domain.result(node.state,a)
                if self._on_path(node, newstate):
                    continue
                newnode = SearchNode(newstate,node,action=a,
                                     depth=node.depth+1)
                # Exercise II.8: record the accumulated cost
                actioncost = self.problem.domain.cost(node.state,a)
                newnode.cost = node.cost + (actioncost if actioncost != None else 0)
                # Exercise II.12: record the heuristic
                newnode.heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        # Exercise II.5: terminal = every node that was not expanded
        self.terminals = len(self._all_nodes) - self.non_terminals
        return None

    # Exercise II.1: check whether "newstate" (the result of an action in
    # "node") is already on the path from the root to "node", which
    # would create a branch with a loop. "node" itself is included, so
    # an action that does not change the state is also a loop.
    def _on_path(self,node,newstate):
        anc = node
        while anc != None:
            if anc.state == newstate:
                return True
            anc = anc.parent
        return False

    # Exercise III.2: obtain the sequence of actions from the root to "node"
    def get_actions(self,node):
        if node.parent == None:
            return []
        acts = self.get_actions(node.parent)
        acts += [node.action]
        return acts

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            # Exercise II.10: uniform cost search - the open nodes are
            # ordered by accumulated cost (checked in search)
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'greedy':
            # Exercise II.13: greedy search - ordered by heuristic
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'a*':
            # Exercise II.14: A* - ordered by cost + heuristic
            self.open_nodes.extend(lnewnodes)
        else:
            self.open_nodes.extend(lnewnodes)
        for n in lnewnodes:
            self._record_node(n)
