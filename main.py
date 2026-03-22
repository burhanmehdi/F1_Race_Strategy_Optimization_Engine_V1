"""Vercel FastAPI entry (matches examples/fastapi/main.py pattern).

Adds ``src/`` to ``sys.path`` so ``f1_strategy_engine`` resolves during the build
before ``pip install -e .`` has run.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from f1_strategy_engine.api.main import app

__all__ = ["app"]
