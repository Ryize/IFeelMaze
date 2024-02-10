from abc import ABC, abstractmethod
from typing import Union, Optional

from game.abstract.abstract_maze import AbstractMazeGame, BaseCell


class AbstractRoom(ABC):
    """
    Класс комнат для прохождения лабиринта.

    В каждой комнате будет свой лабиринт и определённое число участников.
    Является классом посредником (Mediator).

    Fields:
        room_number: str (номер комнаты)
        maze: AbstractMazeGame (объект игрового лабиринта)
        participants: dict (участники комнаты)
    """
    room_number: str
    maze: AbstractMazeGame
    __participants: dict

    @abstractmethod
    def __init__(self, maze: AbstractMazeGame):
        """
        Создаёт комнату.
        """
        pass

    @abstractmethod
    def add_participant(self, participant_id: Union[int, str]) -> None:
        """
        Добавить участника в комнату.
        """
        pass

    @abstractmethod
    def set_participant_name(self,
                             participant_id: Union[int, str],
                             name: str
                             ) -> None:
        """
        Установить имя участника.
        """
        pass

    @abstractmethod
    def set_participant_surname(self,
                                participant_id: Union[int, str],
                                surname: str
                                ) -> None:
        """
        Установить фамилию участника.
        """
        pass

    @abstractmethod
    def remove_participant(self, participant_id: Union[int, str]) -> None:
        """
        Удалить участника из комнаты.
        """
        pass

    @abstractmethod
    def check_participants(self,
                           participant_id: Union[int, str]
                           ) -> Union[bool, 'AbstractRoom']:
        """
        Проверяет состоит ли указанный участник в комнате.
        """
        pass

    @abstractmethod
    def get_end_time_participant(self,
                                 participant_id: Union[int, str]
                                 ) -> Union[bool, float]:
        """
        Возвращает время окончания игры для указанного участника.
        Если участника нет в комнате, вернёт False.
        """
        pass

    @abstractmethod
    def set_end_time_participant(self,
                                 participant_id: Union[int, str],
                                 time_end: float,
                                 ) -> bool:
        """
        Устанавливает время окончания игры для указанного участника.
        Если участника нет в комнате, вернёт False.
        """
        pass

    @abstractmethod
    def get_previous_cells_participant(self,
                                       participant_id: Union[int, str]
                                       ) -> Union[bool, list]:
        """
        Возвращает список с посещёнными клетками для указанного участника.
        Если участника нет в комнате, вернёт False.
        """
        pass

    @abstractmethod
    def add_previous_cells_participant(self,
                                       participant_id: Union[int, str],
                                       cell: BaseCell,
                                       ) -> bool:
        """
        Добавляет клетку в список посещённых для указанного участника.
        """
        pass

    @abstractmethod
    def pop_previous_cells_participant(self,
                                       participant_id: Union[int, str],
                                       ) -> Union[bool, BaseCell]:
        """
        Удаляет и возвращает последнюю добавленную клетку.
        Если участника нет в комнате, вернёт False.
        """
        pass

    @abstractmethod
    def get_participant(self,
                        participant_id: Union[int, str],
                        ) -> Union[bool, dict]:
        """
        Возвращает словарь с данными участника.
        """
        pass

    @abstractmethod
    def get_participants(self,
                         ) -> Optional[dict]:
        """
        Возвращает словарь всех участников комнаты
        """
        pass

    @abstractmethod
    def get_start_time_participant(self,
                                   participant_id: Union[int, str]
                                   ) -> Union[bool, float]:
        """
        Возвращает время начала игры для указанного участника.
        """
        pass

    @abstractmethod
    def set_start_time_participant(self,
                                   participant_id: Union[int, str],
                                   time_start: float,
                                   ) -> bool:
        """
        Устанавливает время начала игры для указанного участника.
        """

    @abstractmethod
    def get_game_time_participant(self,
                                  participant_id: Union[int, str]
                                  ) -> Union[bool, float]:
        """
        Возвращает игровое время для указанного участника.
        """
        pass

    @abstractmethod
    def set_game_time_participant(self,
                                  participant_id: Union[int, str],
                                  time_: float,
                                  ) -> bool:
        """
        Устанавливает игровое время для указанного участника.
        """
        pass

    @abstractmethod
    def add_game_time_participant(self,
                                  participant_id: Union[int, str],
                                  time_: float,
                                  ) -> bool:
        """
        Добавляет игровое время для указанного участника.
        """
        pass


class AbstractRoomAggregator(ABC):
    """
    Нужен для агрегации работы со множеством комнат.
    Также является фасадом упрощающим взаимодействие с AbstractRoom.

    Fields:
        _rooms: list (список комнат)
        __room_class: AbstractRoom (класс комнаты)
        __maze_game_class: AbstractMazeGame (класс игрового лабиринта)
    """
    _rooms: list
    __room_class: AbstractRoom
    __maze_game_class: AbstractMazeGame

    @abstractmethod
    def create_room(self) -> AbstractRoom:
        """
        Создаёт и возвращает комнату.
        """
        pass

    @abstractmethod
    def remove_room(self, room_number: str) -> bool:
        """
        Удаляет комнату.
        """
        pass

    @abstractmethod
    def join_room_participant(self, room_number: str,
                              participant_id: Union[int, str],
                              name: str,
                              surname: str,
                              ) -> bool:
        """
        Добавляет участника в комнату.
        """
        pass

    @abstractmethod
    def leave_room_participant(self, room_number: str,
                               participant_id: Union[int, str]
                               ) -> bool:
        """
        Удаляет участника из комнаты.
        """
        pass

    @abstractmethod
    def get_room(self, room_number: str) -> Optional[AbstractRoom]:
        """
        Возвращает комнату по номеру.
        """
        pass

    @abstractmethod
    def get_room_by_participant(self,
                                participant_id: Union[int, str],
                                ) -> Optional[str]:
        """
        Возвращает номер комнаты по участнику.
        """
        pass

    @abstractmethod
    def get_participant(self,
                        participant_id: Union[int, str]
                        ) -> Optional[dict]:
        """
        Возвращает данные участника по его номеру
        """
        pass

    @abstractmethod
    def get_participants(self,
                         room_number: str,
                         ) -> Optional[dict]:
        """
        Возвращает словарь всех участников комнаты
        """
        pass

    @abstractmethod
    def get_start_time_participant(self,
                                   participant_id: Union[int, str]
                                   ) -> Union[bool, float]:
        """
        Возвращает время начала игры для указанного участника.
        """
        pass

    @abstractmethod
    def set_start_time_participant(self,
                                   participant_id: Union[int, str],
                                   time_start: float,
                                   ) -> bool:
        """
        Устанавливает время начала игры для указанного участника.
        """

    @abstractmethod
    def get_game_time_participant(self,
                                  participant_id: Union[int, str]
                                  ) -> Union[bool, float]:
        """
        Возвращает игровое время для указанного участника.
        """
        pass

    @abstractmethod
    def set_game_time_participant(self,
                                  participant_id: Union[int, str],
                                  time_: float,
                                  ) -> bool:
        """
        Устанавливает игровое время для указанного участника.
        """
        pass

    @abstractmethod
    def add_game_time_participant(self,
                                  participant_id: Union[int, str],
                                  time_: float,
                                  ) -> bool:
        """
        Добавляет игровое время для указанного участника.
        """
        pass

    @abstractmethod
    def get_maze_by_participant_id(self,
                                   participant_id: Union[int, str]
                                   ) -> Optional[AbstractMazeGame]:
        """
        Возвращает игровой лабиринт для указанного участника.
        """
        pass

    def __new__(cls) -> 'AbstractRoomAggregator':
        """
        Singleton, тк агрегатор единый для всей системы.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
