from puzzle import move, display
from copy import deepcopy

my_board = [[4, None, 7, 5], [8, 9, 13, 6], [15, 3, 10, 1], [12, 2, 14, 11]]
moves = [7, 13, 10, 1, 6, 10, 1, 3, 9, 1, 3, 9, 15, 8, 4, 7, 1, 4, 7, 1, 4, 3, 9, 15, 2, 12, 8, 7, 3, 2, 15, 9, 13, 4, 2, 3, 7, 15, 9, 13, 3, 7, 15, 9, 13, 14, 11, 6, 10, 5, 4, 3]

def process(board=my_board, moves=moves):
    temp_board = deepcopy(board)
    for tile in moves:
        move(tile, temp_board)
    return temp_board


if __name__ == "__main__":
    for tile in moves:
        move(tile, my_board)
    display(my_board)
