from abc import ABC, abstractmethod
from typing import Type


class AbstractEffectType(ABC):
    """
    Представляет тип (категорию эффектов).
    """
    @abstractmethod
    def __repr__(self) -> str:
        pass


class AbstractEffect(ABC):
    """
    Конкретный эффект, содержит тип эффекта и коофицент, влияющий на дальнейшие
    расчёты последствий вставания на клетку.
    """
    coefficient: float
    effect_type: AbstractEffectType

    @abstractmethod
    def get_effect(self) -> dict:
        """
        Получить в виде словаря коофицент и тип эффекта.
        """
        pass

    @abstractmethod
    def get_message(self) -> str:
        """
        Получение текста от столкновения с эффектом.
        """
        pass


class BaseEffect(AbstractEffect):
    """
    Базовая вариация эффекта.

    Содержит реализованный метод get_effect, работающий без корректировок для
    любых дочерних классов. Реализует паттерн Singleton.
    """
    def get_effect(self) -> dict:
        """
        Получение данных об эффекте по умолчанию.
        """
        return {
            'type': self.effect_type,
            'coefficient': self.coefficient,
        }

    def __new__(cls) -> 'BaseEffect':
        """
        Singleton, тк нет смысла создавать много объектов эффекта.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


class AbstractFactoryEffects(ABC):
    """
    Создаёт и возвращает эффекты.
    """

    @classmethod
    @abstractmethod
    def get_effects_by_type(cls,
                            effect_types: list[Type[AbstractEffectType]]
                            ) -> list[Type[AbstractEffect]]:
        """
        Возвращает список с эффектами отфильтрованных по указанным типам.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_effects() -> list[Type[AbstractEffect]]:
        """
        Возвращает список со всеми эффектами.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_win_effect() -> AbstractEffect:
        """
        Получить эффект победы.
        """
        pass


class AbstractReducingImpactEffects(ABC):
    """
    Уменьшает воздействие негативных эффектов.
    """
    coefficient: float
    effect_type: AbstractEffectType
