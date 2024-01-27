import random
from typing import Union, Optional

from database.abstract.abstract_room import AbstractRoom, \
    AbstractRoomAggregator
from game.abstract.abstract_maze import AbstractMazeGame, BaseCell
from game.maze import MazeGame


class Room(AbstractRoom):
    """
    Класс комнат для прохождения лабиринта.

    В каждой комнате будет свой лабиринт и определённое число участников.

    Fields:
        room_number: str (номер комнаты)
        maze: AbstractMazeGame (объект игрового лабиринта)
        participants: dict (участники комнаты)
    """

    def __init__(self, maze: AbstractMazeGame):
        self.maze = maze
        self.room_number = str(random.randint(1000000, 999999999))
        self.__participants = {}

    def add_participant(self, participant_id: Union[int, str]) -> None:
        """
        Добавить участника в комнату.

        Args:
            participant_id: Union[int, str] (номер участника, может быть числом
            или строкой)
        """
        self.__participants[participant_id] = {
            'end_time': None,
            'previous_cells': [],
            'name': None,
            'last_name': None,
            'maze': self.maze.copy(),
        }

    def remove_participant(self, participant_id: Union[int, str]) -> None:
        """
        Удалить участника из комнаты.

        Args:
            participant_id: Union[int, str] (номер участника, может быть числом
            или строкой)
        """
        self.__participants.pop(participant_id)

    def check_participants(self,
                           participant_id: Union[int, str]
                           ) -> Union[bool, 'AbstractRoom']:
        """
        Проверяет состоит ли указанный участник в комнате.

        Args:
            participant_id: Union[int, str] (номер участника)

        Returns:
            AbstractRoom: комната в которой состоит участник.
            bool:
                False - не состоит.
        """
        return self.__participants.get(participant_id)

    def get_end_time_participant(self,
                                 participant_id: Union[int, str]
                                 ) -> Union[bool, float]:
        """
        Возвращает время окончания игры для указанного участника.

        Если участника нет в комнате, вернёт False.

        Args:
            participant_id: Union[int, str] (номер участника)

        Returns:
            float: оставшееся время
            bool:
                False - не состоит в комнате
        """
        if self.check_participants(participant_id):
            return self.__participants[participant_id]['end_time']
        return False

    def set_end_time_participant(self,
                                 participant_id: Union[int, str],
                                 time_end: float,
                                 ) -> bool:
        """
        Устанавливает время окончания игры для указанного участника.

        Если участника нет в комнате, вернёт False.

        Args:
            participant_id: Union[int, str] (номер участника)
            time_end: float (время окончания игры)

        Returns:
            bool:
                True - время установлено
                False - не состоит в комнате
        """
        if self.check_participants(participant_id):
            self.__participants[participant_id]['end_time'] = time_end
            return True
        return False

    def get_previous_cells_participant(self,
                                       participant_id: Union[int, str]
                                       ) -> Union[bool, list]:
        """
        Возвращает список с посещёнными клетками для указанного участника.

        Если участника нет в комнате, вернёт False.

        Args:
            participant_id: Union[int, str] (номер участника)

        Returns:
            list: список клеток
            bool:
                False - не состоит в комнате
        """
        if self.check_participants(participant_id):
            return self.__participants[participant_id]['previous_cells']
        return False

    def add_previous_cells_participant(self,
                                       participant_id: Union[int, str],
                                       cell: BaseCell,
                                       ) -> bool:
        """
        Добавляет клетку в список посещённых для указанного участника.

        Args:
            participant_id: Union[int, str] (номер участника)
            cell: BaseCell (клетка)

        Returns:
            bool:
                True - клетка добавлена
                False - не состоит в комнате
        """
        if self.check_participants(participant_id):
            self.__participants[participant_id]['previous_cells'].append(cell)
            return True
        return False

    def pop_previous_cells_participant(self,
                                       participant_id: Union[int, str],
                                       ) -> Union[bool, BaseCell]:
        """
        Удаляет и возвращает последнюю добавленную клетку.

        Если участника нет в комнате, вернёт False.

        Args:
            participant_id: Union[int, str] (номер участника)

        Returns:
            BaseCell: удалённая клетка
            bool:
                False - не состоит в комнате
        """
        if self.check_participants(participant_id):
            return self.__participants[participant_id]['previous_cells'].pop()
        return False

    def set_participant_name(self,
                             participant_id: Union[int, str],
                             name: str
                             ) -> bool:
        """
        Установить имя участника.

        Args:
            participant_id: Union[int, str] (номер участника)
            name: str (имя участника)

        Returns:
            bool:
                True - имя установлено
                False - участника с таким номером нет в комнате
        """
        if self.check_participants(participant_id):
            self.__participants[participant_id]['name'] = name
            return True
        return False

    def set_participant_surname(self,
                                participant_id: Union[int, str],
                                surname: str
                                ) -> bool:
        """
        Установить фамилию участника.

        Args:
            participant_id: Union[int, str] (номер участника)
            surname: str (фамилия участника)

        Returns:
            bool:
                True - фамилия установлена
                False - участника с таким номером нет в комнате
        """
        if self.check_participants(participant_id):
            self.__participants[participant_id]['surname'] = surname
            return True
        return False

    def get_participant(self,
                        participant_id: Union[int, str],
                        ) -> Optional[dict]:
        """
        Возвращает словарь с данными участника.

        Args:
            participant_id: Union[int, str] (номер участника)

        Returns:
            None: участник не найден
            dict: словарь с данными
        """
        return self.__participants.get(participant_id)

    def get_participants(self) -> Optional[dict]:
        """
        Возвращает идентификатор всех участников комнаты.

        Args:
            room_number: str (номер комнаты)

        Returns:
            list: список идентификаторов участников
            None: комната не найдена
        """
        return self.__participants


class RoomAggregator(AbstractRoomAggregator):
    """
    Нужен для агрегации работы со множеством комнат.

    Является посредником взаимодействия контроллер-комната и хранилищем комнат.

    Fields:
        _rooms: list (список комнат)
         __room_class: AbstractRoom (класс комнаты)
        __maze_game_class: AbstractMazeGame (класс игрового лабиринта)
    """
    _rooms: list[AbstractRoom] = []
    __room_class = Room
    __maze_game_class = MazeGame

    def create_room(self) -> str:
        """
        Создаёт и возвращает комнату.

        Returns:
            str: номер комнаты.
        """
        room = self.__room_class(self.__maze_game_class())
        while room.room_number in [existing_room.room_number for
                                   existing_room in self._rooms]:
            del room
            room = self.__room_class(self.__maze_game_class())
        self._rooms.append(room)
        return room.room_number

    def get_room(self, room_number: str) -> Optional[AbstractRoom]:
        """
        Возвращает комнату по номеру.

        Args:
            room_number: str (номер комнаты).

        Returns:
            AbstractRoom: найденная комната.
            None: комната не найдена.
        """
        for room in self._rooms:
            if room.room_number == room_number:
                return room

    def remove_room(self, room_number: str) -> bool:
        """
        Удаляет комнату.

        Returns:
            bool:
                True: комната удалена.
                False: комната не удалена (например, её не было).
        """
        room = self.get_room(room_number)
        if room:
            self._rooms.remove(room)
            return True
        return False

    def join_room_participant(self,
                              room_number: str,
                              participant_id: Union[int, str],
                              name: str,
                              surname: str,
                              ) -> bool:
        """
        Добавляет участника в комнату.

        Args:
            room_number: str (номер комнаты)
            participant_id: Union[int, str] (идентификатор участника)
            name: str (имя участника)
            surname: str (фамилия участника)

        Returns:
            bool:
                True: участник добавлен в комнату
                False: ошибка добавления (например, не найдена комната)
        """
        room = self.get_room(room_number)
        if not room:
            return False
        room.add_participant(participant_id)
        room.set_participant_name(participant_id, name)
        room.set_participant_surname(participant_id, name)
        return True

    def leave_room_participant(self, room_number: str,
                               participant_id: Union[int, str]
                               ) -> bool:
        """
        Удаляет участника из комнаты.

        Args:
            room_number: str (номер комнаты)
            participant_id: Union[int, str] (идентификатор участника)

        Returns:
            bool:
                True: участник добавлен в комнату
                False: ошибка добавления (например, не найдена комната)
        """
        room = self.get_room(room_number)
        if not room:
            return False
        room.remove_participant(participant_id)
        return True

    def get_room_by_participant(self,
                                participant_id: Union[int, str],
                                ) -> Optional[str]:
        """
        Возвращает номер комнаты по участнику.

        Args:
            participant_id: str (идентификатор участника).

        Returns:
            str: номер найденной комнаты.
            None: комната не найдена.
        """
        for room in self._rooms:
            if room.check_participants(participant_id):
                return room.room_number

    def get_participant(self,
                        participant_id: Union[int, str]
                        ) -> Optional[dict]:
        """
        Возвращает данные участника по его номеру.

        Args:
            participant_id: str (идентификатор участника).

        Returns:
            dict: данные участника.
            None: участник не найден.
        """
        for room in self._rooms:
            if room.check_participants(participant_id):
                return room.get_participant(participant_id)

    def get_participants(self,
                         room_number: str,
                         ) -> Optional[dict]:
        """
        Возвращает идентификатор всех участников комнаты.

        Args:
            room_number: str (номер комнаты)

        Returns:
            list: список идентификаторов участников
            None: комната не найдена
        """
        for room in self._rooms:
            if room.room_number == room_number:
                return room.get_participants()
