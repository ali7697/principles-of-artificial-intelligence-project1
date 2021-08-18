from copy import deepcopy

initial_limit = 0
infile = r"E:\test.txt"
        
lines = []
state = []
explored = []
frontier = []
done = False
cont = 0
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

def depth_limited_search(st, lim):
    return recursive_dls(st, lim)

def recursive_dls(st, lim):
    global node_bast_dade_shode
    global node_tolid_shode
    node_bast_dade_shode +=1
    if goal_check(st):
        return st
    else:
        if lim == 0:
            return 0  # cut-off
        else:
            cutoff_occurred = False
            next_moves = next_moves_function(st)
            node_tolid_shode += len(next_moves)
            for ind in range(len(next_moves)):
                child = move_to_next_state(st, next_moves[ind])
                # depth of the child should be handeled
                child[-2] = child[-2] + 1
                child[-1] = st
                result = recursive_dls(child, lim - 1)
                if result == 0:
                    cutoff_occurred = True
                else:
                    if result != -1:
                        return result
            if cutoff_occurred:
                return 0
            else:
                return -1  # failure


def iterative_deepening_search(st):
    global node_tolid_shode
    global node_bast_dade_shode
    depth = initial_limit
    while True:
        result = depth_limited_search(st, depth)
        if result != 0:
            return result
        depth = depth + 1



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


# reading and processing the inputs
with open(infile) as f:
    k, m, n = [int(x) for x in next(f).split()]
    for i in range(k):
        j = 0
        tmp = []
        numbers = []
        colors = []
        card = [x for x in next(f).split()]
        if card != ['#']:
            for j in range(len(card) - 1):
                color = card[j][-1]
                number = card[j][0:-1]
                colors.append(color)
                numbers.append(number)
            if len(card) >= 1:
                if len(card) == 1:
                    j = j - 1
                card[j + 1] = card[j + 1].split("\n")[0]
                color = card[j + 1][-1]
                number = card[j + 1][0:-1]
                colors.append(color)
                numbers.append(number)
        tmp.append(numbers)
        tmp.append(colors)
        state.append(tmp)
# appending depth
state.append(0)
init_state = deepcopy(state)
# appending the parent
state.append(0)


ress = iterative_deepening_search(state)
print(f"node tolid shode: {node_tolid_shode}")
print(f"node bast dade shode: {node_bast_dade_shode}")
print(" ")
# print_state(ress)
printed_states = []
the_s = deepcopy(ress)
while the_s[k + 1] != 0:
    printed_states.append(the_s)
    the_s = the_s[k + 1]
    q = len(printed_states) - 1
print_state(init_state)
while q >= 0:
    print_state(printed_states[q])
    q -= 1