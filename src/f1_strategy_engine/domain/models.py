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
