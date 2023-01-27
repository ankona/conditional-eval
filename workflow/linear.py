from graph import Node
from state import StateHolder

def execute_stateless_workflow(inputs, head: Node, state: StateHolder):
    """ A workflow that maintains no local state & greedily executes 
    the first traversable branch encountered out of each node """
    pos = -1
    spos = state.get('_pos')
    if spos is not None and spos > -1:
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


