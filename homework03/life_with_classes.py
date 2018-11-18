from pygame.locals import *
import random
import copy
import pygame
from copy import deepcopy


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480,
                 cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        cell_list = CellList(self.cell_height, self.cell_width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            self.draw_cell_list(cell_list)
            # Выполнение одного шага игры (обновление состояния ячеек)
            cell_list.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist: "CellList") -> None:
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде
        матрицы
        """

        for cell in clist:
            a = cell.row * self.cell_size + 1
            b = cell.col * self.cell_size + 1
            c = self.cell_size - 1
            d = self.cell_size - 1
            color_cell = pygame.Color('white')
            if cell.is_alive():
                color_cell = pygame.Color('green')
            pygame.draw.rect(self.screen, color_cell, Rect(a, b, c, d))


class Cell:

    def __init__(self, row: int, col: int, state: bool =False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int,
                 randomize: bool = False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.grid = []
        if randomize:
            self.grid = [[Cell(i, j, bool(random.randint(0, 1)))
                          for j in range(ncols)]
                         for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j, bool(0))
                          for j in range(ncols)]
                         for i in range(nrows)]

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        col, row = cell.col, cell.row
        for r in range(row - 1, row + 2):
            for p in range(col - 1, col + 2):
                if r in range(0, self.nrows) and p in range(0, self.ncols)\
                        and (p != col or r != row):
                    neighbours.append(self.grid[r][p])
        return neighbours

    def update(self):
        new_clist = copy.deepcopy(self.grid)
        for cell in self:
            num = sum(i.is_alive() for i in self.get_neighbours(cell))
            if num != 2 and num != 3:
                new_clist[cell.row][cell.col].state = False
            elif num == 3:
                new_clist[cell.row][cell.col].state = True
        self.grid = new_clist
        return self

    def __iter__(self):
        self.r, self.p = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.r < self.nrows:
            cell = self.grid[self.r][self.p]
            self.p += 1
            if self.p == self.ncols:
                self.r += 1
                self.p = 0
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if (self.grid[i][j].alive):
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename: str) -> "CellList":
        with open(filename, 'r') as file:
            grid = []
            row = 0
            col = 0
            for r in file:
                line = []
                for c in r:
                    if c == '0':
                        line.append(Cell(row, col, False))
                    if c == '1':
                        line.append(Cell(row, col, True))
                    col += 1
                ncol = col
                col = 0
                grid.append(line)
            for line in grid:
                for cell in line:
                    cell.row = row
                row += 1

            cell_list = CellList(row, ncol, False)
            cell_list.grid = grid
            return cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
