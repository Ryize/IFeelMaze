from abc import ABC, abstractmethod
from typing import Union, Optional, Type

from game.abstract.abstract_effect import AbstractEffectType


class BaseCell(ABC):
    """
    Базовый класс клетки в лабиринте.
    """
    x: int  # Положение клетки по X
    y: int  # Положение клетки по Y
    visited: bool  # Посещена ли клетка при создании лабиринта
    user_visited: bool  # Посещена ли клетка игроков
    effects: list  # Эффекты клетки
    _walls: dict  # Словарь наличия стен

    @property
    def walls(self):
        return self._walls


class AbstractMaze(ABC):
    @abstractmethod
    def __init__(self, maze_size: int):
        pass

    @abstractmethod
    def generate(self) -> None:
        """
        Генерирует лабиринт, используя точки BaseCell.
        """
        pass

    @abstractmethod
    def get_standard_entry_point(self) -> BaseCell:
        """
        Получение стандартной точки в которой находится пользователь.
        """
        pass

    @abstractmethod
    def check_neighbors(self) -> Union[bool, BaseCell]:
        """
        Проверка соседних клеток. Если такие имеются - возвращает BaseCell,
        иначе False.
        """
        pass

    @abstractmethod
    def check_exist_not_visited_cell(self) -> bool:
        """
        Проверяет существование не посещённых клеток.
        """
        pass

    @abstractmethod
    def copy(self) -> 'AbstractMaze':
        """
        Копирует лабиринт.
        """
        pass

    @property
    @abstractmethod
    def current_cell(self) -> BaseCell:
        pass

    @current_cell.setter
    @abstractmethod
    def current_cell(self, cell: BaseCell):
        pass

    @property
    @abstractmethod
    def maze(self) -> list[BaseCell]:
        pass


class AbstractMazeGame(ABC):
    @abstractmethod
    def generate_maze(self) -> None:
        """
        Генерирует лабиринт используя AbstractMaze.
        """
        pass

    @abstractmethod
    def arrange_effects(self,
                        amount: int,
                        repeat: bool = True,
                        effect_types: list[
                            Optional[Type[AbstractEffectType]]] = None,
                        win: bool = True,
                        ) -> None:
        """
        Проставляет указанное количество эффектов на случайные клетки.
        """
        pass

    @abstractmethod
    def get_maze(self) -> AbstractMaze:
        """
        Получить объект лабиринта AbstractMaze.
        """
        pass

    @abstractmethod
    def set_maze(self, value: AbstractMaze) -> None:
        """
        Устанавливает новый лабиринт.
        """
        pass

    @abstractmethod
    def copy_maze(self) -> AbstractMaze:
        """
        Копирует лабиринт.
        """
        pass

    @abstractmethod
    def move_forward(self) -> Union[bool, BaseCell]:
        """
        Движение вперёд.
        """
        pass

    @abstractmethod
    def move_right(self) -> Union[bool, BaseCell]:
        """
        Движение вправо.
        """
        pass

    @abstractmethod
    def move_bottom(self) -> Union[bool, BaseCell]:
        """
        Движение вниз.
        """
        pass

    @abstractmethod
    def move_left(self) -> Union[bool, BaseCell]:
        """
        Движение влево.
        """
        pass

    @abstractmethod
    def check_move_forward(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вперёд.
        """
        pass

    @abstractmethod
    def check_move_right(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вправо.
        """
        pass

    @abstractmethod
    def check_move_back(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения вниз.
        """
        pass

    @abstractmethod
    def check_move_left(self) -> Union[bool, BaseCell]:
        """
        Проверка возможности движения влево.
        """
        pass
