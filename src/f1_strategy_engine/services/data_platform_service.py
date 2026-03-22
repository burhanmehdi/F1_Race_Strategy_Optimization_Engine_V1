from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "f1db"
ARTIFACTS_DIR = Path(__file__).resolve().parents[3] / "artifacts"


@dataclass(frozen=True)
class DataPlatformService:
    data_dir: Path = field(default=DATA_DIR)
    warehouse_path: Path = field(default=ARTIFACTS_DIR / "f1_strategy.duckdb")

    def backend_name(self) -> str:
        return "duckdb" if self._duckdb_available() else "pandas-fallback"

    def read_table(self, csv_filename: str) -> pd.DataFrame:
        if self._duckdb_available():
            return self._read_with_duckdb(csv_filename)
        return pd.read_csv(self.data_dir / csv_filename, low_memory=False)

    def query(self, sql: str, views: dict[str, str] | None = None) -> pd.DataFrame:
        if not self._duckdb_available():
            raise RuntimeError("DuckDB is not installed; warehouse SQL queries are unavailable.")
        return self._query_with_duckdb(sql, views or {})

    def platform_summary(self) -> dict[str, Any]:
        available = self._duckdb_available()
        return {
            "engine": self.backend_name(),
            "warehouse_path": str(self.warehouse_path),
            "duckdb_available": available,
            "data_dir": str(self.data_dir),
            "mode": "warehouse" if available else "csv-fallback",
        }

    def _duckdb_available(self) -> bool:
        # Vercel serverless filesystem is read-only except /tmp; DuckDB warehouse writes fail.
        if os.environ.get("VERCEL"):
            return False
        try:
            import duckdb  # noqa: F401
        except ModuleNotFoundError:
            return False
        return True

    def _read_with_duckdb(self, csv_filename: str) -> pd.DataFrame:
        import duckdb

        csv_path = (self.data_dir / csv_filename).as_posix()
        self.warehouse_path.parent.mkdir(parents=True, exist_ok=True)
        with duckdb.connect(str(self.warehouse_path)) as connection:
            return connection.execute("SELECT * FROM read_csv_auto(?)", [csv_path]).df()

    def _query_with_duckdb(self, sql: str, views: dict[str, str]) -> pd.DataFrame:
        import duckdb

        self.warehouse_path.parent.mkdir(parents=True, exist_ok=True)
        with duckdb.connect(str(self.warehouse_path)) as connection:
            for view_name, csv_filename in views.items():
                csv_path = (self.data_dir / csv_filename).as_posix().replace("'", "''")
                connection.execute(
                    f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM read_csv_auto('{csv_path}')"
                )
            return connection.execute(sql).df()
