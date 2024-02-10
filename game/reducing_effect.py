from base_reducing_effect import (BaseReducingImpactCompletionTimeEffect,
                                  BaseObstaclesReducingTimeRemainingEffect)


class BucketOfColdWater(BaseObstaclesReducingTimeRemainingEffect):
    """
    Уменьшение воздействия эффекта снижающего оставшееся время прохождения
    лабиринта.

    Ведро с водой.
    """
    coefficient = 1.1


class BottleCocaCola(BaseObstaclesReducingTimeRemainingEffect):
    """
    Уменьшение воздействия эффекта снижающего оставшееся время прохождения
    лабиринта.

    Бутылка колы.
    """
    coefficient = 1.5


class FrequentRest(BaseObstaclesReducingTimeRemainingEffect):
    """
    Уменьшение воздействия эффекта снижающего оставшееся время прохождения
    лабиринта.

    Частый отдых.
    """
    coefficient = 2


class EnergyDrink(BaseReducingImpactCompletionTimeEffect):
    """
    Уменьшение воздействия эффекта увеличивающего время прохождения клетки.

    Энергетик.
    """
    coefficient = 1.1


class StaminaEnhancerPills(BaseReducingImpactCompletionTimeEffect):
    """
    Уменьшение воздействия эффекта увеличивающего время прохождения клетки.

    Таблетки для повышения выносливости.
    """
    coefficient = 1.75


class ReducingBodyDensity(BaseReducingImpactCompletionTimeEffect):
    """
    Уменьшение воздействия эффекта увеличивающего время прохождения клетки.

    Уменьшение плотности тела.
    """
    coefficient = 2.2
