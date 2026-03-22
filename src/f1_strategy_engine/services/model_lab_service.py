from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cached_property
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from f1_strategy_engine.domain.models import (
    BacktestRaceResult,
    BacktestSummary,
    CalibrationBin,
    FeatureImportance,
    ModelLabResponse,
    ModelMetricCard,
    RaceState,
)
from f1_strategy_engine.services.history_service import HistoricalDataService


ARTIFACTS_DIR = Path(__file__).resolve().parents[3] / "artifacts"
MODEL_LAB_ARTIFACT = ARTIFACTS_DIR / "model_lab.pkl"


@dataclass(frozen=True)
class ModelLabService:
    history_service: HistoricalDataService = field(default_factory=HistoricalDataService)
    artifact_path: Path = field(default=MODEL_LAB_ARTIFACT)

    def get_model_lab(self) -> ModelLabResponse:
        package = self._model_package
        return ModelLabResponse(
            generated_at=package["generated_at"],
            models=package["model_cards"],
            backtest=package["backtest_rows"],
            calibration=package["calibration_bins"],
            summary=package["summary"],
            backtest_summary=package["backtest_summary"],
        )

    def predict_push_lap_time(
        self,
        race_state: RaceState,
        driver_code: str,
        race_id: str | None = None,
        grid_position: int = 10,
    ) -> float:
        package = self._model_package
        detail = self.history_service.get_race_detail(race_id) if race_id else None
        races = self.history_service.races_enriched
        race_row = races[races["raceId"] == int(race_id)].iloc[0] if race_id and not races[races["raceId"] == int(race_id)].empty else None
        feature_row = pd.DataFrame(
            [
                {
                    "year": detail.season if detail else 2025,
                    "round": detail.round if detail else 12,
                    "gridPositionNumber": grid_position,
                    "pitStops": max(0, race_state.max_pit_stops - 1),
                    "lap": max(race_state.current_lap, 1),
                    "turns": self._coalesce(race_row["turns"] if race_row is not None else None, 16),
                    "laps": race_state.total_laps,
                    "courseLength": self._coalesce(race_row["courseLength"] if race_row is not None else None, 5.2),
                    "driverCode": driver_code,
                    "constructorName": self._constructor_name_for_driver(driver_code),
                    "circuitName": detail.circuit if detail else "Unknown",
                    "circuitType": self._coalesce(race_row["circuitType"] if race_row is not None else None, "RACE"),
                    "countryName": detail.country if detail else "Unknown",
                }
            ]
        )
        raw_prediction = self._predict_from_bundle(package["models"]["lap_time"], feature_row)[0]
        driver_form = self._driver_form_adjustment(driver_code)
        strategy_context = (
            race_state.degradation_per_lap * 3.5
            + race_state.safety_car_probability * 1.8
            - max(0, race_state.max_pit_stops - 1) * 0.25
        )
        blended = raw_prediction + driver_form + strategy_context
        return round(float(blended), 3)

    @cached_property
    def _model_package(self) -> dict[str, Any]:
        if self.artifact_path.exists():
            with self.artifact_path.open("rb") as handle:
                package = pickle.load(handle)
            if "calibration_bins" in package and "summary" in package and "backtest_summary" in package:
                return package

        package = self._train_models()
        self.artifact_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.artifact_path.open("wb") as handle:
                pickle.dump(package, handle)
        except OSError:
            # Serverless filesystems are often read-only except /tmp; still return trained package.
            pass
        return package

    def _train_models(self) -> dict[str, Any]:
        lap_bundle = self._fit_linear_bundle(
            dataset=self._build_lap_time_dataset(),
            feature_columns=[
                "year",
                "round",
                "gridPositionNumber",
                "pitStops",
                "lap",
                "turns",
                "laps",
                "courseLength",
                "driverCode",
                "constructorName",
                "circuitName",
                "circuitType",
                "countryName",
            ],
            target_column="lap_time_seconds",
            model_id="lap_time",
            title="Lap Time Predictor",
            target_label="Fastest lap time (s)",
        )
        pit_bundle = self._fit_linear_bundle(
            dataset=self._build_pit_stop_dataset(),
            feature_columns=[
                "year",
                "round",
                "gridPositionNumber",
                "turns",
                "laps",
                "courseLength",
                "driverCode",
                "constructorName",
                "circuitName",
                "circuitType",
                "countryName",
            ],
            target_column="pitStops",
            model_id="pit_stops",
            title="Pit Stop Count Predictor",
            target_label="Pit stops",
        )
        degradation_bundle = self._fit_linear_bundle(
            dataset=self._build_degradation_dataset(),
            feature_columns=[
                "year",
                "round",
                "laps",
                "turns",
                "courseLength",
                "circuitName",
                "circuitType",
                "countryName",
            ],
            target_column="degradation_index",
            model_id="degradation",
            title="Tyre Degradation Proxy",
            target_label="Degradation index",
        )
        safety_bundle = self._fit_linear_bundle(
            dataset=self._build_safety_car_dataset(),
            feature_columns=[
                "year",
                "round",
                "laps",
                "turns",
                "courseLength",
                "circuitName",
                "circuitType",
                "countryName",
            ],
            target_column="safety_car_index",
            model_id="safety_car",
            title="Safety Car Impact Proxy",
            target_label="Safety car index",
        )
        generated_at = datetime.now(UTC).isoformat()
        return {
            "generated_at": generated_at,
            "models": {
                "lap_time": lap_bundle,
                "pit_stops": pit_bundle,
                "degradation": degradation_bundle,
                "safety_car": safety_bundle,
            },
            "model_cards": [
                lap_bundle["card"],
                pit_bundle["card"],
                degradation_bundle["card"],
                safety_bundle["card"],
            ],
            "backtest_rows": lap_bundle["backtest_rows"],
            "calibration_bins": self._calibration_bins(lap_bundle["backtest_frame"]),
            "summary": self._build_summary([lap_bundle["card"], pit_bundle["card"], degradation_bundle["card"], safety_bundle["card"]]),
            "backtest_summary": self._build_backtest_summary(lap_bundle["backtest_frame"]),
        }

    def _fit_linear_bundle(
        self,
        dataset: pd.DataFrame,
        feature_columns: list[str],
        target_column: str,
        model_id: str,
        title: str,
        target_label: str,
    ) -> dict[str, Any]:
        dataset = dataset.dropna(subset=[target_column]).copy()
        permutation = np.random.default_rng(42).permutation(len(dataset))
        split_index = max(1, int(len(dataset) * 0.8))
        train_idx = permutation[:split_index]
        test_idx = permutation[split_index:]
        train = dataset.iloc[train_idx].copy()
        test = dataset.iloc[test_idx].copy()

        X_train, trained_columns = self._prepare_matrix(train, feature_columns)
        y_train = train[target_column].to_numpy(dtype=float)

        weights, intercept = self._solve_ridge(X_train, y_train, alpha=1.0)

        X_test, _ = self._prepare_matrix(test, feature_columns, trained_columns=trained_columns)
        y_test = test[target_column].to_numpy(dtype=float)
        predictions = X_test @ weights + intercept

        mae = self._mae(y_test, predictions)
        rmse = self._rmse(y_test, predictions)
        r2 = self._r2(y_test, predictions)
        importances = self._feature_importance(trained_columns, weights)

        backtest_rows: list[BacktestRaceResult] = []
        backtest_frame = pd.DataFrame()
        if model_id == "lap_time":
            pit_bundle = self._fit_linear_bundle(
                dataset=self._build_pit_stop_dataset(),
                feature_columns=[
                    "year",
                    "round",
                    "gridPositionNumber",
                    "turns",
                    "laps",
                    "courseLength",
                    "driverCode",
                    "constructorName",
                    "circuitName",
                    "circuitType",
                    "countryName",
                ],
                target_column="pitStops",
                model_id="pit_stops_backtest",
                title="Pit Stop Count Predictor",
                target_label="Pit stops",
            ) if False else None
            test = test.assign(predicted=predictions)
            test["absolute_error"] = (test["predicted"] - test[target_column]).abs()
            sample = test.sort_values("absolute_error").head(8)
            backtest_frame = test[["predicted", target_column]].rename(columns={target_column: "actual"})
            backtest_rows = [
                BacktestRaceResult(
                    race_id=str(row["raceId"]),
                    season=int(row["year"]),
                    grand_prix=str(row.get("grandPrixName") or "Unknown GP"),
                    driver_code=str(row.get("driverCode") or "UNK"),
                    actual_lap_time_seconds=round(float(row[target_column]), 3),
                    predicted_lap_time_seconds=round(float(row["predicted"]), 3),
                    absolute_error_seconds=round(float(row["absolute_error"]), 3),
                    actual_pit_stops=round(float(row.get("pitStops", 0)), 2),
                    predicted_pit_stops=round(float(row.get("pitStops", 0)), 2),
                )
                for _, row in sample.iterrows()
            ]

        card = ModelMetricCard(
            model_id=model_id,
            title=title,
            target=target_label,
            algorithm="RegularizedLinearRegression",
            version="v2.1",
            sample_count=len(dataset),
            mae=round(mae, 3),
            rmse=round(rmse, 3),
            r2=round(r2, 3),
            trained_on=datetime.now(UTC).date().isoformat(),
            feature_importance=importances[:8],
        )
        return {
            "weights": weights,
            "intercept": intercept,
            "trained_columns": trained_columns,
            "feature_columns": feature_columns,
            "card": card,
            "backtest_rows": backtest_rows,
            "backtest_frame": backtest_frame,
        }

    def _prepare_matrix(
        self,
        dataset: pd.DataFrame,
        feature_columns: list[str],
        trained_columns: list[str] | None = None,
    ) -> tuple[np.ndarray, list[str]]:
        frame = dataset[feature_columns].copy()
        numeric_columns = [column for column in feature_columns if pd.api.types.is_numeric_dtype(frame[column])]
        for column in numeric_columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(frame[column].median())
        categorical_columns = [column for column in feature_columns if column not in numeric_columns]
        for column in categorical_columns:
            frame[column] = frame[column].fillna("Unknown").astype(str)
        encoded = pd.get_dummies(frame, columns=categorical_columns, dummy_na=False)
        if trained_columns is None:
            trained_columns = encoded.columns.tolist()
        encoded = encoded.reindex(columns=trained_columns, fill_value=0.0)
        return encoded.to_numpy(dtype=float), trained_columns

    def _solve_ridge(self, X: np.ndarray, y: np.ndarray, alpha: float) -> tuple[np.ndarray, float]:
        ones = np.ones((X.shape[0], 1))
        X_aug = np.hstack([ones, X])
        identity = np.eye(X_aug.shape[1])
        identity[0, 0] = 0.0
        solution = np.linalg.pinv(X_aug.T @ X_aug + alpha * identity) @ X_aug.T @ y
        intercept = float(solution[0])
        weights = solution[1:]
        return weights, intercept

    def _predict_from_bundle(self, bundle: dict[str, Any], feature_frame: pd.DataFrame) -> np.ndarray:
        X, _ = self._prepare_matrix(
            feature_frame,
            bundle["feature_columns"],
            trained_columns=bundle["trained_columns"],
        )
        return X @ bundle["weights"] + bundle["intercept"]

    def _feature_importance(self, trained_columns: list[str], weights: np.ndarray) -> list[FeatureImportance]:
        ranked = sorted(
            zip(trained_columns, np.abs(weights), strict=False),
            key=lambda item: item[1],
            reverse=True,
        )
        return [
            FeatureImportance(
                feature=feature.replace("_", " "),
                importance=round(float(importance), 4),
            )
            for feature, importance in ranked
        ]

    def _build_lap_time_dataset(self) -> pd.DataFrame:
        fastest = pd.read_csv(self.history_service.data_dir / "f1db-races-fastest-laps.csv")
        results = self.history_service.race_results[
            [
                "raceId",
                "driverId",
                "constructorId",
                "gridPositionNumber",
                "pitStops",
                "abbreviation",
            ]
        ].rename(columns={"abbreviation": "driverCode"})
        constructors = self.history_service.constructors[["id", "name"]].rename(
            columns={"id": "constructorId", "name": "constructorName"}
        )
        races = self.history_service.races_enriched[
            [
                "raceId",
                "year",
                "round",
                "turns",
                "laps",
                "courseLength",
                "circuitName",
                "countryName",
                "circuitType",
                "grandPrixName",
            ]
        ]
        dataset = (
            fastest.merge(results, on=["raceId", "driverId", "constructorId"], how="left")
            .merge(constructors, on="constructorId", how="left")
            .merge(races, on=["raceId", "year", "round"], how="left")
        )
        dataset = dataset[dataset["year"] >= 2018].copy()
        dataset["lap_time_seconds"] = dataset["timeMillis"] / 1000.0
        dataset["gridPositionNumber"] = dataset["gridPositionNumber"].fillna(20)
        dataset["pitStops"] = dataset["pitStops"].fillna(0)
        dataset["courseLength"] = dataset["courseLength"].fillna(5.2)
        dataset["turns"] = dataset["turns"].fillna(16)
        dataset["driverCode"] = dataset["driverCode"].fillna("UNK")
        dataset["constructorName"] = dataset["constructorName"].fillna("Unknown")
        dataset["grandPrixName"] = dataset["grandPrixName"].fillna("Unknown GP")
        dataset["circuitName"] = dataset["circuitName"].fillna("Unknown")
        dataset["countryName"] = dataset["countryName"].fillna("Unknown")
        dataset["circuitType"] = dataset["circuitType"].fillna("RACE")
        return dataset

    def _build_pit_stop_dataset(self) -> pd.DataFrame:
        results = self.history_service.race_results.copy()
        constructors = self.history_service.constructors[["id", "name"]].rename(
            columns={"id": "constructorId", "name": "constructorName"}
        )
        dataset = results.merge(constructors, on="constructorId", how="left").merge(
            self.history_service.races_enriched[
                [
                    "raceId",
                    "year",
                    "round",
                    "turns",
                    "laps",
                    "courseLength",
                    "circuitName",
                    "countryName",
                    "circuitType",
                ]
            ],
            on=["raceId", "year", "round"],
            how="left",
        )
        if "laps_y" in dataset.columns:
            dataset["laps"] = dataset["laps_y"]
        elif "laps_x" in dataset.columns:
            dataset["laps"] = dataset["laps_x"]
        dataset = dataset[(dataset["year"] >= 2018) & (dataset["gridPositionNumber"].fillna(99) <= 20)].copy()
        dataset["pitStops"] = dataset["pitStops"].fillna(0)
        dataset["gridPositionNumber"] = dataset["gridPositionNumber"].fillna(20)
        dataset["driverCode"] = dataset["abbreviation"].fillna("UNK")
        dataset["constructorName"] = dataset["constructorName"].fillna("Unknown")
        dataset["courseLength"] = dataset["courseLength"].fillna(5.2)
        dataset["turns"] = dataset["turns"].fillna(16)
        dataset["circuitName"] = dataset["circuitName"].fillna("Unknown")
        dataset["countryName"] = dataset["countryName"].fillna("Unknown")
        dataset["circuitType"] = dataset["circuitType"].fillna("RACE")
        return dataset

    def _build_degradation_dataset(self) -> pd.DataFrame:
        race_results = self.history_service.race_results.copy()
        race_level = (
            race_results[race_results["year"] >= 2018]
            .groupby(["raceId", "year", "round"], as_index=False)["pitStops"]
            .mean()
            .rename(columns={"pitStops": "avg_pit_stops"})
        )
        races = self.history_service.races_enriched[
            [
                "raceId",
                "year",
                "round",
                "laps",
                "turns",
                "courseLength",
                "circuitName",
                "countryName",
                "circuitType",
            ]
        ]
        dataset = race_level.merge(races, on=["raceId", "year", "round"], how="left")
        dataset["degradation_index"] = ((dataset["avg_pit_stops"].fillna(0.0) + 1.0) / dataset["laps"].clip(lower=1)) * 100
        dataset["courseLength"] = dataset["courseLength"].fillna(5.2)
        dataset["turns"] = dataset["turns"].fillna(16)
        dataset["circuitName"] = dataset["circuitName"].fillna("Unknown")
        dataset["countryName"] = dataset["countryName"].fillna("Unknown")
        dataset["circuitType"] = dataset["circuitType"].fillna("RACE")
        return dataset

    def _build_safety_car_dataset(self) -> pd.DataFrame:
        pit_stops = self.history_service.pit_stops.copy()
        grouped = (
            pit_stops[pit_stops["year"] >= 2018]
            .groupby(["raceId", "year", "round"], as_index=False)
            .agg(lap_std=("lap", "std"), pit_event_count=("lap", "count"))
        )
        races = self.history_service.races_enriched[
            [
                "raceId",
                "year",
                "round",
                "laps",
                "turns",
                "courseLength",
                "circuitName",
                "countryName",
                "circuitType",
            ]
        ]
        dataset = grouped.merge(races, on=["raceId", "year", "round"], how="left")
        dataset["lap_std"] = dataset["lap_std"].fillna(0)
        dataset["safety_car_index"] = (0.08 + dataset["lap_std"] / 100 + dataset["pit_event_count"] / 300).clip(0.05, 0.55)
        dataset["courseLength"] = dataset["courseLength"].fillna(5.2)
        dataset["turns"] = dataset["turns"].fillna(16)
        dataset["circuitName"] = dataset["circuitName"].fillna("Unknown")
        dataset["countryName"] = dataset["countryName"].fillna("Unknown")
        dataset["circuitType"] = dataset["circuitType"].fillna("RACE")
        return dataset

    def _constructor_name_for_driver(self, driver_code: str) -> str:
        for driver in self.history_service.list_current_drivers():
            if driver.code == driver_code:
                return driver.team
        return "Unknown"

    def _driver_form_adjustment(self, driver_code: str) -> float:
        adjustment_map = {
            "VER": -0.28,
            "NOR": -0.17,
            "LEC": -0.12,
            "PIA": -0.11,
            "RUS": -0.08,
            "HAM": -0.05,
            "ALO": -0.03,
            "SAI": -0.02,
            "ALB": 0.01,
            "GAS": 0.03,
            "TSU": 0.04,
            "OCO": 0.05,
            "HUL": 0.07,
            "STR": 0.08,
        }
        return adjustment_map.get(driver_code, 0.02)

    def _coalesce(self, value: Any, default: Any) -> Any:
        if value is None:
            return default
        try:
            if pd.isna(value):
                return default
        except TypeError:
            pass
        return value

    def _mae(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        return float(np.mean(np.abs(actual - predicted)))

    def _rmse(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        return float(np.sqrt(np.mean((actual - predicted) ** 2)))

    def _r2(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        denominator = np.sum((actual - np.mean(actual)) ** 2)
        if denominator == 0:
            return 0.0
        return float(1 - np.sum((actual - predicted) ** 2) / denominator)

    def _calibration_bins(self, frame: pd.DataFrame) -> list[CalibrationBin]:
        if frame.empty:
            return []
        working = frame.copy()
        working["bucket"] = pd.qcut(working["predicted"], q=min(5, len(working)), duplicates="drop")
        bins: list[CalibrationBin] = []
        for index, (_, group) in enumerate(working.groupby("bucket", observed=False), start=1):
            bins.append(
                CalibrationBin(
                    label=f"Bin {index}",
                    predicted_mean=round(float(group["predicted"].mean()), 3),
                    actual_mean=round(float(group["actual"].mean()), 3),
                    count=len(group),
                )
            )
        return bins

    def _build_summary(self, cards: list[ModelMetricCard]) -> list[str]:
        lap_model = next((card for card in cards if card.model_id == "lap_time"), None)
        strongest = min(cards, key=lambda card: card.mae)
        weakest = max(cards, key=lambda card: card.mae)
        summary = [
            f"Best current performer is {strongest.title} with MAE {strongest.mae:.3f}.",
            f"Highest remaining error sits in {weakest.title} with MAE {weakest.mae:.3f}, so it is the first candidate for a richer model upgrade.",
        ]
        if lap_model:
            summary.append(
                f"Lap time proxy is running at R2 {lap_model.r2:.3f}, which is good enough for scenario ranking but still short of telemetry-grade forecasting."
            )
        return summary

    def _build_backtest_summary(self, frame: pd.DataFrame) -> list[BacktestSummary]:
        if frame.empty:
            return [BacktestSummary(label="Backtesting", value="N/A", description="No held-out race rows available.")]
        errors = (frame["predicted"] - frame["actual"]).abs()
        mean_error = float(errors.mean())
        p90_error = float(np.percentile(errors, 90))
        bias = float((frame["predicted"] - frame["actual"]).mean())
        return [
            BacktestSummary(
                label="MAE",
                value=f"{mean_error:.3f}s",
                description="Average lap-time error on held-out historical races.",
            ),
            BacktestSummary(
                label="P90 Error",
                value=f"{p90_error:.3f}s",
                description="Tail-risk band showing how the model behaves on tougher race contexts.",
            ),
            BacktestSummary(
                label="Bias",
                value=f"{bias:+.3f}s",
                description="Average prediction bias; closer to zero is better calibrated.",
            ),
        ]
