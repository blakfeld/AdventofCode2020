#!/usr/bin/env python

import sys

from dataclasses import dataclass, field
from functools import reduce


TREE = '#'
CLEAR = '.'
SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]


@dataclass
class GameBoard(object):
    grid: list = field(default_factory=list)

    def get_point(self, x, y):
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        return self.grid[y % rows][x % cols]

    @staticmethod
    def of_file(input_file):
        with open(input_file, 'r') as f:
            grid = []
            for line in f:
                cols = list(line.strip())
                grid.append(cols)

        return GameBoard(grid=grid)


def count_trees_in_path(board, slope):
    x, y = 0, 0
    slope_right, slope_down = slope

    trees = 0
    while y < len(board.grid):
        if board.get_point(x, y) == TREE:
            trees += 1

        x += slope_right
        y += slope_down

    return trees


def main():
    input_path = sys.argv[1]
    board = GameBoard.of_file(input_path)

    print('Part One:')
    p1_result = count_trees_in_path(board, (3, 1))

    print('Tree Count: {}'.format(p1_result))
    print()

    print('Part Two')
    tree_counts = list(map(lambda s: count_trees_in_path(board, s), SLOPES))
    print(tree_counts)
    p2_result = 1
    for count in tree_counts:
        p2_result *= count

    print('Tree Counts: {}'.format(p2_result))
    print()


if __name__ == '__main__':
    main()
