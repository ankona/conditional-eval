import typing as t

class Conditional(t.Protocol):
    def evaluate(**kwargs) -> bool:
        ...
    
    def operators(self) -> t.List[str]:
        ...


class NumericalComparisonConditional(Conditional):
    def __init__(self, op: str, sentinel: float):
        self._operator = op
        self._sentinel = sentinel

    def operators(self) -> t.List[str]:
        return ["lt", "gt", "eq", "lte", "gte"]

    def evaluate(self, input) -> bool:
        if self._operator == "lt":
            output = input < self._sentinel
            log = f"Numerical({input} < {self._sentinel} == {output})"
        elif self._operator == "gt": 
            output = input > self._sentinel
            log = f"Numerical({input} > {self._sentinel} == {output})"
        elif self._operator == "gte":
            output = input >= self._sentinel
            log = f"Numerical({input} >= {self._sentinel} == {output})"
        elif self._operator == "lte":
            output = input <= self._sentinel
            log = f"Numerical({input} <= {self._sentinel} == {output})"
        else:
            output = input == self._sentinel
            log = f"Numerical({input} = {self._sentinel} == {output})"
        
        print(f'{log} {"succeeds" if output else "fails"}')
        return output


class OrComparisonConditional(Conditional):
    def __init__(self, c_lhs: Conditional, c_rhs: Conditional):
        self._lhs = c_lhs
        self._rhs = c_rhs

    def operators(self) -> t.List[str]:
        return []

    def evaluate(self, input) -> bool:
        if self._lhs.evaluate(input=input) or self._rhs.evaluate(input=input):
            print("Or compound comparison succeeds")
            return True
        
        print("Or compound comparison fails")
        return False


class Unconditional(Conditional):
    def __init__(self):
        ...
    
    def evaluate(self, input) -> bool:
        print("Unconditional comparison succeeds")
        return True
    
    def operators(self) -> t.List[str]:
        return []


class Node:
    def __init__(self, key: str):
        self._next = None
        self._key = key
        self.edges: t.List[Edge] = []

    @property
    def key(self) -> str:
        return self._key

    def next(self, input) -> "Node|None":
        for edge in self.edges:
            if edge.is_traversable(input):
                print(f"Traversing to {edge._rhs.key}")
                return edge._rhs

        return None


class Edge:
    def __init__(self, lhs: Node, rhs: Node, cond: Conditional):
        self._lhs = lhs
        self._rhs = rhs
        self._cond = cond

    def is_traversable(self, input) -> bool:
        return self._cond.evaluate(input=input)


a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")
f = Node("f")
g = Node("g")
h = Node("h")
i = Node("i")
j = Node("j")

# Example Graph Layout
#    ,b-----e
#   / \      \
#  /   \      \  
# a     `d-----\    
#  \            \  
#   \    ,f-----/i      
#    \  /      /   
#     `c--g---/
#       \    /
#        \  /
#         `h

x1 = NumericalComparisonConditional("lt", 0.1)
x2 = NumericalComparisonConditional("gt", 0.2)

compound = OrComparisonConditional(x1, x2)

# ab = Edge(a, b, NumericalComparisonConditional("lte", 0.5))
ab = Edge(a, b, compound)
ac = Edge(a, c, NumericalComparisonConditional("gt", 0.5))

bd = Edge(b, e, NumericalComparisonConditional("lt", 0.2))
be = Edge(b, e, NumericalComparisonConditional("gte", 0.2))

cf = Edge(c, f, NumericalComparisonConditional("gt", 0.8))
cg = Edge(c, g, NumericalComparisonConditional("gt", 0.7))
ch = Edge(c, h, NumericalComparisonConditional("gt", 0.6))

bi = Edge(b, i, Unconditional())
ci = Edge(c, i, Unconditional())
di = Edge(d, i, Unconditional())
ei = Edge(e, i, Unconditional())
fi = Edge(f, i, Unconditional())
gi = Edge(g, i, Unconditional())
hi = Edge(h, i, Unconditional())

a.edges.append(ab)
a.edges.append(ac)

b.edges.append(bd)
b.edges.append(be)

c.edges.append(cf)
c.edges.append(cg)
c.edges.append(ch)

b.edges.append(bi)
c.edges.append(ci)
d.edges.append(di)
e.edges.append(ei)
f.edges.append(fi)
g.edges.append(gi)

tc1 = [0.05, 0.2, 0, 0]
tc2 = [0.51, 0.61, 0, 0]

def execute_workflow(inputs, start: Node):
    node = start
    i = -1

    while node:
        i += 1
        v = inputs[i]
        node = node.next(v)
    
    print('workflow complete')
            
execute_workflow(tc1, a)
