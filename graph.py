import typing as t
from conditional import Conditional
from state import StateHolder
from behavior import Behavior

class Node:
    def __init__(self, key: str, action: t.Optional[Behavior] = None):
        self._next = None
        self._key = key
        self.edges: t.List[Edge] = []
        self.action = action

    @property
    def key(self) -> str:
        return self._key

    def next(self, input) -> "Node|None":
        """ Check outgoing edges for a traversable exit. """
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
        """ Evaluate the attached conditional and return true if it passes """
        return self._cond.evaluate(input=input)

def execute_workflow(inputs, head: Node):
    """ Traverse the workflow """
    pos = -1

    if node := head:
        if node.action:
            node.action()

    while node:
        pos += 1
        v = inputs[pos]
        if node := node.next(v):
            if node.action:
                node.action()
    
    print("workflow complete")


def execute_stateless_workflow(inputs, head: Node, state: StateHolder):
    """ Demonstrate storing workflow state externally during traversal """
    pos = -1
    if spos := state.get('_pos'):
        pos = spos

    snode = state.get('_node')
    if snode:
        node = snode
    else:
        if node := head:
            if node.action:
                node.action()

    pos += 1
    v = inputs[pos]

    sibling = node.next(v)
    state.set('_node', sibling)
    state.set('_pos', pos)

    if sibling and sibling.action:
        sibling.action()
    
    return sibling
