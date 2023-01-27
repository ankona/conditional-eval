from graph import Node, Edge 
from workflow.linear import execute_stateless_workflow as linear_workflow
from conditional import NumericalComparisonConditional, OrComparisonConditional, Unconditional
from state import InMemoryState
from behavior import PrintBehavior, PublishBehavior, CompoundBehavior, CallbackBehavior

def build_demo_graph() -> Node:
    """ Build a demo graph and return the start node """
    # Example Graph Layout
    #    ,b-----d
    #   / \      \
    #  /   \      \  
    # a     `e-----\    
    #  \            \  
    #   \    ,f-----/i      
    #    \  /      /   
    #     `c--g---/
    #       \    /
    #        \  /
    #         `h

    # Demonstrate that the action can be anything
    eb1 = PrintBehavior("e")
    eb2 = PublishBehavior("e")
    compound_behavior = CompoundBehavior(eb1, eb2)

    end1 = PrintBehavior("STOP (i)")
    end2 = CallbackBehavior("https://api.clientcompany.com/callback")
    end_behavior = CompoundBehavior(end1, end2)

    a = Node("a", action=PrintBehavior("START (a)"))
    b = Node("b", action=PublishBehavior("b"))
    c = Node("c", action=PublishBehavior("c"))
    d = Node("d", action=PublishBehavior("d"))
    e = Node("e", action=compound_behavior)
    f = Node("f", action=PublishBehavior("f"))
    g = Node("g", action=PublishBehavior("g"))
    h = Node("h", action=PublishBehavior("h"))
    i = Node("i", action=end_behavior)

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

    d.edges.append(di)
    e.edges.append(ei)
    f.edges.append(fi)
    g.edges.append(gi)
    h.edges.append(hi)

    return a

tc1 = [0.05, 0.2, 0, 0]
tc2 = [0.51, 0.61, 0, 0]

start_node = build_demo_graph()
# execute_workflow(tc1, start_node)

mem_state = InMemoryState()

while next_node := linear_workflow(tc1, start_node, mem_state):
    ...
