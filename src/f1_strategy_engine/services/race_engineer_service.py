from __future__ import annotations

from dataclasses import dataclass, field

from f1_strategy_engine.domain.models import (
    RaceEngineerRequest,
    RaceEngineerResponse,
    RaceState,
    ScenarioComparisonItem,
    ScenarioComparisonResponse,
    ScenarioRecommendation,
    SensitivityMetric,
)
from f1_strategy_engine.services.history_service import HistoricalDataService
from f1_strategy_engine.services.model_lab_service import ModelLabService
from f1_strategy_engine.services.strategy_service import StrategyService


@dataclass
class RaceEngineerService:
    strategy_service: StrategyService = field(default_factory=StrategyService)
    history_service: HistoricalDataService = field(default_factory=HistoricalDataService)
    model_lab_service: ModelLabService = field(default_factory=ModelLabService)

    def analyze(self, request: RaceEngineerRequest) -> RaceEngineerResponse:
        detail = self.history_service.get_race_detail(request.race_id) if request.race_id else None

        base_state = request.race_state.model_copy(
            update={
                "driver_code": request.driver_code,
            }
        )
        push_lap = self.model_lab_service.predict_push_lap_time(
            race_state=base_state,
            driver_code=request.driver_code,
            race_id=request.race_id,
            grid_position=request.grid_position,
        )
        base_state = base_state.model_copy(
            update={
                "base_lap_time_seconds": round((base_state.base_lap_time_seconds + push_lap) / 2, 3),
            }
        )
        primary = self.strategy_service.optimize(base_state)

        fallback_state = self._build_fallback_state(base_state, request)
        fallback = self.strategy_service.optimize(fallback_state)

        confidence = max(
            0.2,
            min(
                0.96,
                (primary.recommended.confidence * 0.55)
                + (1 - request.weather_risk) * 0.15
                + (1 - request.traffic_risk) * 0.15
                + (1 - abs(request.gap_ahead_seconds - request.gap_behind_seconds) / 10) * 0.15,
            ),
        )

        assumptions = [
            f"Predicted push lap for {request.driver_code} at this circuit context is {push_lap:.3f}s.",
            f"Traffic gap ahead is {request.gap_ahead_seconds:.1f}s and gap behind is {request.gap_behind_seconds:.1f}s.",
            f"Safety car fallback is optimized for laps {request.safety_car_window_start}-{request.safety_car_window_end}.",
            f"Weather risk is treated as {int(request.weather_risk * 100)}% and traffic risk as {int(request.traffic_risk * 100)}%.",
        ]
        if detail:
            assumptions.append(
                f"{detail.grand_prix} at {detail.circuit} is tagged as {detail.strategy_bias.lower()} with {detail.overtake_difficulty.lower()} overtaking."
            )

        lap_by_lap = [
            f"Push through lap {max(base_state.current_lap + 2, request.safety_car_window_start - 1)} unless tyre drop exceeds the current degradation estimate.",
            f"If the race stays green, commit to {primary.recommended.plan.name} around lap {primary.recommended.plan.pit_stops[0].lap if primary.recommended.plan.pit_stops else base_state.total_laps}.",
            f"If safety car or VSC lands in laps {request.safety_car_window_start}-{request.safety_car_window_end}, switch to {fallback.recommended.plan.name}.",
            f"Review traffic immediately after each planned stop; if pit exit traffic exceeds {request.gap_behind_seconds + 1.5:.1f}s loss exposure, extend by 1 lap.",
        ]

        sensitivities = [
            SensitivityMetric(
                factor="Safety car timing",
                level="High" if request.race_state.safety_car_probability >= 0.2 else "Moderate",
                effect=f"Fallback strategy becomes favorable if SC/VSC appears between laps {request.safety_car_window_start}-{request.safety_car_window_end}.",
            ),
            SensitivityMetric(
                factor="Tyre degradation",
                level="High" if request.race_state.degradation_per_lap >= 0.09 else "Moderate",
                effect=f"Every +0.01s/lap degradation shifts the ideal stop window earlier by roughly 1 lap.",
            ),
            SensitivityMetric(
                factor="Traffic release",
                level="High" if request.traffic_risk >= 0.3 or request.gap_behind_seconds <= 1.5 else "Controlled",
                effect="Tight pit-exit traffic can erase undercut value, so clean-air availability matters heavily.",
            ),
        ]

        return RaceEngineerResponse(
            driver_code=request.driver_code,
            predicted_push_lap_time_seconds=push_lap,
            primary=self._scenario_card(
                label="Primary call",
                trigger="Green race / normal degradation",
                recommendation=primary,
            ),
            fallback=self._scenario_card(
                label="Fallback",
                trigger=f"SC or VSC between laps {request.safety_car_window_start}-{request.safety_car_window_end}",
                recommendation=fallback,
            ),
            confidence=round(confidence, 2),
            assumptions=assumptions,
            lap_by_lap_callouts=lap_by_lap,
            sensitivities=sensitivities,
        )

    def compare_scenarios(self, request: RaceEngineerRequest) -> ScenarioComparisonResponse:
        scenario_configs = [
            (
                "green",
                "Green Race",
                "Normal tyre fade and full pit loss",
                {},
            ),
            (
                "safety_car",
                "Safety Car",
                f"SC or VSC between laps {request.safety_car_window_start}-{request.safety_car_window_end}",
                {
                    "safety_car_probability": min(0.9, request.race_state.safety_car_probability + 0.32),
                    "pit_loss_seconds": max(11.0, request.race_state.pit_loss_seconds * 0.7),
                },
            ),
            (
                "rain",
                "Rain Crossover",
                "Weather volatility adds degradation and confidence loss",
                {
                    "degradation_per_lap": round(request.race_state.degradation_per_lap + 0.02 + request.weather_risk * 0.02, 3),
                    "base_lap_time_seconds": request.race_state.base_lap_time_seconds + 2.2,
                },
            ),
            (
                "traffic",
                "High Traffic",
                "Undercut risk rises because pit exit traffic is dense",
                {
                    "pit_loss_seconds": request.race_state.pit_loss_seconds + 1.8,
                    "compound_delta_seconds": request.race_state.compound_delta_seconds + 0.25,
                },
            ),
        ]

        scenarios: list[ScenarioComparisonItem] = []
        for scenario_id, title, trigger, updates in scenario_configs:
            state = request.race_state.model_copy(update={"driver_code": request.driver_code, **updates})
            recommendation = self.strategy_service.optimize(state)
            scenarios.append(
                ScenarioComparisonItem(
                    scenario_id=scenario_id,
                    title=title,
                    trigger=trigger,
                    strategy_name=recommendation.recommended.plan.name,
                    expected_race_time_seconds=recommendation.recommended.expected_race_time_seconds,
                    win_probability=recommendation.win_probability,
                    confidence=max(
                        0.2,
                        recommendation.recommended.confidence
                        - (0.1 if scenario_id == "rain" else 0.06 if scenario_id == "traffic" else 0.0),
                    ),
                    risk_level=recommendation.risk_level,
                    pit_laps=[stop.lap for stop in recommendation.recommended.plan.pit_stops],
                    compounds=[stop.new_compound for stop in recommendation.recommended.plan.pit_stops],
                    summary=recommendation.recommended.explanation,
                )
            )

        return ScenarioComparisonResponse(
            driver_code=request.driver_code,
            race_id=request.race_id,
            scenarios=scenarios,
        )

    def _build_fallback_state(self, base_state: RaceState, request: RaceEngineerRequest) -> RaceState:
        return base_state.model_copy(
            update={
                "safety_car_probability": min(0.85, base_state.safety_car_probability + 0.25),
                "pit_loss_seconds": max(12.0, base_state.pit_loss_seconds * 0.72),
                "degradation_per_lap": round(base_state.degradation_per_lap + request.weather_risk * 0.01, 3),
                "max_pit_stops": min(3, max(base_state.max_pit_stops, 2)),
            }
        )

    def _scenario_card(self, label: str, trigger: str, recommendation) -> ScenarioRecommendation:
        return ScenarioRecommendation(
            label=label,
            trigger=trigger,
            strategy_name=recommendation.recommended.plan.name,
            expected_race_time_seconds=recommendation.recommended.expected_race_time_seconds,
            confidence=recommendation.recommended.confidence,
            pit_laps=[stop.lap for stop in recommendation.recommended.plan.pit_stops],
            compounds=[stop.new_compound for stop in recommendation.recommended.plan.pit_stops],
        )
