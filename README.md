## Project preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/a49b5180-f873-4155-ad5b-024c3d0001bc" width="90%" alt="Dashboard preview"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/0ceae334-eefc-4b99-8175-1f84894abaee" width="70%" alt="UI preview"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3e6e7ef5-286b-4101-ac8c-2253b2bc352b" width="90%" alt="Feature preview"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bbb313f8-f25c-454a-9bc7-60cd5b6d8178" width="90%" alt="Feature preview"/>
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

## Deploy on Vercel

Deploy as a **FastAPI** Python project ([FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)).

1. Push this repo to GitHub (e.g. [F1_Race_Strategy_Optimization_Engine_V1](https://github.com/burhanmehdi/F1_Race_Strategy_Optimization_Engine_V1)).
2. [Vercel → New Project](https://vercel.com/new) → import the repository.
3. **Root directory**: repository root (`.`).
4. Deploy; verify **`/health`** on the production URL.

**Details**

- Root **`main.py` / `index.py` / `app.py`** prepend `src/` to `sys.path` so the app resolves during build (same idea as the official [Vercel FastAPI example](https://github.com/vercel/vercel/tree/main/examples/fastapi)).
- **`pyproject.toml`**: `[project.scripts] app = "f1_strategy_engine.api.main:app"` and `[tool.vercel.scripts] build = "python scripts/train_model_lab.py"` to generate `artifacts/model_lab.pkl` at build time (artifact remains gitignored but is included in the deployment output).
- **WebSockets** (`/ws/live-race`) may be limited on serverless; prefer **`POST /api/live-race`** for previews in production.
- If cold starts time out, raise the **function max duration** in the Vercel project settings.

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
