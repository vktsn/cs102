from typing import List, Union, Optional
import random


def read_sudoku(filename: str) -> list:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: list) -> None:
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
                      ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: list, n: int) -> list:
    return [values[i:i + n] for i in range(0, len(values)-1, n)]


def get_row(values: list, pos: tuple) -> list:
    row, _ = pos
    return values[row]


def get_col(values: list, pos: tuple) -> list:
    _, col = pos
    return [values[row][col] for row in range(len(values))]


def get_block(values: list, pos: tuple) -> list:
    row, col = pos
    br = 3 * (row // 3)
    bc = 3 * (col // 3)
    return [values[br+r][bc+c] for r in range(3) for c in range(3)]


def find_empty_positions(grid: list) -> Union[tuple, None]:
    for col in range(len(grid)):
        for row in range(len(grid)):
            if grid[row][col] == '.':
                return (row, col)
    return None


def find_possible_values(grid: list, pos: tuple) -> set:
    return set('123456789') - \
        set(get_row(grid, pos)) - \
        set(get_col(grid, pos)) - \
        set(get_block(grid, pos))


def solve(grid: list) -> Union[list, None]:
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[row][col] = '.'
    return None


def check_solution(solution: list) -> bool:
    for row in range(len(solution)):
        row_values = set(get_row(solution, (row, 0)))
        if row_values != set('123456789'):
            return False

    for col in range(len(solution)):
        col_values = set(get_col(solution, (0, col)))
        if col_values != set('123456789'):
            return False

    for row in (0, 3, 6):
        for col in (0, 3, 6):
            blk_values = set(get_block(solution, (row, col)))
            if blk_values != set('123456789'):
                return False

    return True


def generate_sudoku(n: int) -> list:
    grid = solve([['.'] * 9 for _ in range(9)])
    N = 81 - min(81, max(0, N))
    while N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            N -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
        
