from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class TireCompound(str, Enum):
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class RaceState(BaseModel):
    driver_code: str | None = Field(
        default=None,
        description="Selected driver abbreviation used for driver-specific pace adjustments.",
    )
    current_lap: int = Field(..., ge=1)
    total_laps: int = Field(..., ge=1)
    current_compound: TireCompound
    tire_age_laps: int = Field(..., ge=0)
    pit_loss_seconds: float = Field(..., gt=0)
    base_lap_time_seconds: float = Field(..., gt=0)
    fuel_penalty_per_lap: float = Field(0.03, ge=0)
    safety_car_probability: float = Field(0.1, ge=0, le=1)
    degradation_per_lap: float = Field(0.08, ge=0)
    max_pit_stops: int = Field(3, ge=1, le=3)
    compound_delta_seconds: float = Field(
        0.6,
        ge=0,
        description="Gap between adjacent compounds in base pace.",
    )


class PitStop(BaseModel):
    lap: int = Field(..., ge=1)
    new_compound: TireCompound


class StrategyPlan(BaseModel):
    name: str
    pit_stops: List[PitStop]


class StrategyEvaluation(BaseModel):
    plan: StrategyPlan
    expected_race_time_seconds: float
    green_race_time_seconds: float
    safety_car_race_time_seconds: float
    confidence: float = Field(..., ge=0, le=1)
    explanation: str


class StrategyRecommendation(BaseModel):
    recommended: StrategyEvaluation
    alternatives: List[StrategyEvaluation]
    baseline: StrategyEvaluation
    improvement_seconds: float = Field(..., ge=0)
    win_probability: float = Field(..., ge=0, le=1)
    risk_level: str
    driver_code: str | None = None
    driver_pace_delta_seconds: float = 0.0


class HistoricalRaceSummary(BaseModel):
    race_id: str
    season: int
    round: int
    grand_prix: str
    circuit: str
    country: str


class HistoricalRaceCatalog(BaseModel):
    seasons: List[int]
    circuits: List[str]
    races: List[HistoricalRaceSummary]


class DriverInfo(BaseModel):
    code: str
    name: str
    team: str


class SimulationRequest(BaseModel):
    race_state: RaceState
    driver_code: str
    simulation_count: int = Field(..., ge=100, le=10000)
    grid_position: int = Field(..., ge=1, le=20)


class SimulationCard(BaseModel):
    rank: int
    strategy_name: str
    predicted_race_time_seconds: float
    p10_best: int
    p50_median: int
    p90_worst: int
    sc_during_stop_probability: float
    win_probability: float
    risk_score: float
    pit_laps: List[int]
    compounds: List[TireCompound]
    distribution: List[int]


class SimulationResponse(BaseModel):
    driver_code: str
    simulation_count: int
    grid_position: int
    cards: List[SimulationCard]


class HistoricalPitStopStint(BaseModel):
    compound: TireCompound
    laps: int = Field(..., ge=1)
    used: bool = False


class HistoricalPitStopRow(BaseModel):
    driver_code: str
    finish_lap: int = Field(..., ge=1)
    stints: List[HistoricalPitStopStint]


class HistoricalRaceDetail(BaseModel):
    race_id: str
    season: int
    round: int
    grand_prix: str
    circuit: str
    country: str
    laps: int = Field(..., ge=1)
    pit_loss_seconds: float = Field(..., gt=0)
    base_lap_time_seconds: float = Field(..., gt=0)
    degradation_per_lap: float = Field(..., ge=0)
    safety_car_probability: float = Field(..., ge=0, le=1)
    current_compound: TireCompound
    tire_age_laps: int = Field(..., ge=0)
    fuel_penalty_per_lap: float = Field(..., ge=0)
    compound_delta_seconds: float = Field(..., ge=0)
    strategy_bias: str
    overtake_difficulty: str
    weather_risk: str
    archive_note: str
    drivers: List[str]
    pitstop_rows: List[HistoricalPitStopRow]


class FeatureImportance(BaseModel):
    feature: str
    importance: float = Field(..., ge=0)


class ModelMetricCard(BaseModel):
    model_id: str
    title: str
    target: str
    algorithm: str
    version: str = "v1"
    sample_count: int = Field(..., ge=0)
    mae: float = Field(..., ge=0)
    rmse: float = Field(..., ge=0)
    r2: float
    trained_on: str
    feature_importance: List[FeatureImportance]


class BacktestRaceResult(BaseModel):
    race_id: str
    season: int
    grand_prix: str
    driver_code: str
    actual_lap_time_seconds: float = Field(..., ge=0)
    predicted_lap_time_seconds: float = Field(..., ge=0)
    absolute_error_seconds: float = Field(..., ge=0)
    actual_pit_stops: float = Field(..., ge=0)
    predicted_pit_stops: float = Field(..., ge=0)


class ModelLabResponse(BaseModel):
    generated_at: str
    models: List[ModelMetricCard]
    backtest: List[BacktestRaceResult]
    calibration: List["CalibrationBin"]
    summary: List[str]
    backtest_summary: List["BacktestSummary"]


class RaceEngineerRequest(BaseModel):
    race_id: str | None = None
    race_state: RaceState
    driver_code: str
    grid_position: int = Field(..., ge=1, le=20)
    gap_ahead_seconds: float = Field(1.8, ge=0)
    gap_behind_seconds: float = Field(1.6, ge=0)
    weather_risk: float = Field(0.1, ge=0, le=1)
    traffic_risk: float = Field(0.2, ge=0, le=1)
    safety_car_window_start: int = Field(..., ge=1)
    safety_car_window_end: int = Field(..., ge=1)


class ScenarioRecommendation(BaseModel):
    label: str
    trigger: str
    strategy_name: str
    expected_race_time_seconds: float = Field(..., ge=0)
    confidence: float = Field(..., ge=0, le=1)
    pit_laps: List[int]
    compounds: List[TireCompound]


class SensitivityMetric(BaseModel):
    factor: str
    level: str
    effect: str


class RaceEngineerResponse(BaseModel):
    driver_code: str
    predicted_push_lap_time_seconds: float = Field(..., ge=0)
    primary: ScenarioRecommendation
    fallback: ScenarioRecommendation
    confidence: float = Field(..., ge=0, le=1)
    assumptions: List[str]
    lap_by_lap_callouts: List[str]
    sensitivities: List[SensitivityMetric]


class CalibrationBin(BaseModel):
    label: str
    predicted_mean: float
    actual_mean: float
    count: int = Field(..., ge=0)


class ScenarioComparisonItem(BaseModel):
    scenario_id: str
    title: str
    trigger: str
    strategy_name: str
    expected_race_time_seconds: float = Field(..., ge=0)
    win_probability: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    risk_level: str
    pit_laps: List[int]
    compounds: List[TireCompound]
    summary: str


class ScenarioComparisonResponse(BaseModel):
    driver_code: str
    race_id: str | None = None
    scenarios: List[ScenarioComparisonItem]


class BacktestSummary(BaseModel):
    label: str
    value: str
    description: str


class LiveRaceRequest(BaseModel):
    race_id: str
    driver_code: str
    start_lap: int = Field(default=1, ge=1)
    sample_size: int = Field(default=8, ge=4, le=20)
    provider_name: str | None = None


class LiveTelemetryPoint(BaseModel):
    lap: int = Field(..., ge=1)
    sector_1_seconds: float = Field(default=0, ge=0)
    sector_2_seconds: float = Field(default=0, ge=0)
    sector_3_seconds: float = Field(default=0, ge=0)
    gap_ahead_seconds: float = Field(..., ge=0)
    gap_behind_seconds: float = Field(..., ge=0)
    last_lap_seconds: float = Field(..., ge=0)
    tyre_age_laps: int = Field(..., ge=0)
    fuel_load_index: float = Field(..., ge=0)
    traffic_index: float = Field(..., ge=0)
    weather_risk: float = Field(..., ge=0, le=1)
    safety_car_probability: float = Field(..., ge=0, le=1)
    rival_pitted: bool = False
    vsc_active: bool = False


class LiveWeatherPoint(BaseModel):
    air_temperature_c: float
    track_temperature_c: float
    rain_probability: float = Field(..., ge=0, le=1)
    humidity: float = Field(..., ge=0, le=1)
    wind_speed_kph: float = Field(..., ge=0)
    condition: str


class LiveRaceEvent(BaseModel):
    lap: int = Field(..., ge=1)
    category: str
    title: str
    detail: str
    impact: str


class LiveDecisionRecommendation(BaseModel):
    headline: str
    action: str
    confidence: float = Field(..., ge=0, le=1)
    pit_window_start: int = Field(..., ge=1)
    pit_window_end: int = Field(..., ge=1)
    undercut_gain_seconds: float
    overcut_risk_seconds: float
    traffic_loss_seconds: float
    tyre_cliff_risk: str
    plan_b_trigger: str
    reasons: List[str]


class LiveRaceSnapshot(BaseModel):
    race_id: str
    driver_code: str
    telemetry: LiveTelemetryPoint
    weather: LiveWeatherPoint
    events: List[LiveRaceEvent]
    recommendation: LiveDecisionRecommendation
    scenario_notes: List[str]


class LiveProviderDescriptor(BaseModel):
    provider_name: str
    provider_mode: str
    status: str
    description: str


class LiveProviderCatalog(BaseModel):
    active_provider: str
    mode: str
    available_providers: List[LiveProviderDescriptor]
