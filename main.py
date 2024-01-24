import random
from typing import Union


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True,
        }
        self.visited = False

    def remove_walls(self, *args):
        for wall in args:
            self._walls[wall] = False

    def __repr__(self) -> str:
        return f'({self.x};{self.y})'


class Maze:
    _maze = None
    _current_cell = None

    def __init__(self, max_size: int):
        self.max_size = max_size

    def generate(self) -> None:
        self._maze = [Cell(x, y) for y in range(self.max_size) for x in
                      range(self.max_size)]
        cell = self.get_entry_point()
        self._current_cell = cell

    def get_entry_point(self) -> Cell:
        for cell in self._maze:
            if cell.x == self.max_size // 2 and cell.y == 0:
                return cell

    def check_cell(self, x: int, y: int) -> Union[bool, Cell]:
        try:
            return self._maze[x + y * self.max_size]
        except IndexError:
            return False

    def check_neighbors(self) -> Union[bool, Cell]:
        top = self.check_cell(self._current_cell.x, self._current_cell.y - 1)
        right = self.check_cell(self._current_cell.x + 1, self._current_cell.y)
        bottom = self.check_cell(self._current_cell.x,
                                 self._current_cell.y + 1)
        left = self.check_cell(self._current_cell.x - 1, self._current_cell.y)

        neighbors = []
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return random.choice(neighbors) if neighbors else False

    def remove_walls(self, next_cell: Cell):
        current_cell = self.current_cell
        dx = current_cell.x - next_cell.x
        if dx == 1:
            current_cell.remove_walls('left')
            next_cell.remove_walls('right')
        if dx == -1:
            current_cell.remove_walls('right')
            next_cell.remove_walls('left')

        dy = current_cell.y - next_cell.y
        if dy == 1:
            current_cell.remove_walls('top')
            next_cell.remove_walls('bottom')
        if dy == -1:
            current_cell.remove_walls('bottom')
            next_cell.remove_walls('top')

    @property
    def current_cell(self):
        return self._current_cell

    @current_cell.setter
    def current_cell(self, cell: Cell):
        self._current_cell = cell


class MazeGame:
    def __init__(self, maze_size: int = 16):
        self.maze_size = maze_size
        self.__maze = Maze(maze_size)
        self.__maze.generate()

    def generate_maze(self):
        maze = self.__maze
        _last_cell = []
        for i in range(self.maze_size ** 2):
            next_cell = maze.check_neighbors()
            if next_cell:
                next_cell.visited = True
                _last_cell.append(maze.current_cell)
                maze.remove_walls(next_cell)
                maze.current_cell = next_cell
            elif _last_cell:
                cell = _last_cell.pop()
                maze.current_cell = cell


maze = MazeGame(6)
maze.generate_maze()
for i in maze._MazeGame__maze._maze:
    print(i._walls)
