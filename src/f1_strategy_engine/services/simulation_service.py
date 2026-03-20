from __future__ import annotations

from dataclasses import dataclass
import math
import random
import statistics

from f1_strategy_engine.domain.models import (
    SimulationCard,
    SimulationRequest,
    SimulationResponse,
)
from f1_strategy_engine.services.strategy_service import StrategyService


@dataclass
class SimulationService:
    strategy_service: StrategyService

    def run(self, request: SimulationRequest) -> SimulationResponse:
        recommendation = self.strategy_service.optimize(request.race_state)
        plans = [recommendation.recommended, *recommendation.alternatives][:3]
        cards: list[SimulationCard] = []

        for index, evaluation in enumerate(plans, start=1):
            positions = self._simulate_positions(
                grid_position=request.grid_position,
                win_probability=recommendation.win_probability,
                confidence=evaluation.confidence,
                simulations=request.simulation_count,
                plan_rank=index,
            )
            positions_sorted = sorted(positions)
            cards.append(
                SimulationCard(
                    rank=index,
                    strategy_name=evaluation.plan.name,
                    predicted_race_time_seconds=evaluation.expected_race_time_seconds,
                    p10_best=self._percentile_rank(positions_sorted, 0.10),
                    p50_median=self._percentile_rank(positions_sorted, 0.50),
                    p90_worst=self._percentile_rank(positions_sorted, 0.90),
                    sc_during_stop_probability=round(
                        min(0.6, request.race_state.safety_car_probability * (1.05 + index * 0.08)),
                        2,
                    ),
                    win_probability=round(
                        max(0.02, recommendation.win_probability - (index - 1) * 0.08),
                        2,
                    ),
                    risk_score=round(max(0.08, 1 - evaluation.confidence + index * 0.05), 2),
                    pit_laps=[stop.lap for stop in evaluation.plan.pit_stops],
                    compounds=[stop.new_compound for stop in evaluation.plan.pit_stops],
                    distribution=self._histogram(positions),
                )
            )

        return SimulationResponse(
            driver_code=request.driver_code,
            simulation_count=request.simulation_count,
            grid_position=request.grid_position,
            cards=cards,
        )

    def _simulate_positions(
        self,
        grid_position: int,
        win_probability: float,
        confidence: float,
        simulations: int,
        plan_rank: int,
    ) -> list[int]:
        mean = max(1.0, grid_position - win_probability * 4 + (plan_rank - 1) * 1.2)
        std_dev = max(1.2, 4.2 - confidence * 2.0 + (plan_rank - 1) * 0.5)
        rng = random.Random(f"{grid_position}-{win_probability}-{confidence}-{simulations}-{plan_rank}")
        positions: list[int] = []
        for _ in range(simulations):
            sample = rng.gauss(mean, std_dev)
            clipped = int(round(min(20, max(1, sample))))
            positions.append(clipped)
        return positions

    def _percentile_rank(self, ordered_positions: list[int], percentile: float) -> int:
        index = min(len(ordered_positions) - 1, max(0, math.floor(percentile * (len(ordered_positions) - 1))))
        return ordered_positions[index]

    def _histogram(self, positions: list[int]) -> list[int]:
        buckets = [0] * 20
        for position in positions:
            buckets[position - 1] += 1
        peak = max(buckets) if buckets else 1
        return [max(2, round(bucket / peak * 100)) if bucket else 2 for bucket in buckets]
