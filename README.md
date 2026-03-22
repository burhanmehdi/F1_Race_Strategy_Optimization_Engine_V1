## Project Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/a49b5180-f873-4155-ad5b-024c3d0001bc" width="90%"/>
</p>

<br>
<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/0ceae334-eefc-4b99-8175-1f84894abaee" width="70%"/>
</p>

<br>
<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3e6e7ef5-286b-4101-ac8c-2253b2bc352b" width="90%"/>
</p>

<br>
<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bbb313f8-f25c-454a-9bc7-60cd5b6d8178" width="90%"/>
</p>
<br>

# F1 Strategy Engine

An F1-inspired race strategy dashboard built for AIML and motorsport analytics work.

This project combines:
- a FastAPI backend
- a DuckDB-ready data platform layer
- a race-wall style frontend
- historical F1 CSV data
- strategy optimization
- Monte Carlo race outcome simulation
- live WebSocket race streaming
- explainable strategy outputs

The goal is to make this feel closer to a real race engineering decision-support tool than a basic dashboard demo.

## Current Scope

The app currently supports:
- multi-season race browsing from `2018` onward
- historical race and circuit selection
- current driver selection
- pit-stop board backed by real F1 CSV data
- live race mode with telemetry-style strategy calls
- strategy optimization with ranked plans
- simulation cards with outcome distributions
- race engineer mode with primary and fallback calls
- scenario comparison for green / safety car / rain / traffic cases
- model lab with trained proxies, feature importance, versioned metrics, backtesting, and calibration bins
- tyre degradation and race archive views

The optimizer now reacts to driver selection and surfaces result changes more clearly in the UI.

## Stack

- `Python`
- `FastAPI`
- `DuckDB`-ready warehouse layer with fallback
- `Pydantic`
- `Pandas`
- `NumPy`
- `scikit-learn`
- plain `HTML/CSS/JavaScript`

## Project Structure

```text
.
├── src/
│   └── f1_strategy_engine/
│       ├── __init__.py
│       ├── api/
│       │   └── main.py                  # FastAPI routes
│       ├── domain/
│       │   └── models.py                # Core schemas and typed models
│       ├── ml/
│       │   └── baseline.py              # Baseline ML logic
│       ├── optimizer/
│       │   └── engine.py                # Strategy optimization engine
│       ├── services/
│       │   ├── history_service.py       # Historical CSV data layer
│       │   ├── data_platform_service.py # DuckDB / CSV data platform
│       │   ├── live_race_service.py     # Live race preview + WebSocket stream
│       │   ├── model_lab_service.py     # Model training/evaluation service
│       │   ├── race_engineer_service.py # Race Engineer logic
│       │   ├── simulation_service.py    # Monte Carlo simulation
│       │   └── strategy_service.py      # Strategy orchestration
│       └── static/
│           ├── app.js                   # Frontend logic
│           ├── index.html               # Dashboard UI
│           └── styles.css               # Dashboard styling
│
├── data/
│   └── f1db/                            # Historical F1 CSV dataset
│       ├── f1db-races.csv
│       ├── f1db-races-pit-stops.csv
│       ├── f1db-races-race-results.csv
│       ├── f1db-drivers.csv
│       ├── f1db-circuits.csv
│       └── ... many other F1DB CSV files
│
├── assets/
│   └── screenshots/
│       ├── dashboard-preview.svg
│       ├── optimizer-preview.svg
│       └── race-engineer-preview.svg
│
├── artifacts/
│   └── model_lab.pkl                    # Saved model artifact
│
├── docs/
│   ├── architecture.md
│   ├── mvp_backlog.md
│   └── product_brief.md
│
├── examples/
│   └── sample_optimize_request.json
│
├── scripts/
│   └── train_model_lab.py               # Training script
│
├── tests/
│   ├── conftest.py
│   ├── test_dashboard.py
│   └── test_optimizer.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
├── run_dashboard.py
├── start_dashboard.bat
└── .gitignore

```

## Features

### 1. Historical race control

Select season, Grand Prix, and circuit from the backend catalog to drive the rest of the dashboard.

### 2. Pit-stop board

Shows historical pit-stop structure using real CSV-backed race data. Hover states expose clearer driver and stint details.

### 3. Optimizer

Given a race state, the app returns:
- recommended strategy
- ranked alternatives
- baseline vs optimized comparison
- expected race time
- confidence
- risk level
- driver-aware pace impact

### 4. Live race mode

The app now includes a real-time style race wall flow:
- WebSocket-powered live telemetry stream
- provider-based live data architecture
- lap-by-lap pit call updates
- undercut vs overcut projection
- traffic-loss estimate after pit exit
- tyre cliff risk detection
- explainable recommendation reasons
- live scenario prompts like `box this lap`, `stay out`, and `switch to Plan B`

### 5. Data platform

The backend now includes a stronger data architecture:
- `DataPlatformService` for DuckDB-ready historical querying
- automatic fallback to Pandas/CSV mode when DuckDB is not yet installed
- a platform status endpoint at `/api/platform`
- a pluggable live-provider layer so external timing/weather feeds can be added later without rewriting strategy logic

### 6. Simulation

Runs Monte Carlo-style outcome estimation and returns:
- 3 ranked scenario cards
- finishing position distributions
- P10 / P50 / P90 position bands
- win probability
- pit-lap and compound summaries

### 7. Archive and degradation views

The dashboard also includes:
- historical race archive browsing
- tyre degradation visualization
- model-oriented metadata hooks for future training pipelines

### 8. Race Engineer and Model Lab

Two AIML-focused sections now make the project much stronger for portfolio use:
- `Race Engineer Mode` for primary strategy, fallback strategy, assumptions, lap-by-lap callouts, and side-by-side scenario comparison
- `Model Lab` for trained proxy models, MAE/RMSE/R2, feature importance, model versions, backtesting rows, and calibration-style evaluation bins

## Data

This repository uses the open F1DB CSV dataset stored in:

`data/f1db/`

Important note:
- pit-stop counts and stint structure are backed by real CSV rows
- tyre compound colors on the pit board are inferred where the source dataset does not include public compound-by-stint data

## Run Locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Editable install (application and runtime libraries):

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

To run tests, install dev extras once:

```powershell
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### 3. Start the dashboard

```powershell
.venv\Scripts\python.exe run_dashboard.py
```

Or use:

```powershell
start_dashboard.bat
```

### 4. Open the app

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Run Tests

Requires dev extras (`pip install -e ".[dev]"`).

```powershell
.venv\Scripts\python.exe -m pytest -q
```

## Deploy on Vercel (GitHub)

This app is a FastAPI project that Vercel can run as a Python backend ([FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)). The repo root has `index.py` exporting `app` (required for Vercel’s entrypoint detection), `pyproject.toml` also declares the same target under `[project.scripts]`, and a Vercel build step runs `scripts/train_model_lab.py` so `artifacts/model_lab.pkl` is generated during the build (the file stays gitignored but is included in the deployment output).

1. Push this repository to GitHub (for example [F1_Race_Strategy_Optimization_Engine_V1](https://github.com/burhanmehdi/F1_Race_Strategy_Optimization_Engine_V1)).
2. In the [Vercel dashboard](https://vercel.com/new), **Add New Project** and import the same GitHub repository.
3. Use the default **Root Directory** (repository root). Vercel will install dependencies from `requirements.txt` and run the build script from `pyproject.toml`.
4. Deploy. When the build finishes, open the production URL and check `/health`.

Notes:

- Live **WebSocket** (`/ws/live-race`) may not behave like local Uvicorn on serverless; the **`POST /api/live-race`** path is the reliable preview API.
- If a request times out on the first cold start, increase the **Function max duration** for the Python function in the Vercel project settings.

## Documentation

- [Product Brief](docs/product_brief.md)
- [Architecture](docs/architecture.md)
- [MVP Backlog](docs/mvp_backlog.md)

## What Makes This Resume-Worthy

This is not just a UI project. It demonstrates:
- applied optimization
- simulation-driven decision support
- historical sports data engineering
- explainable outputs
- product thinking for an F1-style use case

## Next Up

The strongest next upgrades are:
- trained predictive models from historical data
- backtesting against past races
- richer uncertainty-aware simulation
- race engineer mode with primary and fallback strategy calls
- model evaluation dashboards
