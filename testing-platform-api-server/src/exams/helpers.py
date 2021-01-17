from src.exams.models import Exam, Problem, ProblemAttachment,\
    ActualProblemAttachment, Question
from collections import OrderedDict
import random


def find_problem_level_actual(problem, level):
    if not problem.actual_source_problems.first():
        return level

    return find_problem_level_actual(problem.actual_source_problems.first().source, level + 1)


def order_questions_actual(question):
    return find_problem_level_actual(question.problem, 0)


def find_problem_level_expected(problem, level):
    if not problem.source_problems.first():
        return level

    return find_problem_level_expected(problem.source_problems.first().source, level + 1)


def order_questions_expected(question):
    return find_problem_level_expected(question.problem, 0)


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


def get_inverse_problem_attachment(pr_att, is_actual=False):
    """E.g. for (3, 1) get (1, 3)
    """
    src, trg = pr_att.source.id, pr_att.target.id
    if is_actual:
        p_a = ActualProblemAttachment.objects.filter(source=trg, target=src)
    else:
        p_a = ProblemAttachment.objects.filter(source=trg, target=src)
    if len(p_a) > 0:
        p_a = p_a[0]
    else:
        p_a = None
    return p_a


def generate_knowledge_states(all_problems, start_problem, state_matrix,
                              len_problems, curr_lst, visited_problem_attachments=set(),
                              is_actual=False):
    if not is_actual:
        pr_atts = ProblemAttachment.objects.filter(source=start_problem.id)
    else:
        pr_atts = ActualProblemAttachment.objects.filter(source=start_problem.id)

    visited_problem_attachments.update([pr_att.id for pr_att in pr_atts])
    # print(f"Visited edges {visited_problem_attachments}")
    # print(f"Start problem {start_problem} {start_problem.id}")
    temp_curr_lst = curr_lst.copy()
    if len(pr_atts) > 0:
        for p_a in pr_atts:
            pr = p_a.target
            temp_curr_lst[all_problems.index(pr)] = "1"
            curr_str = "".join(curr_lst)
            if curr_str not in state_matrix:
                state_matrix.append(curr_str)
            # avoid infinite recursion
            inverse_p_a = get_inverse_problem_attachment(p_a, is_actual)
            if not inverse_p_a or (inverse_p_a and inverse_p_a.id not in visited_problem_attachments):
                generate_knowledge_states(all_problems, pr, state_matrix,
                                          len_problems, temp_curr_lst, visited_problem_attachments)
            temp_curr_lst = curr_lst.copy()
    else:
        temp_curr_lst[all_problems.index(start_problem)] = "1"
        curr_str = "".join(curr_lst)
        if curr_str not in state_matrix:
            state_matrix.append(curr_str)
    return state_matrix


def guess_current_state(all_questions, answered_questions, choices):
    """Guess current state by checking which questions were answered correctly

    Args:
        answered_questions (list): list of all questions
        answered_questions (list): list of objects/answered questions

    Returns:
        string: the guessed current state
    """
    current_state = ["0" for _ in range(len(all_questions))]
    for i in range(len(all_questions)):
        q = all_questions[i]
        a_q = None
        # get question from answered_questions - necessary because of choices
        for question in answered_questions:
            if question["id"] == q.id:
                a_q = question
                break
        if a_q is not None:
            actual_num_correct_answers = len([choice for choice in
                                              q.choices.all() if choice.correct_answer])
            to_add = "1"    # "1" if the question was answered correctly, "0" otherwise
            num_correct_answers = 0
            for c in a_q["choices"]:
                ''' if the student hasn't answered a question correctly, perhaps they
                should be served that question again, hence the 0 gets added, i.e. the
                system pretends that the user hasn't already answered that question
                '''
                if c["id"] in choices:
                    if not c["correct_answer"]:
                        to_add = "0"
                        break
                    else:
                        num_correct_answers += 1
                else:
                    # a correct answer has not been selected => 0 points for question
                    if c["correct_answer"]:
                        to_add = "0"
                        break
            # not all correct answers were selected
            if num_correct_answers < actual_num_correct_answers:
                to_add = "0"
            current_state[i] = to_add
    return "".join(current_state)


def update_likelihoods_per_response_patterns(state_matrix, response_patterns, num_response_patterns):
    """Update likelihoods per response patterns for current exam. In other words,
    take into account how other students have performed on this exam in the past
    when calculating likelihoods per state.

    Args:
        state_matrix (string): binary string, e.g. "100000"
        response_patterns (dict): dictionary of state/num_correct_answers pairs
        num_response_patterns (int): number of response patterns

    Returns:
        dict: state/likelihood pairs
    """
    states_likelihoods = OrderedDict()
    for state in state_matrix:
        numerator = 1
        numerator += response_patterns[state]
        states_likelihoods[state] = round(numerator / num_response_patterns, 2)
    # sort by values descending, i.e. by likelihoods
    states_likelihoods = OrderedDict(sorted(states_likelihoods.items(),
                                     key=lambda t: t[1], reverse=True))
    return states_likelihoods


def update_likelihoods_for_current_state(states_likelihoods, current_state):
    num_answered = current_state.count("1")
    # compare states_likelihoods with current_state
    for state, likelihood in states_likelihoods.items():
        # severely decrease chance of landing in state with 2+ question diff
        if state.count("1") > num_answered + 1:
            states_likelihoods[state] *= 0.7

        for i in range(len(current_state)):
            if current_state[i] == state[i]:
                states_likelihoods[state] *= 1.1
            else:
                states_likelihoods[state] *= 0.9
    # only keep states with a likelihood greater than 0
    states_likelihoods = {k: round(v, 2) for k, v in states_likelihoods.items() if v > 0}
    return states_likelihoods


def update_likelihoods_per_number_of_students_in_state(states_likelihoods, exam_results):
    """Increase the likelihood of all states that have a student in them.
    This function is called once every time an exam is taken,
    before the first question is loaded.
    """
    for e_r in exam_results:
        if e_r.state in states_likelihoods:
            states_likelihoods[e_r.state] = round(states_likelihoods[e_r.state] * 1.1, 2)
    return states_likelihoods


def determine_next_question(answered_questions, choices, exam_id, states_likelihoods):
    answered_questions_ids = [a_q["id"] for a_q in answered_questions]
    exam = Exam.objects.get(id=exam_id)
    all_questions = list(exam.questions.all())
    # don't repeat questions
    next_q_candidates = Question.objects.filter(exam=exam).exclude(id__in=answered_questions_ids)
    print(f"Next question candidates {next_q_candidates}")
    all_question_ids = [q.id for q in all_questions]
    all_problems = list(Problem.objects.filter(question__in=all_question_ids))
    all_problem_ids = [p.id for p in all_problems]
    print(f"Problem ids for this exam: {all_problem_ids}")

    # do Markov
    current_state = guess_current_state(all_questions, answered_questions, choices)
    print(f"Guessed current state {current_state}")
    states_likelihoods = update_likelihoods_for_current_state(states_likelihoods, current_state)
    states_likelihoods = OrderedDict(sorted(states_likelihoods.items(),
                                     key=lambda t: t[1], reverse=True))
    print(f"states_likelihoods after update based on current state {states_likelihoods}")

    for state, likelihood in states_likelihoods.items():
        # small chance of a lucky guess, copying or an accidental mistake
        if random.random() < 0.1:
            print("Random has prevailed")
            continue
        else:
            for i in range(len(state)):
                ''' if question in state and question unanswered or
                answered incorrectly and question is candidate
                '''
                if state[i] == "1" and current_state[i] == "0" and\
                   all_questions[i] in next_q_candidates:
                    print(f"i1 {i} Next question {all_questions[i]}")
                    return all_questions[i], states_likelihoods

    # swords are of no use here, for random is too powerful...
    chosen = next(iter(states_likelihoods))     # get state w/ highest likelihood
    for i in range(len(chosen)):
        if chosen[i] == "1" and current_state[i] == "0" and all_questions[i] in next_q_candidates:
            print(f"i2 {i} Next question {all_questions[i]}")
            return all_questions[i], states_likelihoods
