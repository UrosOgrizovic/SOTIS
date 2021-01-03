def find_problem_level(problem, level):
    if not problem.source_problems.first():
        return level

    return find_problem_level(problem.source_problems.first().source, level + 1)


def order_questions(question):
    return find_problem_level(question.problem, 0)


def is_cyclic_check(node, visited, recursion_stack, nodes, index):
    # Mark current node as visited and
    # adds to recursion stack
    visited[index] = True
    recursion_stack[index] = True

    # Recur for all neighbors
    # if any neighbor is visited and in
    # recStack then graph is cyclic

    for neighbor in node["neighbors"]:
        idx = 0
        neighbor_node = {}
        # neighbor has to be full node, not just index
        for i in range(len(nodes)):
            if nodes[i]['id'] == neighbor:
                idx = i
                neighbor_node = nodes[i]
                break
        if not visited[idx]:
            if is_cyclic_check(neighbor_node, visited, recursion_stack, nodes, idx):
                return True
        elif recursion_stack[idx]:
            return True

    # The node needs to be popped from
    # recursion stack before function ends
    recursion_stack[index] = False
    return False

def is_cyclic(self, nodes):
    visited = [False] * len(nodes)
    recursion_stack = [False] * len(nodes)

    for i in range(len(nodes)):
        if not visited[i]:
            if is_cyclic_check(nodes[i], visited, recursion_stack, nodes, i):
                return True
    return False
