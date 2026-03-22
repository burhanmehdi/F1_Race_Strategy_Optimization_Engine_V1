from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from f1_strategy_engine.domain.models import (
    LiveProviderCatalog,
    LiveProviderDescriptor,
    LiveRaceEvent,
    LiveRaceRequest,
    LiveTelemetryPoint,
    LiveWeatherPoint,
)


class TimingFeedProvider(Protocol):
    provider_name: str
    provider_mode: str
    description: str

    def telemetry_stream(self, request: LiveRaceRequest) -> list[LiveTelemetryPoint]:
        ...


class WeatherFeedProvider(Protocol):
    provider_name: str
    provider_mode: str
    description: str

    def weather_stream(self, request: LiveRaceRequest) -> list[LiveWeatherPoint]:
        ...


class EventFeedProvider(Protocol):
    provider_name: str
    provider_mode: str
    description: str

    def event_stream(self, request: LiveRaceRequest) -> list[list[LiveRaceEvent]]:
        ...


@dataclass(frozen=True)
class HistoricalReplayTimingProvider:
    builder: Callable[[LiveRaceRequest], list[LiveTelemetryPoint]]
    provider_name: str = "historical-replay-timing"
    provider_mode: str = "replay"
    description: str = "Synthetic lap-by-lap timing replay built from historical race context."

    def telemetry_stream(self, request: LiveRaceRequest) -> list[LiveTelemetryPoint]:
        return self.builder(request)


@dataclass(frozen=True)
class HistoricalReplayWeatherProvider:
    builder: Callable[[LiveRaceRequest], list[LiveWeatherPoint]]
    provider_name: str = "historical-replay-weather"
    provider_mode: str = "replay"
    description: str = "Synthetic weather replay matched to the selected historical race."

    def weather_stream(self, request: LiveRaceRequest) -> list[LiveWeatherPoint]:
        return self.builder(request)


@dataclass(frozen=True)
class HistoricalReplayEventProvider:
    builder: Callable[[LiveRaceRequest], list[list[LiveRaceEvent]]]
    provider_name: str = "historical-replay-events"
    provider_mode: str = "replay"
    description: str = "Synthetic event feed for rival pits, SC/VSC changes, and traffic alerts."

    def event_stream(self, request: LiveRaceRequest) -> list[list[LiveRaceEvent]]:
        return self.builder(request)


@dataclass(frozen=True)
class ExternalTimingFeedBlueprint:
    provider_name: str = "external-timing-blueprint"
    provider_mode: str = "external"
    description: str = "Adapter scaffold for a real external lap timing / sector feed."

    def telemetry_stream(self, request: LiveRaceRequest) -> list[LiveTelemetryPoint]:
        raise NotImplementedError("Connect this timing adapter to a real live timing source.")


@dataclass(frozen=True)
class ExternalWeatherFeedBlueprint:
    provider_name: str = "external-weather-blueprint"
    provider_mode: str = "external"
    description: str = "Adapter scaffold for real weather observations and forecast updates."

    def weather_stream(self, request: LiveRaceRequest) -> list[LiveWeatherPoint]:
        raise NotImplementedError("Connect this weather adapter to a real weather source.")


@dataclass(frozen=True)
class ExternalEventFeedBlueprint:
    provider_name: str = "external-event-blueprint"
    provider_mode: str = "external"
    description: str = "Adapter scaffold for incident, pit, and control message events."

    def event_stream(self, request: LiveRaceRequest) -> list[list[LiveRaceEvent]]:
        raise NotImplementedError("Connect this event adapter to a real live event source.")


def build_provider_catalog(active_mode: str = "historical-replay") -> LiveProviderCatalog:
    providers = [
        LiveProviderDescriptor(
            provider_name="historical-replay",
            provider_mode="replay",
            status="active" if active_mode == "historical-replay" else "available",
            description="Current working local provider for live strategy demos.",
        ),
        LiveProviderDescriptor(
            provider_name="external-timing-blueprint",
            provider_mode="external",
            status="blueprint",
            description="Plug real sector timing and gaps into the race wall.",
        ),
        LiveProviderDescriptor(
            provider_name="external-weather-blueprint",
            provider_mode="external",
            status="blueprint",
            description="Plug real weather nowcasts and radar risk into the race wall.",
        ),
        LiveProviderDescriptor(
            provider_name="external-event-blueprint",
            provider_mode="external",
            status="blueprint",
            description="Plug pit events, flags, incidents, and control messages into the race wall.",
        ),
    ]
    return LiveProviderCatalog(
        active_provider=active_mode,
        mode="replay" if active_mode == "historical-replay" else "external",
        available_providers=providers,
    )
