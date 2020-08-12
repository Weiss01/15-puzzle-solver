from collections import deque
from copy import deepcopy
from random import randint
from puzzle import display, move, generate_board
from process import process
from time import time, sleep
from os import system

def get_position(item, board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == item:
                return i, j


def convert_path_to_position(path, board):
    res = []
    for tile in path:
        res.append(get_position(tile, board))
    return res


def neighbours(v, board):
    i, j = get_position(v, board)
    res = []
    if i != 0: res.append(board[i-1][j])
    if i != 3: res.append(board[i+1][j])
    if j != 0: res.append(board[i][j-1])
    if j != 3: res.append(board[i][j+1])
    return res


def random_path(board, start, goal, exclude=[]):
    visited = set()
    boundary = [start]
    parent = {}
    while len(boundary) > 0:
        v = boundary.pop(randint(0, len(boundary)-1))
        visited.add(v)
        if v == goal:
            path = deque([v])
            while True:
                path.appendleft(parent[v])
                v = parent[v]
                if v == start:
                    return list(path)
        for w in neighbours(v, board):
            if w not in visited and w not in exclude:
                parent[w] = v
                boundary.append(w)


def mirror(counterpart, c_board, target):
    i, j = get_position(counterpart, c_board)
    return target[i][j]


def custom_path_fix(board, target):
    i, j = get_position(target, board)
    temp_board = deepcopy(board)
    # print(temp_board, target)
    res = []
    res += [temp_board[i-1][j-1]]
    move(temp_board[i-1][j-1], temp_board)
    res += [temp_board[i-1][j]]
    move(temp_board[i-1][j], temp_board)
    res += [temp_board[i][j]]
    move(temp_board[i][j], temp_board)
    res += [temp_board[i][j+1]]
    move(temp_board[i][j+1], temp_board)
    res += [temp_board[i-1][j+1]]
    move(temp_board[i-1][j+1], temp_board)
    res += [temp_board[i-1][j-1]]
    move(temp_board[i-1][j-1], temp_board)
    res += [temp_board[i][j-1]]
    move(temp_board[i][j-1], temp_board)
    # res += [temp_board[i][j]]
    # move(temp_board[i][j], temp_board)
    # res += [temp_board[i-1][j]]
    # move(temp_board[i-1][j], temp_board)
    # res += [temp_board[i-1][j+1]]
    # move(temp_board[i-1][j+1], temp_board)
    return res


def complete_fix(board, target):
    i, j = get_position(target, board)
    temp_board = deepcopy(board)
    res = []
    res += [temp_board[i-1][j-1]]
    move(temp_board[i-1][j-1], temp_board)
    res += [temp_board[i-1][j]]
    move(temp_board[i-1][j], temp_board)
    res += [temp_board[i][j]]
    move(temp_board[i][j], temp_board)
    res += [temp_board[i][j+1]]
    move(temp_board[i][j+1], temp_board)
    res += [temp_board[i-1][j+1]]
    move(temp_board[i-1][j+1], temp_board)
    res += [temp_board[i-1][j-1]]
    move(temp_board[i-1][j-1], temp_board)
    res += [temp_board[i][j-1]]
    move(temp_board[i][j-1], temp_board)
    res += [temp_board[i][j]]
    move(temp_board[i][j], temp_board)
    res += [temp_board[i-1][j]]
    move(temp_board[i-1][j], temp_board)
    res += [temp_board[i-1][j+1]]
    move(temp_board[i-1][j+1], temp_board)
    return res


def backtracking(solution, board, exclude=[], part=[]):
    def complete(part):
        my_board = deepcopy(board)
        for tile in part:
            move(tile, my_board)
        if 'T' in solution[1] and my_board[solution[0]][solution[1].index('T')+1:len(solution[1])] == solution[1][solution[1].index('T')+1:]:
            return True
        elif my_board[solution[0]][:len(solution[1])] == solution[1]:
            return True
        else:
            return False

    def options(part):
        my_board = deepcopy(board)
        for tile in part:
            move(tile, my_board)

        start, goal = '', ''
        for index, tile in enumerate(my_board[solution[0]]):
            if tile != solution[1][index]:
                if solution[1][index] == 'T':
                    continue
                goal = solution[1][index]
                break
        c_board = []
        for i in range(4):
            if i == solution[0]:
                c_board.append(solution[1])
            else:
                c_board.append(['', '', '', ''])

        try:
            none_path = []
            pre = []
            if random_path(my_board, goal, mirror(goal, c_board, my_board), exclude+solution[1][:index]) == None:
                # print("pre -> ", pre)
                pre = custom_path_fix(my_board, goal)
            none_path = random_path(process(my_board, pre), goal, mirror(goal, c_board, my_board), exclude+solution[1][:index])[1:]
        except Exception as e:
            # display(my_board)
            # print("start -> ", goal, "\ngoal -> ", mirror(goal, c_board, my_board), "\nexclude -> ", exclude, solution[1][:index])
            raise e

        full_path = []
        res = []
        # for times in range(1):
        temp_board = []
        temp_board = deepcopy(my_board)
        for i, j in convert_path_to_position(pre + none_path, temp_board):
            try:
                if goal == None:
                    unit_path = random_path(temp_board, None, temp_board[i][j], exclude+[goal]+solution[1][:index])[1:]
                else:
                    if random_path(temp_board, None, temp_board[i][j], exclude+[goal]+solution[1][:index]) == None:
                        unit_path = complete_fix(temp_board, goal)
                    else:
                        unit_path = random_path(temp_board, None, temp_board[i][j], exclude+[goal]+solution[1][:index])[1:] + [goal]
            # except TypeError as e:
            #     print('TypeError')
            #     unit_path = []
            except KeyError as e:
                unit_path = [goal]
            for tile in unit_path:
                move(tile, temp_board)
            full_path += unit_path
        res.append(full_path) # [[1,2,3,4,5,6]]
        if res == [[]]:
            return []
        return res


    if complete(part):
        return [part]
    else:
        res = []
        for o in options(part):
            res += backtracking(solution, board, exclude, part + o)
            if len(res) > 0:
                break
        return res


def main(board):
        my_board = board
        a = backtracking([0, [1, 2, 3]], my_board)
        q =  process(my_board, a[0])
        if q[0] != [1, 2, 3, 4]:
            b = []
            if q[0][3] == None and q[1][3] == 4:
                b = [a[0] + [4]]
            else:
                b = backtracking([1, ['T', None, 4]], my_board, [1, 2, 3], a[0])
                q =  process(my_board, b[0])
                b[0] += [2, 3, 4, q[1][3], q[0][3], 3, 2]
        else:
            b = a
        c = backtracking([1, [5, 6, 7]], my_board, [1, 2, 3, 4], b[0])
        q =  process(my_board, c[0])
        if q[1] != [5, 6, 7, 8]:
            d = []
            if q[1][3] == None and q[2][3] == 8:
                d = [a[0] + [8]]
            else:
                d = backtracking([2, ['T', None, 8]], my_board, [1, 2, 3, 4, 5, 6, 7], c[0])
                q =  process(my_board, d[0])
                d[0] += [6, 7, 8, q[2][3], q[1][3], 7, 6]
        else:
            d = c
        q =  process(my_board, d[0])
        if q[0] != [1,2,3,4] or q[1] != [5,6,7,8]:
            # print("NO LOL")
            return "NO LOL"

        e = backtracking([2, [9, 10]], my_board, [1, 2, 3, 4, 5, 6, 7, 8], d[0])
        f = backtracking([3, [None]], my_board, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], e[0])
        f = [f[0] + [9, 10]]

        g = backtracking([2, [10, 11, 12]], my_board, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], f[0])
        h = backtracking([3, [9, None]], my_board, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], g[0])
        h = [h[0] + [11, 12]]

        i = backtracking([2, [10, 12, None, 15]], my_board, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], h[0])

        i = [i[0] + [12, 11, 14, 15, 10, 9, 15]]

        return i[0]


def solve(board):
    try:
        ans = main(board)
        if ans == "NO LOL":
            return "I'm not solving for you you fucking noob"
        else: return ans
    except Exception as e:
        return "I'm not solving for you you fucking trash"


the_board = generate_board()
start = time()
ans = solve(the_board)
for tile in ans:
    # system('cls')
    print("MOVE -> ", tile)
    move(tile, the_board)
    display(the_board)
    # sleep(0.01)
end = time()
print(f"Time -> {end - start}s")




#
