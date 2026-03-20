from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import pandas as pd

from f1_strategy_engine.domain.models import (
    DriverInfo,
    HistoricalPitStopRow,
    HistoricalPitStopStint,
    HistoricalRaceCatalog,
    HistoricalRaceDetail,
    HistoricalRaceSummary,
    TireCompound,
)


DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "f1db"
MIN_SUPPORTED_SEASON = 2018


@dataclass(frozen=True)
class HistoricalDataService:
    data_dir: Path = field(default=DATA_DIR)

    def list_current_drivers(self) -> list[DriverInfo]:
        results = self.race_results
        latest_year = int(results["year"].max())
        latest_round = int(results.loc[results["year"] == latest_year, "round"].max())
        latest_grid = (
            results[(results["year"] == latest_year) & (results["round"] == latest_round)]
            .loc[lambda frame: frame["gridPositionNumber"].fillna(99) <= 20]
            .sort_values("gridPositionNumber")
            .drop_duplicates(subset=["driverId"])
            .head(20)
        )
        merged = (
            latest_grid[["driverId", "constructorId"]]
            .merge(
                self.drivers[["id", "abbreviation", "fullName"]],
                left_on="driverId",
                right_on="id",
                how="left",
            )
            .merge(
                self.constructors[["id", "name"]],
                left_on="constructorId",
                right_on="id",
                how="left",
                suffixes=("", "_constructor"),
            )
        )
        return [
            DriverInfo(
                code=row["abbreviation"],
                name=row["fullName"],
                team=row["name"],
            )
            for _, row in merged.iterrows()
        ]

    def list_catalog(
        self,
        season: int | None = None,
        circuit: str | None = None,
    ) -> HistoricalRaceCatalog:
        races = self._race_summaries()
        filtered = [
            race for race in races
            if (season is None or race.season == season)
            and (circuit is None or race.circuit == circuit)
        ]
        return HistoricalRaceCatalog(
            seasons=sorted({race.season for race in races}),
            circuits=sorted({race.circuit for race in races}),
            races=filtered,
        )

    def get_race_detail(self, race_id: str) -> HistoricalRaceDetail:
        race_row = self.races_enriched[self.races_enriched["raceId"] == int(race_id)]
        if race_row.empty:
            raise KeyError(race_id)

        race = race_row.iloc[0]
        source_race = self._resolve_source_race(race)
        race_results = self.race_results[self.race_results["raceId"] == source_race["raceId"]].copy()
        race_pitstops = self.pit_stops[self.pit_stops["raceId"] == source_race["raceId"]].copy()
        pitstop_rows = self._build_pitstop_rows(race_results, race_pitstops)
        drivers = [
            code for code in race_results.sort_values("gridPositionNumber")["abbreviation"].dropna().tolist()
        ]
        fallback_note = ""
        if int(source_race["raceId"]) != int(race["raceId"]):
            fallback_note = (
                f" No completed race-result CSV was available yet for {race['year']} {race['grandPrixName']}, "
                f"so the pit-stop board is using the latest completed race at {source_race['circuitName']} "
                f"from {source_race['year']}."
            )

        return HistoricalRaceDetail(
            race_id=str(race["raceId"]),
            season=int(race["year"]),
            round=int(race["round"]),
            grand_prix=race["grandPrixName"],
            circuit=race["circuitName"],
            country=race["countryName"],
            laps=int(race["laps"]),
            pit_loss_seconds=round(self._estimate_pit_loss(race_pitstops), 2),
            base_lap_time_seconds=round(float(race["distance"]) / float(race["laps"]) * 18.7, 2),
            degradation_per_lap=round(self._estimate_degradation(race_pitstops, race_results), 3),
            safety_car_probability=round(self._estimate_safety_car_probability(race_pitstops), 2),
            current_compound=self._suggest_current_compound(pitstop_rows),
            tire_age_laps=max(6, int(race["laps"] // 5)),
            fuel_penalty_per_lap=0.03,
            compound_delta_seconds=0.6,
            strategy_bias=self._strategy_bias(race_pitstops),
            overtake_difficulty=self._overtake_difficulty(race["circuitType"], race["turns"]),
            weather_risk=self._weather_risk(race["countryName"]),
            archive_note=(
                f"Loaded from the F1DB race and pit-stop CSVs. Stint lengths and stop counts are real; "
                f"compound colors are inferred because the public pit-stop CSV does not include tyre compounds."
                f"{fallback_note}"
            ),
            drivers=drivers,
            pitstop_rows=pitstop_rows,
        )

    @cached_property
    def races_enriched(self) -> pd.DataFrame:
        races = self.races.merge(
            self.grands_prix[["id", "shortName"]].rename(columns={"id": "grandPrixKey"}),
            left_on="grandPrixId",
            right_on="grandPrixKey",
            how="left",
        ).merge(
            self.circuits[["id", "fullName", "placeName", "countryId", "type"]].rename(columns={"id": "circuitKey"}),
            left_on="circuitId",
            right_on="circuitKey",
            how="left",
        ).merge(
            self.countries[["id", "name"]].rename(columns={"id": "countryKey"}),
            left_on="countryId",
            right_on="countryKey",
            how="left",
        )
        races = races[races["year"] >= MIN_SUPPORTED_SEASON].copy()
        races = races.rename(columns={"id": "raceId"})
        races["grandPrixName"] = races["shortName"].fillna(races["officialName"])
        races["circuitName"] = races["placeName"].fillna(races["fullName"])
        races["countryName"] = races["name"]
        races["circuitType"] = races["type"]
        return races

    @cached_property
    def races(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-races.csv")

    @cached_property
    def pit_stops(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-races-pit-stops.csv")

    @cached_property
    def race_results(self) -> pd.DataFrame:
        results = pd.read_csv(self.data_dir / "f1db-races-race-results.csv", low_memory=False)
        return results.merge(
            self.drivers[["id", "abbreviation", "fullName"]],
            left_on="driverId",
            right_on="id",
            how="left",
        )

    @cached_property
    def drivers(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-drivers.csv")

    @cached_property
    def constructors(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-constructors.csv")

    @cached_property
    def circuits(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-circuits.csv")

    @cached_property
    def grands_prix(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-grands-prix.csv")

    @cached_property
    def countries(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "f1db-countries.csv")

    def _race_summaries(self) -> list[HistoricalRaceSummary]:
        races = self.races_enriched.sort_values(["year", "round"])
        return [
            HistoricalRaceSummary(
                race_id=str(row["raceId"]),
                season=int(row["year"]),
                round=int(row["round"]),
                grand_prix=row["grandPrixName"],
                circuit=row["circuitName"],
                country=row["countryName"],
            )
            for _, row in races.iterrows()
        ]

    def _build_pitstop_rows(
        self,
        race_results: pd.DataFrame,
        race_pitstops: pd.DataFrame,
    ) -> list[HistoricalPitStopRow]:
        rows: list[HistoricalPitStopRow] = []
        pit_groups = {
            driver_id: sorted(group["lap"].dropna().astype(int).tolist())
            for driver_id, group in race_pitstops.groupby("driverId")
        }

        for _, result in race_results.sort_values("gridPositionNumber").iterrows():
            finish_lap = int(result["laps"]) if pd.notna(result["laps"]) and int(result["laps"]) > 0 else 1
            stops = pit_groups.get(result["driverId"], [])
            stint_laps = self._laps_from_stops(stops, finish_lap)
            stints = self._infer_compounds(stint_laps)
            rows.append(
                HistoricalPitStopRow(
                    driver_code=result["abbreviation"],
                    finish_lap=finish_lap,
                    stints=stints,
                )
            )
        return rows

    def _resolve_source_race(self, requested_race: pd.Series) -> pd.Series:
        direct_results = self.race_results[self.race_results["raceId"] == requested_race["raceId"]]
        if not direct_results.empty:
            return requested_race

        same_circuit = self.races_enriched[
            (self.races_enriched["circuitId"] == requested_race["circuitId"])
            & (self.races_enriched["date"] < requested_race["date"])
        ].sort_values(["date", "round"], ascending=False)

        for _, candidate in same_circuit.iterrows():
            candidate_results = self.race_results[self.race_results["raceId"] == candidate["raceId"]]
            if not candidate_results.empty:
                return candidate

        return requested_race

    def _laps_from_stops(self, stops: list[int], finish_lap: int) -> list[int]:
        if not stops:
            return [finish_lap]
        stint_laps: list[int] = []
        previous_lap = 0
        for lap in stops:
            stint_laps.append(max(1, lap - previous_lap))
            previous_lap = lap
        stint_laps.append(max(1, finish_lap - previous_lap))
        return stint_laps

    def _infer_compounds(self, stint_laps: list[int]) -> list[HistoricalPitStopStint]:
        if len(stint_laps) == 1:
            compounds = [TireCompound.HARD]
        elif len(stint_laps) == 2:
            compounds = [TireCompound.MEDIUM, TireCompound.HARD]
        elif len(stint_laps) == 3:
            compounds = [TireCompound.MEDIUM, TireCompound.HARD, TireCompound.SOFT]
        else:
            compounds = [TireCompound.SOFT, TireCompound.MEDIUM, TireCompound.HARD, TireCompound.SOFT]
        return [
            HistoricalPitStopStint(
                compound=compounds[min(index, len(compounds) - 1)],
                laps=stint_laps[index],
                used=index > 0,
            )
            for index in range(len(stint_laps))
        ]

    def _estimate_pit_loss(self, race_pitstops: pd.DataFrame) -> float:
        if race_pitstops.empty:
            return 21.0
        median_ms = race_pitstops["timeMillis"].dropna().median()
        return max(17.0, min(32.0, float(median_ms) / 1000 + 18.0))

    def _estimate_degradation(self, race_pitstops: pd.DataFrame, race_results: pd.DataFrame) -> float:
        avg_stops = race_results["pitStops"].fillna(0).mean()
        return max(0.05, min(0.12, 0.06 + float(avg_stops) * 0.01))

    def _estimate_safety_car_probability(self, race_pitstops: pd.DataFrame) -> float:
        if race_pitstops.empty:
            return 0.12
        stop_variance = race_pitstops["lap"].dropna().std()
        return max(0.08, min(0.45, 0.10 + (0 if pd.isna(stop_variance) else float(stop_variance) / 100)))

    def _strategy_bias(self, race_pitstops: pd.DataFrame) -> str:
        avg_stops = race_pitstops["stop"].max() if not race_pitstops.empty else 1
        if avg_stops >= 3:
            return "High-degradation multi-stop"
        if avg_stops == 2:
            return "Flexible two-stop"
        return "Track-position one-stop"

    def _overtake_difficulty(self, circuit_type: str, turns: float) -> str:
        if circuit_type == "STREET":
            return "Low"
        if turns >= 18:
            return "Medium"
        return "High"

    def _weather_risk(self, country: str) -> str:
        if country in {"Belgium", "Great Britain", "Brazil", "Japan"}:
            return "Elevated"
        return "Stable"

    def _suggest_current_compound(self, pitstop_rows: list[HistoricalPitStopRow]) -> TireCompound:
        if not pitstop_rows or not pitstop_rows[0].stints:
            return TireCompound.MEDIUM
        return pitstop_rows[0].stints[0].compound
