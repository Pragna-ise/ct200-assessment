def assign_parents(nodes):

    stack = []

    for node in nodes:

        while stack and stack[-1].level >= node.level:
            stack.pop()

        node.parent = stack[-1].title if stack else None

        stack.append(node)

    return nodes