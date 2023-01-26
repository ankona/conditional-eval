import typing as t
from graph import Node, Edge, execute_workflow, execute_stateless_workflow
from conditional import NumericalComparisonConditional, OrComparisonConditional, Unconditional
from state import InMemoryState

def build_mock_action(node_name: str) -> t.Union[t.Callable[..., None], None]:
    def _build_mock_action():
        print(f"\tExecuting mock action: {node_name}")
    return _build_mock_action

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
    a = Node("a", action=build_mock_action("START"))
    b = Node("b", action=build_mock_action("b"))
    c = Node("c", action=build_mock_action("c"))
    d = Node("d", action=build_mock_action("d"))
    e = Node("e", action=build_mock_action("e"))
    f = Node("f", action=build_mock_action("f"))
    g = Node("g", action=build_mock_action("g"))
    h = Node("h", action=build_mock_action("h"))
    i = Node("i", action=build_mock_action("STOP"))

    # Test a compound evaluator with a "hole"
    x1 = NumericalComparisonConditional("lt", 0.1)
    x2 = NumericalComparisonConditional("gt", 0.2)
    compound = OrComparisonConditional(x1, x2)

    # TODO: Complete AndConditional And Test value in the hole
    # TODO: Consider BetweenConditional or stick with construction using elementary operators?
    # h1 = NumericalComparisonConditional("gte", 0.1)
    # h2 = NumericalComparisonConditional("lte", 0.2)
    # and_compound = AndComparisonConditional(h1, h2)

    # ab = Edge(a, b, NumericalComparisonConditional("lte", 0.5))
    ab = Edge(a, b, compound)
    ac = Edge(a, c, NumericalComparisonConditional("gt", 0.5))

    # Testing edge case correctness (greater than or equal to)
    bd = Edge(b, e, NumericalComparisonConditional("lt", 0.2))
    be = Edge(b, e, NumericalComparisonConditional("gte", 0.2))

    # Testing fallthrough behavior
    cf = Edge(c, f, NumericalComparisonConditional("gt", 0.8))
    cg = Edge(c, g, NumericalComparisonConditional("gt", 0.7))
    ch = Edge(c, h, NumericalComparisonConditional("gt", 0.6))

    # Test unconditional traversal to end node
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
# execute_workflow(tc1, start_node)

mem_state = InMemoryState()

while next_node := execute_stateless_workflow(tc1, start_node, mem_state):
    ...
