# F1 Strategy Engine

An F1-inspired race strategy dashboard built for AIML and motorsport analytics work.

This project combines:
- a FastAPI backend
- a race-wall style frontend
- historical F1 CSV data
- strategy optimization
- Monte Carlo race outcome simulation
- explainable strategy outputs

The goal is to make this feel closer to a real race engineering decision-support tool than a basic dashboard demo.

## Current Scope

The app currently supports:
- multi-season race browsing from `2018` onward
- historical race and circuit selection
- current driver selection
- pit-stop board backed by real F1 CSV data
- strategy optimization with ranked plans
- simulation cards with outcome distributions
- tyre degradation and race archive views

The optimizer now reacts to driver selection and surfaces result changes more clearly in the UI.

## Stack

- `Python`
- `FastAPI`
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
│       ├── api/              # FastAPI routers
│       ├── domain/           # Core data models & schemas
│       ├── ml/               # ML pipelines & inference hooks
│       ├── optimizer/        # Strategy optimization engine
│       ├── services/         # Simulation, history & orchestration
│       └── static/           # Frontend dashboard assets
│
├── data/
│   └── f1db/                # Historical race datasets (CSV)
│
├── docs/                   # System design & architecture docs
│
├── tests/                  # Test suite (API, optimizer, ML)
│
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
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

### 4. Simulation

Runs Monte Carlo-style outcome estimation and returns:
- 3 ranked scenario cards
- finishing position distributions
- P10 / P50 / P90 position bands
- win probability
- pit-lap and compound summaries

### 5. Archive and degradation views

The dashboard also includes:
- historical race archive browsing
- tyre degradation visualization
- model-oriented metadata hooks for future training pipelines

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

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
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

```powershell
.venv\Scripts\python.exe -m pytest -q
```

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
