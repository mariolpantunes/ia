

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Sistemas Inteligentes I
# DETI / UA
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# Exercise II.2.15(a): associations that admit a single value
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   p = AssocOne('socrates','pai','sofronisco')

# Exercise II.2.15(a): associations with numerical values
class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   n = AssocNum('socrates','pulsacao',51)

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    # Exercise II.2.1: names of the associations that exist on the network
    def list_associations(self):
        return list(set([ d.relation.name
                           for d in self.declarations
                           if isinstance(d.relation, Association) ]))

    # Exercise II.2.2: objects whose existence can be inferred, i.e.
    # entities declared as instances (member) of some type
    def list_objects(self):
        return list(set([ d.relation.entity1
                           for d in self.declarations
                           if d.relation.name == "member" ]))

    # Exercise II.2.3: users on the network
    def list_users(self):
        return list(set([ d.user for d in self.declarations ]))

    # Exercise II.2.4: types on the network (super of a subtype and
    # type of a member)
    def list_types(self):
        return list(set([ d.relation.entity2
                           for d in self.declarations
                           if d.relation.name in ("subtype","member") ]))

    # Exercise II.2.5: names of the associations declared locally
    # for a given entity
    def list_local_associations(self,e1):
        return list(set([ d.relation.name
                           for d in self.declarations
                           if isinstance(d.relation, Association)
                           and d.relation.entity1 == e1 ]))

    # Exercise II.2.6: names of the relations declared by a user
    def list_relations_by_user(self,user):
        return list(set([ d.relation.name
                           for d in self.declarations
                           if d.user == user ]))

    # Exercise II.2.7: number of different associations used in the
    # relations declared by a user
    def associations_by_user(self,user):
        return len(set([ d.relation.name
                          for d in self.declarations
                          if d.user == user
                          and isinstance(d.relation, Association) ]))

    # Exercise II.2.8: locally declared associations of an entity as
    # (name, user) tuples
    def list_local_associations_by_entity(self,e1):
        return list(set((d.relation.name, d.user)
                         for d in self.declarations
                         if isinstance(d.relation, Association)
                         and d.relation.entity1 == e1 ))

    # Exercise II.2.9: True if a is a predecessor (ancestor) of b,
    # i.e. there is a chain of member and/or subtype relations
    # connecting b to a
    def predecessor(self,a,b):
        for d in self.declarations:
            r = d.relation
            if r.entity1 == b and r.name in ("member","subtype"):
                if r.entity2 == a or self.predecessor(a,r.entity2):
                    return True
        return False

    # Exercise II.2.10: path (list of entities) from a predecessor a to
    # b; None if a is not a predecessor of b
    def predecessor_path(self,a,b):
        if a == b:
            return [a]
        for d in self.declarations:
            r = d.relation
            if r.entity1 == b and r.name in ("member","subtype"):
                sub = self.predecessor_path(a,r.entity2)
                if sub != None:
                    return sub + [r.entity1]
        return None

    # Exercise II.2.11 helper: the entity itself and all its ancestors
    # (types through member/subtype chains), from specific to general
    def _ancestors(self,e1):
        chain = [e1]
        for d in self.declarations:
            r = d.relation
            if r.entity1 == e1 and r.name in ("member","subtype"):
                chain += self._ancestors(r.entity2)
        return chain

    # Exercise II.2.11(a): all local and inherited Association
    # declarations for a given entity (optionally of a given name)
    def query(self,e1,assoc=None):
        result = []
        for ent in self._ancestors(e1):
            for d in self.query_local(e1=ent):
                if isinstance(d.relation, Association) \
                   and (assoc == None or d.relation.name == assoc):
                    result.append(d)
        self.query_result = result
        return result

    # Exercise II.2.11(b): all local declarations (Association,
    # Subtype and Member) plus inherited Association declarations
    # (optionally of a given relation name)
    def query2(self,e1,assoc=None):
        local = self.query_local(e1=e1)
        inherited = [ d for d in self.query(e1,assoc)
                       if d not in local ]
        result = [ d for d in local
                    if assoc == None or d.relation.name == assoc ]
        result += inherited
        self.query_result = result
        return result

    # Exercise II.2.12: query with cancellation of inheritance - when
    # an association is declared in an entity, the entity does not
    # inherit that association from its predecessors (the rule applies
    # to every entity on the inheritance chain)
    def query_cancel(self,e1,assoc):
        localA = [ d for d in self.query_local(e1=e1,rel=assoc)
                    if isinstance(d.relation, Association) ]
        if localA != []:
            result = localA
        else:
            result = []
            for d in self.declarations:
                r = d.relation
                if r.entity1 == e1 and r.name in ("member","subtype"):
                    result += self.query_cancel(r.entity2,assoc)
        self.query_result = result
        return result

    # Exercise II.2.13: declarations of an association in the
    # descendants (subtypes and/or instances) of a type
    def query_down(self,type,assoc):
        result = []
        for d in self.declarations:
            r = d.relation
            if isinstance(r, Association) \
               and r.name == assoc \
               and self.predecessor(type,r.entity1):
                result.append(d)
        self.query_result = result
        return result

    # Exercise II.2.14: inductive inference - the most frequent value of
    # an association in the descending entities (subtypes/instances) of
    # a type
    def query_induce(self,type,assoc):
        values = [ d.relation.entity2
                    for d in self.query_down(type,assoc) ]
        return max(set(values), key=values.count)

    # Exercise II.2.15(b): values of the local associations of a given
    # entity, according to the type of the association
    def query_local_assoc(self,e1,assoc):
        decls = [ d for d in self.query_local(e1=e1,rel=assoc)
                   if isinstance(d.relation,(Association,AssocOne,AssocNum)) ]
        if decls == []:
            return None
        reltype = type(decls[0].relation)
        if reltype == Association:
            # most frequent values: added in decreasing order of
            # frequency until the sum of frequencies is >= 0.75
            values = [ d.relation.entity2 for d in decls ]
            n = len(values)
            freqs = [ (v, values.count(v)/n) for v in set(values) ]
            freqs.sort(key=lambda t: -t[1])
            result = []
            total = 0.0
            for (v,f) in freqs:
                result.append((v,round(f,2)))
                total += f
                if total >= 0.75:
                    break
            return result
        elif reltype == AssocOne:
            values = [ d.relation.entity2 for d in decls ]
            v = max(set(values), key=values.count)
            return (v, values.count(v)/len(values))
        else:
            # AssocNum: the average of the local values
            return sum(d.relation.entity2 for d in decls) / len(decls)

    # Exercise II.2.16: value of an association in an entity, taking
    # inherited declarations into account in case of local conflict
    def query_assoc_value(self,e1,assoc):
        local = [ d.relation.entity2 for d in self.query_local(e1=e1,rel=assoc)
                   if isinstance(d.relation, Association) ]
        if local != [] and len(set(local)) == 1:
            # all local declarations agree: ignore the predecessors
            return local[0]
        inherited = [ d.relation.entity2
                       for d in self.query(e1,assoc)
                       if d not in self.query_local(e1=e1,rel=assoc) ]
        if local == [] and inherited == []:
            return None
        # candidates in order of first declaration (deterministic)
        candidates = []
        for v in local + inherited:
            if v not in candidates:
                candidates.append(v)
        def F(v):
            L = (local.count(v)/len(local) if local != [] else 0.0)
            H = (inherited.count(v)/len(inherited)
                 if inherited != [] else 0.0)
            return L + H*H
        return max(candidates, key=F)


