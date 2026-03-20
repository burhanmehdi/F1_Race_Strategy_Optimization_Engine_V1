from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from f1_strategy_engine.domain.models import (
    DriverInfo,
    HistoricalRaceCatalog,
    HistoricalRaceDetail,
    RaceState,
    SimulationRequest,
    SimulationResponse,
    StrategyRecommendation,
)
from f1_strategy_engine.services.history_service import HistoricalDataService
from f1_strategy_engine.services.simulation_service import SimulationService
from f1_strategy_engine.services.strategy_service import StrategyService

app = FastAPI(title="F1 Race Strategy Optimization Engine", version="0.1.0")
strategy_service = StrategyService()
simulation_service = SimulationService(strategy_service=strategy_service)
historical_data_service = HistoricalDataService()
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
