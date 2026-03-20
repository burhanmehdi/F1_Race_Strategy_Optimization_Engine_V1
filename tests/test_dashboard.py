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
