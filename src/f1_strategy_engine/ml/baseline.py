from __future__ import annotations

from f1_strategy_engine.domain.models import TireCompound


class BaselineLapTimeModel:
    """Simple heuristic predictor that can later be replaced by a trained model."""

    compound_offset = {
        TireCompound.SOFT: 0.0,
        TireCompound.MEDIUM: 0.6,
        TireCompound.HARD: 1.1,
    }

    def predict_lap_time(
        self,
        base_lap_time_seconds: float,
        compound: TireCompound,
        tire_age_laps: int,
        degradation_per_lap: float,
        fuel_adjustment: float,
    ) -> float:
        return (
            base_lap_time_seconds
            + self.compound_offset[compound]
            + tire_age_laps * degradation_per_lap
            + fuel_adjustment
        )

