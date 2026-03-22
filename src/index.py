"""Vercel FastAPI entry re-export (see https://vercel.com/docs/frameworks/backend/fastapi)."""

from f1_strategy_engine.api.main import app

__all__ = ["app"]
