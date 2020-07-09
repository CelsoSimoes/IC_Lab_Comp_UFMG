ALLOW = "ALLOW"
DENY = "DENY"


def dfs(adj, node, fn):
  stack = []
  visited = set()

  stack.append(node)

  while stack:
    elem = stack.pop()
    visited.add(elem)

    if fn(elem):
      return True

    for neigh in adj[elem]:
      if not neigh in visited:
        stack.append(neigh)

  return False


# n1 ∧ n2 = ⊥ iff there's no node n such that there's a path from n1 to n and n2 to n
def is_glb_bottom(n1, n2, adj):
  path_n1 = set()
  path_n2 = set()
  dfs(adj, n1, lambda n: path_n1.add(n))
  dfs(adj, n2, lambda n: path_n2.add(n))
  return not path_n1.intersection(path_n2)


def path(adj, n1, n2):
  return dfs(adj, n1, lambda n: n == n2)


# lattice is an adjacency list, so v ≤ v' iff there's a path from v' to v
def partial_order(v, v_, lattice):
  return path(lattice, v_, v)


# True if TG ⊆ TC
# TG ⊆ TC = ∀ x . TG_x ⊆_x TC_x
# TG_x ⊆_x TC_x = ∀ v ∈ TG_x ∃ v' ∈ TC_x . v ≤_x v'
def order(TG, TC, lattices):
  for k, vs in TG.items():

    for v in vs:
      if not any([partial_order(v, v_, lattices[k]) for v_ in TC[k]]):
        return False
  return True


# True if ∀ x . ⊥ ∈ TG_x ⋂_x TC_x
# ⊥ ∈ TG = ∃ x . ⊥ ∈ T_x
# TG_x ⋂_x TC_x = { ∀ v ∈ TG_x v ∧_x v' | v' ∈ TC_x }
# basically we want to check if there's an attribute x such that v ∧_x v' = ⊥
def inter(TG, TC, lattices):
  return any([
      any([
          is_glb_bottom(v, v_, lattices[k]) for v in TG[k] for v_ in TC[k]
      ]) for k in TG.keys()
  ])


def allow(TC, TG, except_deny, lattice):
  return order(TG, TC, lattice) and all([deny(clause[1], TG, clause[2], lattice) for clause in except_deny])


def deny(TC, TG, except_allow, lattice):
  return inter(TG, TC, lattice) or any([allow(clause[1], TG, clause[2], lattice) for clause in except_allow])


def validate(nodes, clauses, lattices):
  for (method, TC, except_list) in clauses:

    policy = allow if method == ALLOW else deny

    for TG in nodes:
      if not policy(TC, TG, except_list, lattices):
        return False
  return True

# testing

# Each graph node G is labeled with a vector TG . Similarly, policy clauses contain a vector TC.

# Legalease policies are checked at each graph node.

# TG or TC is a list of nodes each which is a map of type "atribute" -> set of values


# these are the concept lattices for each attribute
# a lattice is an adjacency list where v ≤ v' iff there's an edge v' -> v
Actors = {
    "Top": {"Looker", "Intern"},
    "Looker": {"Analyst"},
    "Analyst": {"Alice", "Bob"},
    "Intern": {"Bob", "Jeff"},
    "Bob": {},
    "Alice": {},
    "Jeff": {}
}

#             +----+
#             |Top |
#             +----+
#             |    |
#             v    v
#     +-------+    +
#     |Looker |    |
#     ----+----    +
#         |        |
#         v        v
#     +-------+    +-------+
#     |Analyst|    |Intern |
#     +-------+    +-------+
#     |       |    |       |
#     v       v    v       v
# +---+-+    ++----+     +-+---+
# |Alice |    |Bob |     |Jeff |
# +-----+    +-----+     +-----+

Resources = {
    "Top": {"info", "Data"},
    "info": {"CNN", "Ip"},
    "Data": {"Ip", "SNN"},
    "CNN": {},
    "Ip": {},
    "SNN": {}
}

#             +----+
#             |Top |
#             +----+
#             |    |
#             v    v
#     +-------+    +-------+
#     | Info |    | Data  |
#     +-------+    +-------+
#     |       |    |       |
#     v       v    v       v
# +---+-+    ++----+     +-+---+
# | CNN |    | Ip  |     | SNN |
# +-----+    +-----+     +-----+

lattices = {"Actors": Actors, "Resources": Resources}


# policy:
# DENY
# EXCEPT
#   ALLOW Actors Analyst
#         Resources CNN
#   EXCEPT
#     DENY Actors Bob
#          Resources CNN

# these are the legalease clause translated from the above code
# each clause is a trIple containing (DENY / ALLOW, attributes, except list of clauses (recursive))
clauses = [
    ("DENY", {'Actors': {"Top"}, 'Resources': {"Top"}}, [
        ("ALLOW", {'Actors': {"Analyst"}, 'Resources': {"CNN"}}, [
            ("DENY", {'Actors': {"Bob"}, 'Resources': {"CNN"}}, [])
        ])
    ])
]

# this is a Data dependency graph
# for each test i'll create only one node meaning that actor X access resource Y
nodes1 = [{'Actors': {"Bob"}, 'Resources': {"CNN"}}]  # Bob access Ip
nodes2 = [{'Actors': {"Alice"}, 'Resources': {"CNN"}}]  # Alice access CNN
nodes3 = [{'Actors': {"Jeff"}, 'Resources': {"CNN"}}]  # Jeff access CNN

# should return False as Bob can't access Ip
print(validate(nodes1, clauses, lattices))
# should return True as Alice can access CNN
print(validate(nodes2, clauses, lattices))
# should return False as Jeff can't access CNN
print(validate(nodes3, clauses, lattices))

# @TODO: so I don't need to handle "Key Error" exceptions in the algorithm, when generating the TG and TC sets, for every attribute I must generate a set, if there's no contraint in such attribute, then use an empty set.

# end
