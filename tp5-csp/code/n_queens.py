import argparse
import csv
import json
import math
import random
import sys

import backtracking
import forward


def initialize_board(size, seed, fixed_ratio=0.2):
    random.seed(seed)

    board = [list(range(size)) for _ in range(size)]
    if size <= 0:
        return board, {}, []

    num_fixed = max(1, math.ceil(size * fixed_ratio))
    num_fixed = min(num_fixed, size)

    target_columns = list(range(size))
    random.shuffle(target_columns)
    target_columns = target_columns[:num_fixed]

    assignment = {}

    def helper(index):
        if index == len(target_columns):
            return True

        column = target_columns[index]
        values = list(range(size))
        random.shuffle(values)

        for row in values:
            if all(
                assignment[prev_col] != row
                and abs(assignment[prev_col] - row) != abs(prev_col - column)
                for prev_col in assignment
            ):
                assignment[column] = row
                if helper(index + 1):
                    return True
                del assignment[column]

        return False

    def normalize_board():

        new_board = [[] for _ in range(size)]
        for col in range(size):
            if col in assignment:
                new_board[col] = assignment[col]
            else:
                new_board[col] = "?"
        return new_board
        
        

    if helper(0):
        for column, row in assignment.items():
            board[column] = [row]
    else:
        assignment = {}

    return board, assignment, normalize_board()


def format_board(board):
    return "[" + ", ".join("?" if cell == "?" else str(cell) for cell in board) + "]"


parser = argparse.ArgumentParser(description="N-Queens Problem Solver")
parser.add_argument("-size",required=True, type=int, help="Size of the chessboard (N x N)")
parser.add_argument("-seed",required=True, type=int, help="Random seed for reproducibility")
args = parser.parse_args()

size = args.size
seed = args.seed
board, fixed_assignment, board_to_show = initialize_board(size, seed)

#name, board, duration, states = backtracking.run(board, seed, fixed_assignment)
name, board, duration, states = forward.run(board, seed, fixed_assignment)

writer = csv.writer(sys.stdout)
writer.writerow([
    name,
    seed,
    size,
    format_board(board_to_show),
    json.dumps(board),
    duration,
    states,
])
