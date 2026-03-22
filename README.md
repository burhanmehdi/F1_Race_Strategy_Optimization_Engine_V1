## Project preview

## Project preview

<p align="center">
  <img src="assets/screenshots/1.png" width="90%" alt="Simulation UI"/>
</p>

<p align="center">
  <img src="assets/screenshots/2.png" width="90%" alt="Tyre Degradation"/>
</p>

<p align="center">
  <img src="assets/screenshots/3.png" width="90%" alt="Race Archive"/>
</p>

<p align="center">
  <img src="assets/screenshots/4.png" width="90%" alt="Model Lab"/>
</p>

<p align="center">
  <img src="assets/screenshots/5.png" width="90%" alt="Backtesting"/>
</p>

<p align="center">
  <img src="assets/screenshots/6.png" width="90%" alt="Strategy Engine"/>
</p>

<p align="center">
  <img src="assets/screenshots/7.png" width="90%" alt="Pit Stops"/>
</p>

<p align="center">
  <img src="assets/screenshots/8.png" width="90%" alt="Race Engineer Mode"/>
</p>

<p align="center">
  <img src="assets/screenshots/9.png" width="90%" alt="Scenario Comparison"/>
</p>

<p align="center">
  <img src="assets/screenshots/10.png" width="90%" alt="Optimizer"/>
</p>

---

# F1 Race Strategy Optimization Engine

**FastAPI** dashboard for F1-style **race strategy**, **simulation**, and **AIML** demos—built on historical **F1DB** CSV data. The goal is a credible **decision-support** feel (race wall, optimizer, engineer view), not a static chart page.

| | |
|:---|:---|
| **Backend** | FastAPI, Pydantic |
| **Data** | F1DB CSVs under `data/f1db/`; DuckDB-ready layer with **Pandas/CSV fallback** |
| **Frontend** | Vanilla HTML / CSS / JavaScript in `src/f1_strategy_engine/static/` |
| **ML / analytics** | NumPy, Pandas, scikit-learn; Model Lab + training script |

---

## Contents

- [Features](#features)
- [Repository layout](#repository-layout)
- [Data](#data)
- [Run locally](#run-locally)
- [Tests](#tests)
- [Deploy on Vercel](#deploy-on-vercel)
- [Documentation](#documentation)

---

## Features

### Race control & history

- Multi-season browsing from **2018** onward; race, circuit, and **driver** selection
- **Pit-stop board** from real CSV-backed stints (compound colouring **inferred** where the dataset does not expose compound-by-stint)

### Strategy & simulation

- **Optimizer**: recommended plan, ranked alternatives, baseline vs optimized, timing and risk-style signals; reacts to driver selection in the UI
- **Monte Carlo–style simulation**: scenario cards, position bands, win probability, pit/compound summaries

### Live-style race flow

- **HTTP** live race preview (`POST /api/live-race`) and **WebSocket** stream (`/ws/live-race`) for local Uvicorn
- Pluggable **live provider** layer for future timing/weather feeds

### AIML-focused views

- **Race Engineer**: primary/fallback strategy, assumptions, lap-by-lap callouts, **scenario comparison** (green / safety car / rain / traffic)
- **Model Lab**: proxy models, metrics (MAE / RMSE / R²), feature importance, backtesting rows, calibration-style bins
- **Archive** and **tyre degradation** views

### Platform & APIs

- **`/api/platform`**: data platform / engine summary
- **`DataPlatformService`**: DuckDB path when available; on **Vercel**, warehouse writes are skipped in favour of CSV mode (read-only filesystem constraints)

---

## Repository layout

```text
.
├── main.py, index.py, app.py     # Vercel FastAPI entrypoints (bootstrap src/ + re-export app)
├── run_dashboard.py              # Local Uvicorn (127.0.0.1:8000)
├── start_dashboard.bat           # Launch dashboard in a new window
├── start_dashboard_detached.bat  # Detached launcher variant
├── pyproject.toml                # Package metadata, deps, Vercel app script + build hook
├── requirements.txt              # Editable install: -e .
├── .python-version               # Python 3.12 (tooling / Vercel hint)
├── .vercelignore                 # Trim deploy upload
│
├── src/
│   ├── index.py                  # Alternate Vercel entry under src/
│   └── f1_strategy_engine/
│       ├── api/main.py           # FastAPI app, routes, static mount, WebSockets
│       ├── domain/models.py      # Pydantic / shared models
│       ├── ml/baseline.py
│       ├── optimizer/engine.py
│       ├── services/
│       │   ├── history_service.py
│       │   ├── data_platform_service.py
│       │   ├── live_data_provider_service.py
│       │   ├── live_race_service.py
│       │   ├── model_lab_service.py
│       │   ├── race_engineer_service.py
│       │   ├── simulation_service.py
│       │   └── strategy_service.py
│       └── static/               # index.html, app.js, styles.css
│
├── data/f1db/                    # F1DB CSV dataset (large; not listed file-by-file)
├── artifacts/                    # Generated model_lab.pkl (gitignored; built on CI/Vercel)
├── assets/screenshots/           # SVG previews for docs / readme
├── docs/                         # Product & architecture notes
├── examples/                     # Sample JSON payloads
├── scripts/train_model_lab.py    # Trains / refreshes Model Lab artifact
└── tests/                        # pytest (API + optimizer)
```

---

## Data

Open **F1DB** CSVs live in **`data/f1db/`**. Pit counts and stint structure follow the files; compound colours on the board are **inferred** when stint-level compounds are missing.

---

## Run locally

**1. Virtual environment (Windows PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**2. Install**

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**3. Run**

```powershell
.venv\Scripts\python.exe run_dashboard.py
```

Or double-click / run `start_dashboard.bat`.

**4. Open** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Tests

Install dev extras once, then run pytest:

```powershell
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

---

## Documentation

- [Product brief](docs/product_brief.md)
- [Architecture](docs/architecture.md)
- [MVP backlog](docs/mvp_backlog.md)

---

## Why this project

- Optimization and **simulation** tied to **real historical** motorsport data  
- **Explainable** strategy-style outputs and engineer-facing UX  
- Clear path from **data → models → UI**, suitable for portfolio and AIML coursework  

---

## Possible next steps

- Stronger predictive models trained end-to-end on historical seasons  
- Systematic **backtesting** against past races  
- Richer uncertainty and calibration in simulation  
- Deeper **model evaluation** dashboards  
