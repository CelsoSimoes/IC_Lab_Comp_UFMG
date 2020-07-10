class Datagraph:
  def __init__(self, T, lattices):
    self.lattices = lattices
    self.T = T

  def _dfs(self, attr, node, fn):
    adj = self.lattices[attr]
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

  def _glb_bottom(self, attr, n1, n2):
    path_n1 = set()
    path_n2 = set()
    self._dfs(attr, n1, lambda n: path_n1.add(n))
    self._dfs(attr, n2, lambda n: path_n2.add(n))
    return not path_n1.intersection(path_n2)

  def _path(self, attr, n1, n2):
    return self._dfs(attr, n1, lambda n: n == n2)

  def __getitem__(self, key):
    return self.T[key]

  def __str__(self):
    return str(self.T)

  def __le__(self, T_):
    for k, vs in self.T.items():
      for v in vs:
        if not any([self._path(k, v_, v) for v_ in T_[k]]):
          return False
    return True

  def inter(self, T_):
    return any([
        any([
            self._glb_bottom(k, v, v_) for v in self.T[k] for v_ in T_[k]
        ]) for k in self.T.keys()
    ])


class Legalease():
  def __init__(self, lattices):
    self.lattices = lattices
    self.policy = {"ALLOW": self.allow, "DENY": self.deny}

  def allow(self, TC, TG, except_deny):
    return TG <= TC and all(self.policies(TG, except_deny))

  def deny(self, TC, TG, except_allow):
    return TG.inter(TC) or any(self.policies(TG, except_allow))

  def policies(self, TG, clauses):
    return [
        self.policy[method](
            Datagraph(TC, self.lattices),
            TG,
            except_list
        )
        for (method, TC, except_list) in clauses
    ]

  def validate(self, nodes, clauses):
    return all([
        all(self.policies(Datagraph(TG, self.lattices), clauses))
        for TG in nodes
    ])


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
# +---+-+    +-----+     +-+---+
# |Alice |   | Bob |     |Jeff |
# +-----+    +-----+     +-----+


Resources = {
    "Top": {"claims"},
    "claims": {"finance"},
    "finance": {"customers", "companies"},
    "customers": {"CCN"},
    "companies": {"EMAIL", "SSN"},
    "CCN": {},
    "EMAIL": {},
    "SSN": {}
}

#             +-------+
#             |  Top  |
#             +-------+
#                 |
#                 v
#           +-----------+
#           |   Claims  |
#           +-----------+
#                   |
#                   v
#           +---------------+
#           |     Finance   |
#           +---------------+
#          |                |
#          v                v
#     +----------+      +----------+
#     |Customers |      |Companies |
#     +---------+      +----------+
#         |            |           |
#        v            v           v
#    +---+-+       +------+    +-----+
#    | CCN |      | EMAIL|    | SSN |
#    +-----+     +------+    +-----+

Actions = {
    "Top": {"Reads", "Deletes", "Updates"},
    "Reads": {},
    "Deletes": {},
    "Updates": {}
}

#                 +----------+
#                 |    Top   |
#         +------------+------------+
#         |            |            |
#         v            v            v
#     +-------+    +-------+    +-------+
#     | Reads |    |Deletes|    |Updates|
#     +-------+    +-------+    +-------+

lattices = {"Actors": Actors, "Resources": Resources, "Actions": Actions}

# policy:
#DENY
#EXCEPT
#  ALLOW Actors = Looker
#        Resources = CCN, EMAIL
#        Actions = Updates, Deletes
#  EXCEPT
#    DENY Actors = Bob
#         Resources = CCN
#         Actions = Deletes

clauses = [
    ("DENY", {'Actors': {"Top"}, 'Resources': {"Top"}, 'Actions': {"Top"}}, [
        ("ALLOW", {'Actors': {"Looker"}, 'Resources': {"CCN", "EMAIL"}, "Actions": {"Updates", "Deletes"}}, [
            ("DENY", {'Actors': {"Bob"}, 'Resources': {
             "CCN"}, "Actions": {"Deletes"}}, [])
        ])
    ])
]


def query(actor, action, resource):
  return [{'Actors': {actor}, 'Actions': {action}, 'Resources': {resource}}]


lgl = Legalease(lattices)
nodes = query("Bob", "Deletes", "CCN")
print(lgl.validate(nodes, clauses))
