from src.exams.models import Exam, Problem, ProblemAttachment
from collections import OrderedDict

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


def is_cyclic(nodes):
    visited = [False] * len(nodes)
    recursion_stack = [False] * len(nodes)

    for i in range(len(nodes)):
        if not visited[i]:
            if is_cyclic_check(nodes[i], visited, recursion_stack, nodes, i):
                return True
    return False


def generate_knowledge_states(all_problems, start_problem, matrix, len_problems, curr_lst, visited_problems=[]):
        visited_problems.append(start_problem)
        pr_ats = ProblemAttachment.objects.filter(source=start_problem.id)
        temp_curr_lst = curr_lst.copy()
        if len(pr_ats) > 0:
            for p_a in pr_ats:
                pr = p_a.target
                temp_curr_lst[all_problems.index(pr)] = "1"
                curr_str = "".join(curr_lst)
                if curr_str not in matrix:
                    matrix.append(curr_str)
                generate_knowledge_states(all_problems, pr, matrix, len_problems, temp_curr_lst, visited_problems)
                temp_curr_lst = curr_lst.copy()
        else:
            temp_curr_lst[all_problems.index(start_problem)] = "1"
            curr_str = "".join(curr_lst)
            if curr_str not in matrix:
                matrix.append(curr_str)
        return matrix

def determine_next_question(answered_questions, choices, exam_id):
    exam = Exam.objects.get(id=exam_id)
    all_questions = list(exam.questions.all())
    all_question_ids = [q.id for q in all_questions]
    all_problems = list(Problem.objects.filter(question__in=all_question_ids))
    all_problem_ids = [p.id for p in all_problems]
    print(f"Problem ids {all_problem_ids}")
    len_problems = len(all_problems)
    start_problem = all_problems[0]
    curr_taken_idxs = [0]   # indexes of preconditions
    matrix = []
    # first problem can always be alone in a knowledge state
    matrix.append("1" + "0" * (len_problems - 1))
    curr_lst = ["0" for i in range(len_problems)]
    curr_lst[0] = "1"

    # 1. generate knowledge states
    matrix = generate_knowledge_states(all_problems, start_problem, matrix, len_problems, curr_lst)
    matrix.sort(key=lambda el: el.count("1"))
    print(f"Matrix of knowledge states {matrix}")

    # 2. set response patterns
    response_patterns = OrderedDict()
    # 3. do Markov
