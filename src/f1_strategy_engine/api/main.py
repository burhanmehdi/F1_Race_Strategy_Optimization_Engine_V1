from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from f1_strategy_engine.domain.models import (
    DriverInfo,
    HistoricalRaceCatalog,
    HistoricalRaceDetail,
    ModelLabResponse,
    RaceState,
    RaceEngineerRequest,
    RaceEngineerResponse,
    ScenarioComparisonResponse,
    SimulationRequest,
    SimulationResponse,
    StrategyRecommendation,
)
from f1_strategy_engine.services.history_service import HistoricalDataService
from f1_strategy_engine.services.model_lab_service import ModelLabService
from f1_strategy_engine.services.race_engineer_service import RaceEngineerService
from f1_strategy_engine.services.simulation_service import SimulationService
from f1_strategy_engine.services.strategy_service import StrategyService

app = FastAPI(title="F1 Race Strategy Optimization Engine", version="0.1.0")
strategy_service = StrategyService()
simulation_service = SimulationService(strategy_service=strategy_service)
historical_data_service = HistoricalDataService()
model_lab_service = ModelLabService(history_service=historical_data_service)
race_engineer_service = RaceEngineerService(
    strategy_service=strategy_service,
    history_service=historical_data_service,
    model_lab_service=model_lab_service,
)
BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/optimize", response_model=StrategyRecommendation)
def optimize(race_state: RaceState) -> StrategyRecommendation:
    return strategy_service.optimize(race_state)


@app.post("/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest) -> SimulationResponse:
    return simulation_service.run(request)


@app.post("/race-engineer", response_model=RaceEngineerResponse)
def race_engineer(request: RaceEngineerRequest) -> RaceEngineerResponse:
    return race_engineer_service.analyze(request)


@app.post("/race-engineer/scenarios", response_model=ScenarioComparisonResponse)
def compare_race_engineer_scenarios(request: RaceEngineerRequest) -> ScenarioComparisonResponse:
    return race_engineer_service.compare_scenarios(request)


@app.get("/api/catalog", response_model=HistoricalRaceCatalog)
def get_catalog(
    season: int | None = Query(default=None),
    circuit: str | None = Query(default=None),
) -> HistoricalRaceCatalog:
    return historical_data_service.list_catalog(season=season, circuit=circuit)


@app.get("/api/races/{race_id}", response_model=HistoricalRaceDetail)
def get_race_detail(race_id: str) -> HistoricalRaceDetail:
    try:
        return historical_data_service.get_race_detail(race_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Race not found") from exc


@app.get("/api/drivers/current", response_model=list[DriverInfo])
def get_current_drivers() -> list[DriverInfo]:
    return historical_data_service.list_current_drivers()


@app.get("/api/model-lab", response_model=ModelLabResponse)
def get_model_lab() -> ModelLabResponse:
    return model_lab_service.get_model_lab()
