from game.abstract.abstract_effect import AbstractEffectType


class IncreasesEffectTypeCellCompletionTime(AbstractEffectType):
    """
    Категория эффектов увеличивающих время прохождения клетки.
    """
    def __repr__(self) -> str:
        return 'Время прохождения клетки увеличено'


class ReduceTimeRemainingEffectType(AbstractEffectType):
    """
    Категория эффектов уменьшающих оставшееся время.
    """
    def __repr__(self) -> str:
        return 'Оставшееся время уменьшено'


class ChangingItemsEffectType(AbstractEffectType):
    """
    Категория эффектов изменяющих предметы дальнейшего прохождения.
    """
    def __repr__(self) -> str:
        return 'Предметы изменены'


class WinEffectType(AbstractEffectType):
    """
    Категория эффектов победы в лабиринте.
    """
    def __repr__(self) -> str:
        return 'Победа в лабиринте'
