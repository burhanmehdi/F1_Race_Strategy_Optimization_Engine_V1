from f1_strategy_engine.domain.models import RaceState, TireCompound
from f1_strategy_engine.services.strategy_service import StrategyService


def test_strategy_service_returns_ranked_recommendation() -> None:
    service = StrategyService()
    recommendation = service.optimize(
        RaceState(
            driver_code="VER",
            current_lap=18,
            total_laps=57,
            current_compound=TireCompound.MEDIUM,
            tire_age_laps=12,
            pit_loss_seconds=21.5,
            base_lap_time_seconds=91.2,
        )
    )

    assert recommendation.recommended.plan.name
    assert recommendation.recommended.expected_race_time_seconds > 0
    assert recommendation.recommended.confidence >= 0.35
    assert len(recommendation.alternatives) >= 1
    assert recommendation.baseline.plan.name
    assert recommendation.improvement_seconds >= 0
    assert 0 <= recommendation.win_probability <= 1


def test_driver_selection_changes_optimizer_output() -> None:
    service = StrategyService()
    base_state = dict(
        current_lap=18,
        total_laps=57,
        current_compound=TireCompound.MEDIUM,
        tire_age_laps=12,
        pit_loss_seconds=21.5,
        base_lap_time_seconds=91.2,
    )

    front_runner = service.optimize(RaceState(driver_code="VER", **base_state))
    midfield_runner = service.optimize(RaceState(driver_code="HUL", **base_state))

    assert front_runner.driver_pace_delta_seconds != midfield_runner.driver_pace_delta_seconds
    assert (
        front_runner.recommended.expected_race_time_seconds
        != midfield_runner.recommended.expected_race_time_seconds
    )
