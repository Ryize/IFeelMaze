import random
from typing import Union, Optional, Type

from game.abstract.abstract_effect import AbstractEffectType
from game.abstract.abstract_maze import BaseCell, AbstractMaze, AbstractMazeGame
from game.effects import FactoryEffects


class Cell(BaseCell):
    """
    Представляет клетку в лабиринте.

    Fields:
        x: int (координата X).
        y: int (координата Y).
        visited: bool (посещена ли клетка).
        _walls: dict (словарь наличия стен)
            key: str (всегда четыре ключа: top, bottom, left, right
             представляющих положение стены в клетке)
            value: bool (False - нет стены, True - есть стена).
    """

    def __init__(self, x: int, y: int):
        self.x = x  # координата X
        self.y = y  # координата Y
        self._walls = {  # словарь наличия стен
            'top': True,
            'right': True,
            'bottom': True,
            'left': True,
        }
        self.visited = False  # посещена ли клетка
        self.effects = []

    def remove_walls(self, *args) -> None:
        """
        Удаляет у клетки указанные стены.

        Принимает кортеж стен, элементы кортежа - ключи словаря _walls.
        Меняет значения указанных стен в словаре _walls на False.

        Args:
            args: tuple[str] (кортеж со стенами. Элементы кортежа - ключи
            имеющиеся в _walls: top, right, bottom, left).
        """
        for wall in args:
            if wall in self._walls:
                self._walls[wall] = False

    @property
    def walls(self):
        return self._walls

    def __repr__(self) -> str:
        """
        При вызове вернёт строку с координатами X и Y в формате (X;Y).

        Returns:
            str (строка в формате (X;Y)).
        """
        return f'({self.x};{self.y})'


class Maze(AbstractMaze):
    """
    Класс лабиринта.

    Создаёт лабиринт по размеру. Лабиринт квадратный.

    Позволяет:
    1) Сгенерировать лабиринт по указанному размеру (generate).
    2) Получить точку, в которой находится пользователь (get_entry_point).
    3) Проверить существует ли клетка (или она выходит за границы лабиринта)
       (check_cell).
    4) Проверить и получить случайную точку, соседнюю с той в которой сейчас
       находится пользователь (check_neighbors).
    5) Удалить стены, при переходе из текущей клетки в соседнюю (remove_walls).

    Fields:
        maze_size: int (размер лабиринта по X и Y).
        _maze: None | list (по умолчанию None. При генерации лабиринта хранит в
            виде списка клетки лабиринта (class Cell)).
        _current_cell: None | Cell (по умолчанию None. При генерации лабиринта
            хранит текущую клетку, на которой сейчас находится пользователь.
            При генерации лабиринта по умолчанию получает центральную по X
            точку и 0 по Y).
    """

    # По умолчанию None. При генерации лабиринта хранит в
    # виде списка клетки лабиринта (class Cell).
    _maze = None
    # По умолчанию None. При генерации лабиринта хранит текущую клетку, на
    # которой сейчас находится пользователь.
    _current_cell = None

    def __init__(self, maze_size: int, *args, **kwargs):
        self.maze_size = maze_size  # Размер лабиринта

    def generate(self) -> None:
        """
        Генерирует лабиринт.

        Создаёт поле _maze в виде списка и добавляет указанное число клеток
        (в maze_size). Т.е. в списке _maze будет maze_size * maze_size клеток.
        """
        self._maze = [Cell(x, y) for y in range(self.maze_size) for x in
                      range(self.maze_size)]
        # Получаем базовое положение пользователя в лабиринте
        cell = self.get_standard_entry_point()
        self._current_cell = cell

    def get_standard_entry_point(self) -> Cell:
        """
        Получает изначальное положение пользователя в лабиринте.

        Изначальное положение: центр лабиринта по X (self.maze_size // 2)
        и 0 по Y. Получается нижний центр.

        Returns:
            Cell: точка в которой по умолчанию находится пользователь.
        """
        for cell in self._maze:
            if cell.x == self.maze_size // 2 and cell.y == 0:
                return cell

    def check_cell(self, x: int, y: int) -> Union[bool, Cell]:
        """
        Проверяет существует ли клетка в лабиринте.

        Если не существует, возвращает False, в ином случае возвращает клетку.

        Args:
            x: int (координата X проверяемой клетки).
            y: int (координата Y проверяемой клетки).

        Returns:
            Union[False, Cell]:
                bool[False] - клетки с такими координатами нет в лабиринте.
                Cell - найденная клетка.
        """
        try:
            return self._maze[x + y * self.maze_size]
        except IndexError:
            return False

    def check_neighbors(self) -> Union[bool, Cell]:
        """
        Получение случайной соседней клетки.

        Получает случайную клетку, соседнюю с той на которой стоит
        пользователь, получаемая клетка не должна быть посещённой (visited).

        Returns:
            Union[False, Cell]:
                bool[False] - соседних, не посещённых клеток нет.
                Cell - случайная соседняя клетка.
        """
        # Получение верхней, правой, нижней, левой клетки
        all_neighbors = self.get_neighbors()

        neighbors = []
        top = all_neighbors['top']
        right = all_neighbors['right']
        bottom = all_neighbors['bottom']
        left = all_neighbors['left']
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        # Возвращаем случайную соседнюю клетку, если такой клетки нет, то False
        return random.choice(neighbors) if neighbors else False

    def get_neighbors(self) -> dict:
        """
        Возвращает словарь с клетками.

        Если клетки не существует, она будет False.

        Returns:
            dict: (словарь с клетками).
        """
        top = self.check_cell(self._current_cell.x, self._current_cell.y - 1)
        right = self.check_cell(self._current_cell.x + 1, self._current_cell.y)
        bottom = self.check_cell(self._current_cell.x,
                                 self._current_cell.y + 1)
        left = self.check_cell(self._current_cell.x - 1, self._current_cell.y)

        return {
            'top': top,
            'right': right,
            'left': left,
            'bottom': bottom,
        }

    def remove_walls(self, next_cell: Cell) -> None:
        """
        Удаляет стены у текущей и следующей клетки.

        Удаление стен может использоваться при переходе из одной клетки в
        другую.

        Args:
            next_cell: Cell (клетка в которую мы переходим).
        """
        current_cell = self.current_cell
        # Проверяем меняется ли координата X при переходе в другую клетку.
        dx = current_cell.x - next_cell.x
        # Переход в левую клетку
        if dx == 1:
            current_cell.remove_walls('left')
            next_cell.remove_walls('right')
        # Переход в правую клетку
        if dx == -1:
            current_cell.remove_walls('right')
            next_cell.remove_walls('left')

        dy = current_cell.y - next_cell.y
        # Переход в верхнюю клетку
        if dy == 1:
            current_cell.remove_walls('top')
            next_cell.remove_walls('bottom')
        # Переход в нижнюю клетку
        if dy == -1:
            current_cell.remove_walls('bottom')
            next_cell.remove_walls('top')

    def check_exist_not_visited_cell(self) -> bool:
        """
        Проверяет есть ли в лабиринте не посещённые клетки.

        Returns:
            bool:
                True - Есть.
                False - Нет.
        """
        for cell in self._maze:
            if not cell.visited:
                return True
        return False

    def copy(self) -> AbstractMaze:
        """
        Копирует лабиринт.

        Возвращает точную копию лабиринта. Является прототипом

        Returns:
            AbstractMaze: новый лабиринт
        """
        new_obj = self.__class__(**self.__dict__)
        new_obj.__dict__.update(self.__dict__)
        return new_obj

    @property
    def current_cell(self):
        return self._current_cell

    @current_cell.setter
    def current_cell(self, cell: Cell):
        self._current_cell = cell

    @property
    def maze(self):
        return self._maze


class MazeGame(AbstractMazeGame):
    """
    Класс реализующий игру лабиринт.

    Генерирует лабиринт (Maze) и создаёт пути.
    Генерация лабиринта происходит по алгоритму обхода в ширину.

    Fields:
        maze_size: int (размер лабиринта по X и Y)
        __maze: Maze (объект класса Maze)
    """

    def __init__(self, maze_size: int = 16):
        """
        Args:
            maze_size: int (размер лабиринта по X и Y)
        """
        self.maze_size = maze_size
        # Получаем объект Maze и генерируем лабиринт
        self.__maze = Maze(maze_size)
        self.__maze.generate()

    def generate_maze(self) -> None:
        """
        Создаёт игровой лабиринт.

        Изменяет стандартный лабиринт генерируемый классом Maze так, что из
        клетки можно попасть в любую другую клетку. Для этого используется
        алгоритм обхода в ширину.
        """
        maze = self.__maze
        # Стек посещённых клеток. Нужен для ситуации если нет соседних клеток,
        # но ещё не все клетки посещены, тогда мы будем брать поочерёдно
        # каждый элемент стека и искать его соседей до тех пор, пока не найдём
        # или не переберём весь лабиринт.
        _last_cell = []
        while self.__maze.check_exist_not_visited_cell():
            next_cell = maze.check_neighbors()
            if next_cell:
                # Если у текущей клетки есть не посещённая соседняя, переходим
                # в неё, помечаем как посещённую. Также добавляем текущую
                # клетку в стек посещённых клеток.
                next_cell.visited = True
                _last_cell.append(maze.current_cell)
                maze.remove_walls(next_cell)
                maze.current_cell = next_cell
            elif _last_cell:
                # Если у текущей клетки нет не посещённых соседних, то
                # откатываемся на предыдущую вершину. Действие повторяется до
                # тех пор, пока не будет найдена клетка у которой есть
                # не посещённые соседние клетки.
                cell = _last_cell.pop()
                maze.current_cell = cell

    def arrange_effects(self,
                        amount: int,
                        repeat: bool = True,
                        effect_types: list[
                            Optional[Type[AbstractEffectType]]] = None,
                        win: bool = True,
                        ) -> None:
        """
        Проставляет указанное количество эффектов на случайные клетки.

        Args:
            amount: int (количество эффектов)
            repeat: bool (может ли быть несколько эффектов на одной клетке)
            effect_types: list[Optional[AbstractEffectType]] (использовать
            только эффекты из указанных категорий)
            win: bool (добавить эффект победы в лабиринте)
        """
        current_cell = self.__maze.current_cell
        all_cells = self.__maze.maze.copy()
        if effect_types:
            effects = FactoryEffects.get_effects_by_type(effect_types)
        else:
            effects = FactoryEffects.get_effects()
        i = 0
        while i < amount:
            cell = random.choice(all_cells)
            if abs(current_cell.x - cell.x) > 2 or abs(
                    current_cell.y - cell.y) > 2:
                effect = random.choice(effects)
                if effect in cell.effects:
                    continue
                cell.effects.append(effect)
                if not repeat:
                    all_cells.remove(cell)
                i += 1
            else:
                all_cells.remove(cell)
        if win:
            all_cells = self.__maze.maze.copy()
            while all_cells:
                cell = random.choice(all_cells)
                if abs(current_cell.x - cell.x) > 3 and abs(
                        current_cell.y - cell.y) > 3 and not cell.effects:
                    cell.effects.append(FactoryEffects.get_win_effect())
                    break
                all_cells.remove(cell)

    def check_move_forward(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вперёд.

        Можно двигаться если клетка существует, и между ними нет стены.

        Returns:
            BaseCell: проверяемая клетка
            bool:
                False - двигаться нельзя
        """
        return self._check_move('top')

    def check_move_right(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вправо.

        Можно двигаться если клетка существует, и между ними нет стены.

        Returns:
            BaseCell: проверяемая клетка
            bool:
                False - двигаться нельзя
        """
        return self._check_move('right')

    def check_move_back(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вниз.

        Можно двигаться если клетка существует, и между ними нет стены.

        Returns:
            BaseCell: проверяемая клетка
            bool:
                False - двигаться нельзя
        """
        return self._check_move('bottom')

    def check_move_left(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения влево.

        Можно двигаться если клетка существует, и между ними нет стены.

        Returns:
            BaseCell: проверяемая клетка
            bool:
                False - двигаться нельзя
        """
        return self._check_move('left')

    def _check_move(self, direction: str) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения в указанную сторону.

        Можно двигаться если клетка существует, и между ними нет стены.

        Args:
            direction: str (сторона, может быть: top, right, bottom, left)

        Returns:
            BaseCell: проверяемая клетка
            bool:
                False - двигаться нельзя
        """
        cell = self.__maze.get_neighbors()[direction]
        if not (cell.walls.get(direction, True) or
                self.__maze.current_cell.walls.get(direction, True)):
            return cell
        return False

    def move_forward(self) -> Union[bool, BaseCell]:
        """
        Движение вперёд.

        Перед движением проверяет, можно ли двигаться.

        Returns:
            BaseCell: клетка на которую переместились
            bool:
                False - движения не произошло
        """
        return self._move('top')

    def move_right(self) -> Union[bool, BaseCell]:
        """
        Движение вправо.

        Перед движением проверяет, можно ли двигаться.

        Returns:
            BaseCell: клетка на которую переместились
            bool:
                False - движения не произошло
        """
        return self._move('right')

    def move_bottom(self) -> Union[bool, BaseCell]:
        """
        Движение вниз.

        Перед движением проверяет, можно ли двигаться.

        Returns:
            BaseCell: клетка на которую переместились
            bool:
                False - движения не произошло
        """
        return self._move('bottom')

    def move_left(self) -> Union[bool, BaseCell]:
        """
        Движение влево.

        Перед движением проверяет, можно ли двигаться.

        Returns:
            BaseCell: клетка на которую переместились
            bool:
                False - движения не произошло
        """
        return self._move('left')

    def _move(self, direction: str) -> Union[bool, BaseCell]:
        """
        Позволяет двигаться на соседнюю клетку.

        Перед движением проверяет, можно ли двигаться.
        Для проверки используется _check_move.

        Args:
            direction: str (сторона, может быть: top, right, bottom, left)

        Returns:
            BaseCell: клетка на которую переместились
            bool:
                False - движения не произошло
        """
        if self.check_move_forward():
            forward_cell = self.__maze.get_neighbors()[direction]
            self.__maze.current_cell = forward_cell
            return forward_cell
        return False

    def copy_maze(self) -> AbstractMaze:
        """
        Копирует лабиринт.

        Возвращает точную копию текущего лабиринта.

        Returns:
             AbstractMaze: созданный лабиринт.
        """
        return self.__maze.copy()

    def get_maze(self) -> Maze:
        """
        Возвращает объект Maze.

        Returns:
            Maze.
        """
        return self.__maze


maze = MazeGame(9)
maze.generate_maze()
maze.arrange_effects(10)
for i in maze._MazeGame__maze._maze:
    if i.effects:
        print(i, i.effects)
