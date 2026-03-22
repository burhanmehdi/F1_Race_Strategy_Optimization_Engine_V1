## Project preview

<p align="center">
<img width="1457" height="670" alt="1" src="https://github.com/user-attachments/assets/06a64806-fc32-4f93-8e96-6bdb0fb2b983" />
</p>
</b>
</b>
<img width="1164" height="631" alt="6" src="https://github.com/user-attachments/assets/bd7cf66c-7b4b-4da3-ac97-7fa6be070bee" />
</p>
</b>
</b>
<img width="1168" height="915" alt="5" src="https://github.com/user-attachments/assets/5fe49226-ff6e-4069-b27a-e6171e208ef8" />
</p>
</b>
</b>
<img width="766" height="859" alt="4" src="https://github.com/user-attachments/assets/e5178223-03a0-4a82-9419-1b00a63d7933" />
</p>
</b>
</b>
<img width="1171" height="879" alt="3" src="https://github.com/user-attachments/assets/ac7bb005-e606-42d1-bae3-d892a6e904e1" />
</p>
</b>
</b>
<img width="1491" height="909" alt="2" src="https://github.com/user-attachments/assets/8748de81-ad75-4509-9c34-f4e9a8298494" />
</p>
</b>
</b>
<img width="1153" height="854" alt="10" src="https://github.com/user-attachments/assets/f46ef4e5-cc5e-4ecd-a00a-f21dc9d45c9f" />
</p>
<img width="1160" height="827" alt="9" src="https://github.com/user-attachments/assets/935a6406-9c3b-4e9a-98b1-c5d0e5fdb10e" />
</p>
</b>
</b>
<img width="1159" height="777" alt="8" src="https://github.com/user-attachments/assets/633bedf1-6c04-4c6c-a93a-cb96b26276bc" />
</p>
</b>
</b>
<img width="1160" height="896" alt="7" src="https://github.com/user-attachments/assets/4b78d784-79f4-45e2-a0c8-43d25dd2bceb" />
</p>
</b>
</b>

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
