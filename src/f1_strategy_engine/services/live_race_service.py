from __future__ import annotations

from dataclasses import dataclass, field
from math import sin

from f1_strategy_engine.domain.models import (
    LiveDecisionRecommendation,
    LiveProviderCatalog,
    LiveRaceRequest,
    LiveRaceEvent,
    LiveRaceSnapshot,
    LiveTelemetryPoint,
    LiveWeatherPoint,
    RaceEngineerRequest,
    RaceState,
)
from f1_strategy_engine.services.history_service import HistoricalDataService
from f1_strategy_engine.services.live_data_provider_service import (
    HistoricalReplayEventProvider,
    HistoricalReplayTimingProvider,
    HistoricalReplayWeatherProvider,
    build_provider_catalog,
)
from f1_strategy_engine.services.model_lab_service import ModelLabService
from f1_strategy_engine.services.race_engineer_service import RaceEngineerService


@dataclass(frozen=True)
class LiveRaceService:
    history_service: HistoricalDataService = field(default_factory=HistoricalDataService)
    model_lab_service: ModelLabService = field(default_factory=ModelLabService)
    race_engineer_service: RaceEngineerService = field(default_factory=RaceEngineerService)

    def build_stream(self, request: LiveRaceRequest) -> list[LiveRaceSnapshot]:
        timing_provider = HistoricalReplayTimingProvider(builder=self._build_replay_telemetry)
        weather_provider = HistoricalReplayWeatherProvider(builder=self._build_replay_weather)
        event_provider = HistoricalReplayEventProvider(builder=self._build_replay_events)
        telemetry_points = timing_provider.telemetry_stream(request)
        weather_points = weather_provider.weather_stream(request)
        event_points = event_provider.event_stream(request)
        detail = self.history_service.get_race_detail(request.race_id)
        snapshots: list[LiveRaceSnapshot] = []
        for index, telemetry in enumerate(telemetry_points):
            weather = weather_points[min(index, len(weather_points) - 1)]
            events = event_points[min(index, len(event_points) - 1)]
            recommendation = self._recommend(detail.race_id, request.driver_code, telemetry, detail)
            scenario_notes = [
                f"If SC arrives between L{max(1, telemetry.lap - 1)}-L{telemetry.lap + 2}, switch to Plan B.",
                "Undercut benefit is rising." if recommendation.undercut_gain_seconds > 1.5 else "Stay on current offset while tyre remains stable.",
                "Rain crossover risk rising." if weather.rain_probability >= 0.22 else "Weather stable for current stint plan.",
            ]
            snapshots.append(
                LiveRaceSnapshot(
                    race_id=request.race_id,
                    driver_code=request.driver_code,
                    telemetry=telemetry,
                    weather=weather,
                    events=events,
                    recommendation=recommendation,
                    scenario_notes=scenario_notes,
                )
            )
        return snapshots

    def provider_name(self) -> str:
        return "historical-replay"

    def provider_summary(self) -> LiveProviderCatalog:
        return build_provider_catalog("historical-replay")

    def _build_replay_telemetry(self, request: LiveRaceRequest) -> list[LiveTelemetryPoint]:
        detail = self.history_service.get_race_detail(request.race_id)
        driver_rank = self._driver_rank(detail.drivers, request.driver_code)
        sample_count = min(request.sample_size, max(4, detail.laps - request.start_lap))
        points: list[LiveTelemetryPoint] = []

        for offset in range(sample_count):
            lap = min(detail.laps - 1, request.start_lap + offset * 2)
            tyre_age = max(1, detail.tire_age_laps + offset * 2)
            weather_risk = min(1.0, 0.06 + 0.03 * offset + (0.08 if detail.weather_risk == "Elevated" else 0.02))
            sc_probability = min(0.95, detail.safety_car_probability + 0.015 * offset)
            rival_pitted = offset in {2, 5}
            vsc_active = offset == sample_count - 2
            last_lap = self.model_lab_service.predict_push_lap_time(
                race_state=RaceState(
                    driver_code=request.driver_code,
                    current_lap=lap,
                    total_laps=detail.laps,
                    current_compound=detail.current_compound,
                    tire_age_laps=tyre_age,
                    pit_loss_seconds=detail.pit_loss_seconds,
                    base_lap_time_seconds=detail.base_lap_time_seconds,
                    fuel_penalty_per_lap=detail.fuel_penalty_per_lap,
                    safety_car_probability=sc_probability,
                    degradation_per_lap=detail.degradation_per_lap,
                    max_pit_stops=3,
                    compound_delta_seconds=detail.compound_delta_seconds,
                ),
                driver_code=request.driver_code,
                race_id=request.race_id,
                grid_position=driver_rank,
            )
            traffic_index = max(0.02, min(0.95, 0.18 + 0.08 * sin(offset + driver_rank / 4)))
            telemetry = LiveTelemetryPoint(
                lap=lap,
                sector_1_seconds=round(last_lap * 0.31, 3),
                sector_2_seconds=round(last_lap * 0.34, 3),
                sector_3_seconds=round(last_lap * 0.35, 3),
                gap_ahead_seconds=round(max(0.3, 1.4 + offset * 0.35 - driver_rank * 0.05), 2),
                gap_behind_seconds=round(max(0.4, 1.1 + (sample_count - offset) * 0.28), 2),
                last_lap_seconds=last_lap,
                tyre_age_laps=tyre_age,
                fuel_load_index=round(max(0.05, (detail.laps - lap) / detail.laps), 2),
                traffic_index=round(traffic_index, 2),
                weather_risk=round(weather_risk, 2),
                safety_car_probability=round(sc_probability, 2),
                rival_pitted=rival_pitted,
                vsc_active=vsc_active,
            )
            points.append(telemetry)
        return points

    def _build_replay_weather(self, request: LiveRaceRequest) -> list[LiveWeatherPoint]:
        detail = self.history_service.get_race_detail(request.race_id)
        sample_count = min(request.sample_size, max(4, detail.laps - request.start_lap))
        points: list[LiveWeatherPoint] = []
        for offset in range(sample_count):
            rain_probability = min(0.8, 0.06 + offset * 0.04 + (0.12 if detail.weather_risk == "Elevated" else 0.02))
            points.append(
                LiveWeatherPoint(
                    air_temperature_c=round(24.0 + sin(offset / 2) * 1.8, 1),
                    track_temperature_c=round(31.0 + sin(offset / 2 + 0.5) * 3.4, 1),
                    rain_probability=round(rain_probability, 2),
                    humidity=round(min(0.92, 0.46 + offset * 0.05), 2),
                    wind_speed_kph=round(8.0 + offset * 1.2, 1),
                    condition="Showers threat" if rain_probability >= 0.24 else "Dry running",
                )
            )
        return points

    def _build_replay_events(self, request: LiveRaceRequest) -> list[list[LiveRaceEvent]]:
        detail = self.history_service.get_race_detail(request.race_id)
        sample_count = min(request.sample_size, max(4, detail.laps - request.start_lap))
        points: list[list[LiveRaceEvent]] = []
        for offset in range(sample_count):
            lap = min(detail.laps - 1, request.start_lap + offset * 2)
            events = [
                LiveRaceEvent(
                    lap=lap,
                    category="timing",
                    title="Pace update",
                    detail="Sector balance remains stable across the last flying lap.",
                    impact="low",
                )
            ]
            if offset in {2, 5}:
                events.append(
                    LiveRaceEvent(
                        lap=lap,
                        category="pit",
                        title="Rival pitted",
                        detail="A nearby rival boxed, increasing undercut protection pressure.",
                        impact="high",
                    )
                )
            if offset == sample_count - 2:
                events.append(
                    LiveRaceEvent(
                        lap=lap,
                        category="control",
                        title="VSC watch",
                        detail="Control projection suggests elevated VSC/SC likelihood in the next window.",
                        impact="medium",
                    )
                )
            if offset >= 3:
                events.append(
                    LiveRaceEvent(
                        lap=lap,
                        category="weather",
                        title="Rain trend",
                        detail="Rain probability trend is rising, increasing crossover sensitivity.",
                        impact="medium",
                    )
                )
            points.append(events)
        return points

    def _recommend(
        self,
        race_id: str,
        driver_code: str,
        telemetry: LiveTelemetryPoint,
        detail,
    ) -> LiveDecisionRecommendation:
        tyre_cliff_score = telemetry.tyre_age_laps * detail.degradation_per_lap
        traffic_loss = round(telemetry.traffic_index * 2.8 + max(0, 1.2 - telemetry.gap_ahead_seconds), 2)
        undercut_gain = round(
            max(0.1, tyre_cliff_score * 0.95 + (0.9 if telemetry.rival_pitted else 0.25) + telemetry.safety_car_probability * 1.2),
            2,
        )
        overcut_risk = round(max(0.1, traffic_loss * 0.8 + tyre_cliff_score * 0.7), 2)
        pit_now = undercut_gain > overcut_risk or telemetry.vsc_active
        action = "BOX THIS LAP" if pit_now else "STAY OUT"
        headline = "Attack the undercut now" if pit_now else "Extend the stint"
        tyre_cliff_risk = "High" if tyre_cliff_score > 1.8 else "Medium" if tyre_cliff_score > 1.1 else "Low"
        reasons = [
            f"Undercut projection {undercut_gain:.2f}s versus overcut risk {overcut_risk:.2f}s.",
            f"Traffic loss after pit exit projected at {traffic_loss:.2f}s.",
            f"Tyre cliff risk is {tyre_cliff_risk.lower()} with age {telemetry.tyre_age_laps} laps.",
        ]
        if telemetry.rival_pitted:
            reasons.append("A nearby rival has pitted, so undercut protection became more valuable.")
        if telemetry.safety_car_probability >= 0.24:
            reasons.append("Safety car probability rose, making Plan B more viable.")
        if telemetry.weather_risk >= 0.22:
            reasons.append("Weather risk increased and pushes the crossover window earlier.")

        confidence = max(0.52, min(0.94, 0.62 + undercut_gain * 0.06 - traffic_loss * 0.03))
        pit_window_start = max(telemetry.lap, telemetry.lap - 1)
        pit_window_end = min(detail.laps - 1, telemetry.lap + 3)

        return LiveDecisionRecommendation(
            headline=headline,
            action=action,
            confidence=round(confidence, 2),
            pit_window_start=pit_window_start,
            pit_window_end=pit_window_end,
            undercut_gain_seconds=undercut_gain,
            overcut_risk_seconds=overcut_risk,
            traffic_loss_seconds=traffic_loss,
            tyre_cliff_risk=tyre_cliff_risk,
            plan_b_trigger=f"Switch to Plan B if SC/VSC arrives between L{pit_window_start}-L{pit_window_end}.",
            reasons=reasons,
        )

    def build_engineer_request(self, race_id: str, driver_code: str, telemetry: LiveTelemetryPoint) -> RaceEngineerRequest:
        detail = self.history_service.get_race_detail(race_id)
        return RaceEngineerRequest(
            race_id=race_id,
            driver_code=driver_code,
            grid_position=self._driver_rank(detail.drivers, driver_code),
            gap_ahead_seconds=telemetry.gap_ahead_seconds,
            gap_behind_seconds=telemetry.gap_behind_seconds,
            weather_risk=telemetry.weather_risk,
            traffic_risk=telemetry.traffic_index,
            safety_car_window_start=max(1, telemetry.lap - 1),
            safety_car_window_end=min(detail.laps, telemetry.lap + 3),
            race_state=RaceState(
                driver_code=driver_code,
                current_lap=telemetry.lap,
                total_laps=detail.laps,
                current_compound=detail.current_compound,
                tire_age_laps=telemetry.tyre_age_laps,
                pit_loss_seconds=detail.pit_loss_seconds,
                base_lap_time_seconds=detail.base_lap_time_seconds,
                fuel_penalty_per_lap=detail.fuel_penalty_per_lap,
                safety_car_probability=telemetry.safety_car_probability,
                degradation_per_lap=detail.degradation_per_lap,
                max_pit_stops=3,
                compound_delta_seconds=detail.compound_delta_seconds,
            ),
        )

    def _driver_rank(self, drivers: list[str], driver_code: str) -> int:
        try:
            return max(1, drivers.index(driver_code) + 1)
        except ValueError:
            return 10
