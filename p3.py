from copy import deepcopy

infile = r"E:\test.txt"

state = []
explored = []
frontier = []
node_tolid_shode = 0
node_bast_dade_shode = 0

def print_state(printed_state):
    for column in range(k):
        if printed_state[column][0]:
            for indd in range(len(printed_state[column][0])):
                print(printed_state[column][0][indd], end='')
                print(printed_state[column][1][indd], end='')
                print(" ", end='')
            print(" ")
        else:
            print('#')
    print("depth = ", end='')
    print(printed_state[k])
    print(" ")


def move_to_next_state(st1, mv):
    st = deepcopy(st1)
    source_column = mv[0]
    destination_column = mv[1]
    # number
    st[destination_column][0].append(st[source_column][0][-1])
    # column
    st[destination_column][1].append(st[source_column][1][-1])
    st[source_column][0].pop(-1)
    st[source_column][1].pop(-1)
    return st


def goal_check(st):
    nums_sorted = [False] * (len(st) - 2)
    same_color = [False] * (len(st) - 2)
    for index in range(len(st) - 2):
        nums = st[index][0][:]
        if len(nums) == 0:
            same_color[index] = True
            nums_sorted[index] = True
            continue
        if len(nums) != n:
            return False
        cols = st[index][1][:]
        nums.sort(reverse=True)
        if nums == st[index][0]:
            nums_sorted[index] = True
        same_color[index] = all(elem == st[index][1][0] for elem in cols)
    final_num_check = all(elem == True for elem in nums_sorted)
    final_color_check = all(elem == True for elem in same_color)
    if final_color_check and final_num_check:
        return True
    return False

def next_moves_function(st):
    possible_moves = []
    for column in range(len(st) - 2):
        if st[column][0]:
            last_card_num = st[column][0][-1]
            for col in range(len(st) - 2):
                if col != column:
                    if st[col][0]:
                        if last_card_num < st[col][0][-1]:
                            # we have a move now
                            possible_moves.append([column, col])
                    else:
                        possible_moves.append([column, col])
    return possible_moves

def heuristic_calculate(st):
    g = 0
    for d in range(len(st)-2):
        changed = False
        column_current_length = len(st[d][0])
        # column length
        if column_current_length > n:
            g = g + (column_current_length - n)
        # order of the numbers
        for c in range(len(st[d][0])):
            if st[d][0] and st[d][0][c] != (n - c):
                g = g + (len(st[d][0]) - c)
                changed = True
                break
        # colors
        if not changed and st[d][1]:
            for c in range(1, len(st[d][1])):
                if st[d][1][c] != st[d][1][c-1]:
                    g = g + (len(st[d][0]) - c)
                    break
    return g

def a_star(st):
    global node_tolid_shode
    global node_bast_dade_shode
    global frontier
    done = False
    while not done:
        next_moves = next_moves_function(st)
        for ind in range(len(next_moves)):
            tmp_state = move_to_next_state(st, next_moves[ind])
            # graph search
            tmp_state[k] = tmp_state[k] + 1
            tmp_state[k+1] = deepcopy(st)
            flag_in_explored = False
            for s in explored:
                flag = True
                for c in range(k):
                    if s[c] != tmp_state[c]:
                        flag = False
                        break
                if flag:
                    flag_in_explored = True
                    break
            if flag_in_explored:
                continue

            flag_in_frontier = False
            for s in frontier:
                flag = True
                for c in range(k):
                    if s[c] != tmp_state[c]:
                        flag = False
                        break
                if flag:
                    flag_in_frontier = True
                    the_state = s
                    break
            if flag_in_frontier:
                # heuristics are equal
                # should just go for tmp_state[k]
                if tmp_state[k] < the_state[k]:  # is this incorrect?!
                    frontier.remove(the_state)
                    frontier.append(deepcopy(tmp_state))
                continue
            frontier.append(deepcopy(tmp_state))
            node_tolid_shode += 1

        # get the state with the minimum f + g
        min_value_state = frontier[0]
        for s in frontier:
            cost = heuristic_calculate(s)+s[k]
            min_cost = heuristic_calculate(min_value_state) + min_value_state[k]
            if cost < min_cost:
                min_value_state = s
        node_bast_dade_shode += 1
        if goal_check(min_value_state):
            print("done!")
            print(f"node tolid shode: {node_tolid_shode}")
            print(f"node bast dade shode: {node_bast_dade_shode}")
            printed_states = []
            the_s = deepcopy(min_value_state)
            while the_s[k + 1] != 0:
                printed_states.append(the_s)
                the_s = the_s[k + 1]
            q = len(printed_states) - 1
            print_state(init_state)
            while q >= 0:
                # print(printed_states[q][0:6])
                print_state(printed_states[q])
                q -= 1
            break

        explored.append(deepcopy(min_value_state))
        frontier.remove(min_value_state)
        st = min_value_state


# reading and processing the inputs
with open(infile) as f:
    k, m, n = [int(inp) for inp in next(f).split()]
    for i in range(k):
        j = 0
        tmp = []
        numbers = []
        colors = []
        card = [inp for inp in next(f).split()]
        if card != ['#']:
            for j in range(len(card) - 1):
                color = card[j][-1]
                number = card[j][0:-1]
                colors.append(color)
                numbers.append(int(number))
            if len(card) >= 1:
                if len(card) == 1:
                    j = j - 1
                card[j + 1] = card[j + 1].split("\n")[0]
                color = card[j + 1][-1]
                number = card[j + 1][0:-1]
                colors.append(color)
                numbers.append(int(number))
        tmp.append(numbers)
        tmp.append(colors)
        state.append(tmp)
# appending depth
state.append(0)
# appending the parent
state.append(0)
init_state = deepcopy(state)
r = heuristic_calculate(state)
a_star(state)
