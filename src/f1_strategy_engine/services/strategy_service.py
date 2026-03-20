from __future__ import annotations

from dataclasses import dataclass, field

from f1_strategy_engine.domain.models import RaceState, StrategyRecommendation
from f1_strategy_engine.ml.baseline import BaselineLapTimeModel
from f1_strategy_engine.optimizer.engine import RaceStrategyOptimizer


@dataclass
class StrategyService:
    optimizer: RaceStrategyOptimizer = field(
        default_factory=lambda: RaceStrategyOptimizer(lap_time_model=BaselineLapTimeModel())
    )

    def optimize(self, race_state: RaceState) -> StrategyRecommendation:
        return self.optimizer.optimize(race_state)
