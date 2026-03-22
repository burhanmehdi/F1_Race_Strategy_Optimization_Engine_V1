"""Alternate Vercel FastAPI entry name (some CLI versions check app.py first)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from f1_strategy_engine.api.main import app

__all__ = ["app"]
