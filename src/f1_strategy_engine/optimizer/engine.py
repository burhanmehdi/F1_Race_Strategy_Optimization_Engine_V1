from __future__ import annotations

from dataclasses import dataclass
from f1_strategy_engine.domain.models import (
    PitStop,
    RaceState,
    StrategyEvaluation,
    StrategyPlan,
    StrategyRecommendation,
    TireCompound,
)
from f1_strategy_engine.ml.baseline import BaselineLapTimeModel


@dataclass
class RaceStrategyOptimizer:
    lap_time_model: BaselineLapTimeModel
    driver_pace_adjustments: dict[str, float] | None = None

    def __post_init__(self) -> None:
        if self.driver_pace_adjustments is None:
            self.driver_pace_adjustments = {
                "VER": -0.32,
                "NOR": -0.24,
                "LEC": -0.18,
                "PIA": -0.15,
                "RUS": -0.11,
                "HAM": -0.08,
                "ALO": -0.05,
                "SAI": -0.04,
                "ANT": -0.02,
                "LAW": 0.00,
                "ALB": 0.02,
                "GAS": 0.03,
                "HAD": 0.04,
                "TSU": 0.05,
                "STR": 0.07,
                "OCO": 0.08,
                "BEA": 0.10,
                "HUL": 0.12,
                "BOR": 0.14,
                "DOO": 0.17,
            }

    def optimize(self, race_state: RaceState) -> StrategyRecommendation:
        candidates = self._generate_candidates(race_state)
        evaluations = [self._evaluate_plan(race_state, plan) for plan in candidates]
        ranked = sorted(evaluations, key=lambda item: item.expected_race_time_seconds)
        baseline = self._evaluate_plan(race_state, self._build_baseline_plan(race_state))
        improvement = max(0.0, baseline.expected_race_time_seconds - ranked[0].expected_race_time_seconds)
        driver_delta = self._driver_pace_delta(race_state.driver_code)
        driver_bonus = max(-0.08, min(0.08, (-driver_delta) * 0.18))
        win_probability = min(0.97, max(0.08, 0.34 + ranked[0].confidence * 0.25 + improvement / 25 + driver_bonus))
        risk_level = "High" if race_state.safety_car_probability >= 0.3 else "Moderate" if race_state.safety_car_probability >= 0.15 else "Controlled"
        return StrategyRecommendation(
            recommended=ranked[0],
            alternatives=ranked[1:],
            baseline=baseline,
            improvement_seconds=round(improvement, 3),
            win_probability=round(win_probability, 2),
            risk_level=risk_level,
            driver_code=race_state.driver_code,
            driver_pace_delta_seconds=round(driver_delta, 3),
        )

    def _generate_candidates(self, race_state: RaceState) -> list[StrategyPlan]:
        remaining_laps = race_state.total_laps - race_state.current_lap + 1
        window_start = race_state.current_lap + max(2, remaining_laps // 6)
        window_mid = race_state.current_lap + max(4, remaining_laps // 3)

        candidates = [
            StrategyPlan(
                name="Stay out to hard",
                pit_stops=[PitStop(lap=min(window_start, race_state.total_laps), new_compound=TireCompound.HARD)],
            ),
            StrategyPlan(
                name="Cover undercut with medium",
                pit_stops=[PitStop(lap=min(window_start + 1, race_state.total_laps), new_compound=TireCompound.MEDIUM)],
            ),
            StrategyPlan(
                name="Aggressive two-stop",
                pit_stops=[
                    PitStop(lap=min(window_start, race_state.total_laps - 2), new_compound=TireCompound.MEDIUM),
                    PitStop(lap=min(window_mid, race_state.total_laps), new_compound=TireCompound.SOFT),
                ],
            ),
        ]
        return [plan for plan in candidates if len(plan.pit_stops) <= race_state.max_pit_stops]

    def _evaluate_plan(self, race_state: RaceState, plan: StrategyPlan) -> StrategyEvaluation:
        green_time = self._simulate_plan(race_state, plan, safety_car=False)
        sc_time = self._simulate_plan(race_state, plan, safety_car=True)
        expected_time = (
            green_time * (1 - race_state.safety_car_probability)
            + sc_time * race_state.safety_car_probability
        )
        confidence = max(0.35, 1.0 - race_state.safety_car_probability * 0.5)
        explanation = self._build_explanation(race_state, plan, green_time, sc_time)
        return StrategyEvaluation(
            plan=plan,
            expected_race_time_seconds=round(expected_time, 3),
            green_race_time_seconds=round(green_time, 3),
            safety_car_race_time_seconds=round(sc_time, 3),
            confidence=round(confidence, 2),
            explanation=explanation,
        )

    def _build_baseline_plan(self, race_state: RaceState) -> StrategyPlan:
        remaining_laps = race_state.total_laps - race_state.current_lap + 1
        baseline_stop = min(race_state.current_lap + max(8, remaining_laps // 2), race_state.total_laps)
        return StrategyPlan(
            name="Baseline track-position plan",
            pit_stops=[PitStop(lap=baseline_stop, new_compound=TireCompound.HARD)],
        )

    def _simulate_plan(self, race_state: RaceState, plan: StrategyPlan, safety_car: bool) -> float:
        total_time = 0.0
        current_compound = race_state.current_compound
        current_tire_age = race_state.tire_age_laps
        stops_by_lap = {stop.lap: stop for stop in plan.pit_stops}
        driver_delta = self._driver_pace_delta(race_state.driver_code)

        for lap in range(race_state.current_lap, race_state.total_laps + 1):
            fuel_adjustment = max(0.0, (race_state.total_laps - lap) * race_state.fuel_penalty_per_lap)
            lap_time = self.lap_time_model.predict_lap_time(
                base_lap_time_seconds=race_state.base_lap_time_seconds,
                compound=current_compound,
                tire_age_laps=current_tire_age,
                degradation_per_lap=race_state.degradation_per_lap,
                fuel_adjustment=fuel_adjustment,
            )
            lap_time += driver_delta
            if safety_car:
                lap_time *= 0.88
            total_time += lap_time
            current_tire_age += 1

            if lap in stops_by_lap:
                stop_loss = race_state.pit_loss_seconds * (0.6 if safety_car else 1.0)
                total_time += stop_loss
                current_compound = stops_by_lap[lap].new_compound
                current_tire_age = 0

        return total_time

    def _build_explanation(
        self,
        race_state: RaceState,
        plan: StrategyPlan,
        green_time: float,
        sc_time: float,
    ) -> str:
        if len(plan.pit_stops) == 1:
            plan_style = "single-stop"
        else:
            plan_style = "two-stop"

        delta = sc_time - green_time
        driver_delta = self._driver_pace_delta(race_state.driver_code)
        driver_note = ""
        if race_state.driver_code:
            direction = "gain" if driver_delta <= 0 else "drag"
            driver_note = f" Driver pace input for {race_state.driver_code} adds {abs(driver_delta):.2f}s/lap {direction}."
        return (
            f"This {plan_style} plan balances pit loss of {race_state.pit_loss_seconds:.1f}s "
            f"against degradation at {race_state.degradation_per_lap:.2f}s per lap. "
            f"The safety-car scenario shifts total race time by {delta:.1f}s."
            f"{driver_note}"
        )

    def _driver_pace_delta(self, driver_code: str | None) -> float:
        if not driver_code or not self.driver_pace_adjustments:
            return 0.0
        return self.driver_pace_adjustments.get(driver_code.upper(), 0.0)
