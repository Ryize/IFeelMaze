from abstract.abstract_effect import AbstractReducingImpactEffects
from effect_type import (ReduceTimeRemainingEffectType,
                         IncreasesEffectTypeCellCompletionTime,
                         ChangingItemsEffectType
                         )


class BaseObstaclesReducingTimeRemainingEffect(AbstractReducingImpactEffects):
    """
    Уменьшает воздействия эффектов, снижающих оставшееся время прохождения
    лабиринта.
    """
    effect_type = ReduceTimeRemainingEffectType


class BaseReducingImpactCompletionTimeEffect(AbstractReducingImpactEffects):
    """
    Уменьшает воздействия эффектов, увеличивающих время прохождения клетки.
    """
    effect_type = IncreasesEffectTypeCellCompletionTime


class BaseReducingChangingItemsEffect(AbstractReducingImpactEffects):
    """
    Уменьшает воздействия эффектов, изменяющих предметы дальнейшего
    прохождения.
    """
    effect_type = ChangingItemsEffectType
