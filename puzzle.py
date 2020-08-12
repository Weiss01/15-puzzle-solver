from random import choice
from time import time
from copy import deepcopy
from os import system
solution = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, None]
]


def solve(board):
	for i in range(2):
		for j in range(len(board)):
			while board[i][j] != solution[i][j]:
				position = get_position(solution[i][j])
				correct_path = [6, 10, 11, 3]


def get_empty_coordinate(board, tile=None):
    res = {}
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == tile:
                res['row'] = i
                res['col'] = j
                break
        if len(res) == 2:
            break
    return res

def generate_board():
    my_board = deepcopy(solution)
    for i in range(200):
        coordinate = get_empty_coordinate(my_board)
        pool = []
        for i, row in enumerate(my_board):
            if i == coordinate['row']:
                pool.extend(row)
            for j, item in enumerate(row):
                if j == coordinate['col']:
                    pool.append(item)
        move(choice(pool), my_board)
    display(my_board)
    return my_board

def is_valid_move(instruction, board, stack):
    if instruction.upper() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'Z'] and len(instruction) != 0:
        return False
    if instruction.upper() == 'Z' and len(stack) == 0:
        return False
    res =  True
    if instruction.upper() != 'Z':
        coordinate = get_empty_coordinate(board)
        my_position = get_empty_coordinate(board, int(instruction))
        if my_position['col'] != coordinate['col'] and my_position['row'] != coordinate['row']:
            res = False
    return res

def display(board):
    for row in board:
        for item in row:
            if item == None:
                print(f'|{" ":^4}', end = '')
            else:
                print(f'|{item:^4}', end = '')
        print('|')
    print('')


def move(tile, board):
    coordinate = get_empty_coordinate(board)
    my_position = get_empty_coordinate(board, tile)
    if my_position['col'] == coordinate['col']:
        if my_position['row'] < coordinate['row']: # move down
            for i in range(coordinate['row'], my_position['row'], -1):
                board[i][coordinate['col']], board[i-1][coordinate['col']] = board[i-1][coordinate['col']], board[i][coordinate['col']]
        elif my_position['row'] > coordinate['row']: # move up
            for i in range(coordinate['row'], my_position['row']):
                board[i][coordinate['col']], board[i+1][coordinate['col']] = board[i+1][coordinate['col']], board[i][coordinate['col']]
    elif my_position['row'] == coordinate['row']:
        if my_position['col'] < coordinate['col']:
            for i in range(coordinate['col'], my_position['col'], -1):
                board[coordinate['row']][i], board[coordinate['row']][i-1] = board[coordinate['row']][i-1], board[coordinate['row']][i]
        elif my_position['col'] > coordinate['col']:
            for i in range(coordinate['col'], my_position['col']):
                board[coordinate['row']][i], board[coordinate['row']][i+1] = board[coordinate['row']][i+1], board[coordinate['row']][i]
# [[7, None, 15, None, 4, 11, 10, 5, 8, None, 8, None, 8, 4, 4, None, 4, 11, 8, None]]
if __name__ == "__main__":
    my_board = [[4, None, 7, 5], [8, 9, 13, 6], [15, 3, 10, 1], [12, 2, 14, 11]]
    my_stack = []
    start = time()
    while not my_board == solution:
        system('cls')
        print([9, 13, 10, 1, 6, 10, 1, 6, 10, 1, 7, 5, 1, 7, 5, 1, 7, 5, 13, 9, 1, 13, 9, 8, 4, 1, 8, 3, 2, 12, 15, 4, 3, 8, 13, 9, 6, 2, 8, 13, 9, 7, 5, 10, 2, 6, 10, 2, 6, 8, 13, 10, 2, 5, 7, 2, 10, 9, 2, 7, 5, 6, 8, 13, 4, 3, 9, 10, 13, 4, 3, 9, 10, 3, 4, 13, 3, 4, 13, 8, 6, 5, 7, 3, 4])
        display(my_board)
        instruction = input('\nEnter move: ')
        while not is_valid_move(instruction, my_board, my_stack):
            print('Invalid move!')
            instruction = input('Reenter move: ')
        if instruction.upper() == 'Z':
            my_board = my_stack.pop()
        elif int(instruction) in range(1, 16):
            my_stack.append(deepcopy(my_board))
            move(int(instruction), my_board)
    end = time()
    print('CONGRATULATIONS!!!')
    print(f'TIME TAKEN = {round(end - start, 3)}s')
