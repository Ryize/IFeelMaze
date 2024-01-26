from typing import Type

from abstract.abstract_effect import (BaseEffect, AbstractEffectType,
                                      AbstractEffect, AbstractFactoryEffects,
                                      )
from effect_type import (ReduceTimeRemainingEffectType,
                         IncreasesEffectTypeCellCompletionTime, WinEffectType)


class HeatEffect(BaseEffect):
    """
    Эффект - жара. Уменьшает оставшееся время на прохождение лабиринта.
    """
    coefficient = 1.2
    effect_type = ReduceTimeRemainingEffectType

    def get_message(self) -> str:
        return f'Жара, думаю у меня будет тепловой удар. ' \
               f'Время прохождение лабиринта уменьшено на' \
               f' {(self.coefficient - 1) * 100}%.'


class ColdEffect(BaseEffect):
    """
    Эффект - холод. Увеличивает время прохождения клетки.
    """
    coefficient = 2
    effect_type = IncreasesEffectTypeCellCompletionTime

    def get_message(self) -> str:
        return f'Вот это мороз... быстро идти на получится.' \
               f' Время прохождение клетки увеличено на' \
               f' {(self.coefficient - 1) * 100}%.'


class FloodEffect(BaseEffect):
    """
    Эффект - топь. Увеличивает время прохождения клетки.
    """
    coefficient = 3
    effect_type = IncreasesEffectTypeCellCompletionTime

    def get_message(self) -> str:
        return f'О нет, топь, придётся идти очень осторожно.' \
               f' Время прохождение клетки увеличено на' \
               f' {(self.coefficient - 1) * 100}%.'


class SharpStonesEffect(BaseEffect):
    """
    Эффект - острые камни. Увеличивает время прохождения клетки.
    """
    coefficient = 2.25
    effect_type = IncreasesEffectTypeCellCompletionTime

    def get_message(self) -> str:
        return f'Острые камни, надо сбавить темп или я поранюсь.' \
               f' Время прохождение клетки увеличено на' \
               f' {(self.coefficient - 1) * 100}%.'


class WinEffect(BaseEffect):
    """
    Эффект - победа. После вызова считается что пользователь покинул лабиринт.
    """
    coefficient = 0
    effect_type = WinEffectType

    def get_message(self) -> str:
        return f'Вы прошли лабиринт!'


class FactoryEffects(AbstractFactoryEffects):
    """
    Создаёт и возвращает объекты эффектов.
    """

    @classmethod
    def get_effects_by_type(cls,
                            effect_types: list[Type[AbstractEffectType]]
                            ) -> list[Type[AbstractEffect]]:
        """
        Получение эффекта по типам.

        Args:
            effect_types: list[AbstractEffectType] (список с типами эффектов)

        Returns:
            list[AbstractEffect]: список с эффектами отфильтрованными по
            указанному типу.
        """
        effects = cls.get_effects()
        effects_with_correct_type = []
        for effect in effects:
            if effect.effect_type in effect_types:
                effects_with_correct_type.append(effect)
        return effects_with_correct_type

    @staticmethod
    def get_effects() -> list[Type[AbstractEffect]]:
        """
        Получение списка всех эффектов.

        Returns:
            list[AbstractEffect]: список с эффектами.
        """
        effects = AbstractEffect.__subclasses__()
        for effect in effects:
            if effect is BaseEffect:
                effects.extend(BaseEffect.__subclasses__())
                effects.remove(effect)
            if effect is WinEffect:
                effects.remove(effect)
        return list(map(lambda effect: effect(), effects))

    @staticmethod
    def get_win_effect() -> AbstractEffect:
        """
        Получить эффект победы.
        """
        return WinEffect()
