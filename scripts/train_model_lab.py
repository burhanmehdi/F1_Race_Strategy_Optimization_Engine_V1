from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from f1_strategy_engine.services.model_lab_service import ModelLabService  # noqa: E402


if __name__ == "__main__":
    service = ModelLabService()
    result = service.get_model_lab()
    print(f"Generated at: {result.generated_at}")
    for model in result.models:
        print(
            f"{model.title}: samples={model.sample_count} mae={model.mae} rmse={model.rmse} r2={model.r2}"
        )
