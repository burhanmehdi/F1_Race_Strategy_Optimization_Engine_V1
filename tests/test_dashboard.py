from fastapi.testclient import TestClient

from f1_strategy_engine.api.main import app


def test_dashboard_page_loads() -> None:
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "F1 Strategy Engine" in response.text
    assert "Run Optimizer" in response.text
    assert "Race Archive" in response.text


def test_catalog_endpoint_returns_historical_races() -> None:
    client = TestClient(app)
    response = client.get("/api/catalog")

    assert response.status_code == 200
    payload = response.json()
    assert 2018 in payload["seasons"]
    assert 2025 in payload["seasons"]
    assert 2024 in payload["seasons"]
    assert any(race["grand_prix"] == "Austrian GP" for race in payload["races"])
    assert any(race["circuit"] == "Lusail" for race in payload["races"])


def test_platform_endpoint_reports_backend_and_live_provider() -> None:
    client = TestClient(app)
    response = client.get("/api/platform")

    assert response.status_code == 200
    payload = response.json()
    assert payload["engine"] in {"duckdb", "pandas-fallback"}
    assert payload["live_provider"] == "historical-replay"


def test_live_provider_catalog_endpoint_returns_blueprints() -> None:
    client = TestClient(app)
    response = client.get("/api/live/providers")

    assert response.status_code == 200
    payload = response.json()
    assert payload["active_provider"] == "historical-replay"
    assert any(item["provider_name"] == "external-timing-blueprint" for item in payload["available_providers"])


def test_race_detail_endpoint_returns_selected_race() -> None:
    client = TestClient(app)
    catalog = client.get("/api/catalog").json()
    race_id = catalog["races"][0]["race_id"]
    detail = client.get(f"/api/races/{race_id}")

    assert detail.status_code == 200
    payload = detail.json()
    assert payload["race_id"] == race_id
    assert payload["pitstop_rows"]


def test_current_drivers_endpoint_returns_20_driver_lineup() -> None:
    client = TestClient(app)
    response = client.get("/api/drivers/current")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 20
    assert any(driver["code"] == "VER" for driver in payload)
    assert any(driver["team"] == "Ferrari" for driver in payload)


def test_simulation_endpoint_returns_three_cards() -> None:
    client = TestClient(app)
    response = client.post(
        "/simulate",
        json={
            "driver_code": "VER",
            "simulation_count": 1000,
            "grid_position": 3,
            "race_state": {
                "current_lap": 18,
                "total_laps": 57,
                "current_compound": "MEDIUM",
                "tire_age_laps": 12,
                "pit_loss_seconds": 21.5,
                "base_lap_time_seconds": 91.2,
                "fuel_penalty_per_lap": 0.03,
                "safety_car_probability": 0.18,
                "degradation_per_lap": 0.09,
                "max_pit_stops": 3,
                "compound_delta_seconds": 0.6,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["cards"]) == 3
    assert payload["cards"][0]["distribution"]


def test_model_lab_endpoint_returns_metrics() -> None:
    client = TestClient(app)
    response = client.get("/api/model-lab")

    assert response.status_code == 200
    payload = response.json()
    assert payload["models"]
    assert any(model["model_id"] == "lap_time" for model in payload["models"])
    assert any(model["version"] == "v2.1" for model in payload["models"])
    assert payload["backtest"]
    assert payload["calibration"]
    assert payload["summary"]
    assert payload["backtest_summary"]


def test_live_race_preview_endpoint_returns_snapshots() -> None:
    client = TestClient(app)
    catalog = client.get("/api/catalog").json()
    race_id = catalog["races"][0]["race_id"]
    response = client.post(
        "/api/live-race",
        json={
            "race_id": race_id,
            "driver_code": "VER",
            "start_lap": 14,
            "sample_size": 6,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 6
    assert payload[0]["recommendation"]["action"] in {"BOX THIS LAP", "STAY OUT"}
    assert payload[0]["recommendation"]["reasons"]


def test_live_race_websocket_streams_updates() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws/live-race?race_id=1046&driver_code=VER&start_lap=14&sample_size=4") as websocket:
        first = websocket.receive_json()
        assert first["driver_code"] == "VER"
        assert "telemetry" in first
        assert "recommendation" in first


def test_race_engineer_endpoint_returns_primary_and_fallback() -> None:
    client = TestClient(app)
    catalog = client.get("/api/catalog").json()
    race_id = catalog["races"][0]["race_id"]
    response = client.post(
        "/race-engineer",
        json={
            "race_id": race_id,
            "driver_code": "VER",
            "grid_position": 3,
            "gap_ahead_seconds": 1.8,
            "gap_behind_seconds": 1.5,
            "weather_risk": 0.12,
            "traffic_risk": 0.2,
            "safety_car_window_start": 18,
            "safety_car_window_end": 24,
            "race_state": {
                "driver_code": "VER",
                "current_lap": 18,
                "total_laps": 57,
                "current_compound": "MEDIUM",
                "tire_age_laps": 12,
                "pit_loss_seconds": 21.5,
                "base_lap_time_seconds": 91.2,
                "fuel_penalty_per_lap": 0.03,
                "safety_car_probability": 0.18,
                "degradation_per_lap": 0.09,
                "max_pit_stops": 3,
                "compound_delta_seconds": 0.6,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["primary"]["strategy_name"]
    assert payload["fallback"]["strategy_name"]
    assert payload["assumptions"]
    assert payload["lap_by_lap_callouts"]


def test_race_engineer_scenario_comparison_returns_four_views() -> None:
    client = TestClient(app)
    response = client.post(
        "/race-engineer/scenarios",
        json={
            "race_id": "1046",
            "driver_code": "VER",
            "grid_position": 3,
            "gap_ahead_seconds": 1.8,
            "gap_behind_seconds": 1.5,
            "weather_risk": 0.12,
            "traffic_risk": 0.2,
            "safety_car_window_start": 18,
            "safety_car_window_end": 24,
            "race_state": {
                "driver_code": "VER",
                "current_lap": 18,
                "total_laps": 57,
                "current_compound": "MEDIUM",
                "tire_age_laps": 12,
                "pit_loss_seconds": 21.5,
                "base_lap_time_seconds": 91.2,
                "fuel_penalty_per_lap": 0.03,
                "safety_car_probability": 0.18,
                "degradation_per_lap": 0.09,
                "max_pit_stops": 3,
                "compound_delta_seconds": 0.6,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["scenarios"]) == 4
    assert any(item["scenario_id"] == "green" for item in payload["scenarios"])
    assert any(item["scenario_id"] == "safety_car" for item in payload["scenarios"])
