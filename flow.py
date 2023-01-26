from graph import Node, Edge, execute_workflow
from conditional import NumericalComparisonConditional, OrComparisonConditional, Unconditional

def build_demo_graph() -> Node:
    """ Build a demo graph and return the start node """
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

    return a

tc1 = [0.05, 0.2, 0, 0]
tc2 = [0.51, 0.61, 0, 0]

start_node = build_demo_graph()
execute_workflow(tc1, start_node)
