from abc import ABC, abstractmethod
from typing import Union


class BaseCell(ABC):
    """
    Базовый класс клетки в лабиринте.
    """
    x: int  # Положение клетки по X
    y: int  # Положение клетки по Y
    visited: bool  # Посещённость клетки
    effects: list  # Эффекты клетки


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


class AbstractMazeGame(ABC):
    @abstractmethod
    def generate_maze(self) -> None:
        """
        Генерирует лабиринт используя AbstractMaze.
        """
        pass

    @abstractmethod
    def get_maze(self) -> AbstractMaze:
        """
        Получить объект лабиринта AbstractMaze.
        """
        pass
