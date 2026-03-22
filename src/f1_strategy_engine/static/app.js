const form = document.getElementById("optimizer-form");
const navPills = document.querySelectorAll(".topnav .nav-pill");
const views = document.querySelectorAll(".view");
const compoundPills = document.querySelectorAll(".compound-pill");

const globalSeason = document.getElementById("global-season");
const globalRace = document.getElementById("global-race");
const globalCircuit = document.getElementById("global-circuit");
const seasonTag = document.getElementById("season-tag");
const contextRaceSummary = document.getElementById("context-race-summary");
const contextRaceNote = document.getElementById("context-race-note");
const contextUsageChips = document.getElementById("context-usage-chips");
const contextSectionMap = document.getElementById("context-section-map");
const contextTrackTitle = document.getElementById("context-track-title");
const contextTrackMeta = document.getElementById("context-track-meta");
const contextTrackBias = document.getElementById("context-track-bias");
const contextTrackPitloss = document.getElementById("context-track-pitloss");
const contextTrackSc = document.getElementById("context-track-sc");
const contextTrackOvertake = document.getElementById("context-track-overtake");
const liveDriver = document.getElementById("live-driver");
const liveProviderName = document.getElementById("live-provider-name");
const liveStartLap = document.getElementById("live-start-lap");
const liveSampleSize = document.getElementById("live-sample-size");
const liveSampleSizeLabel = document.getElementById("live-sample-size-label");
const startLiveRaceButton = document.getElementById("start-live-race");
const liveRaceStatus = document.getElementById("live-race-status");
const liveStatusChip = document.getElementById("live-status-chip");
const liveHeadline = document.getElementById("live-headline");
const liveSubheadline = document.getElementById("live-subheadline");
const liveAction = document.getElementById("live-action");
const liveLap = document.getElementById("live-lap");
const liveConfidence = document.getElementById("live-confidence");
const livePlanB = document.getElementById("live-plan-b");
const liveUndercut = document.getElementById("live-undercut");
const liveTrafficLoss = document.getElementById("live-traffic-loss");
const liveTyreCliff = document.getElementById("live-tyre-cliff");
const liveTelemetryGrid = document.getElementById("live-telemetry-grid");
const liveWeatherGrid = document.getElementById("live-weather-grid");
const liveEventLog = document.getElementById("live-event-log");
const liveReasons = document.getElementById("live-reasons");
const liveScenarioNotes = document.getElementById("live-scenario-notes");

const summaryTime = document.getElementById("summary-time");
const summaryConfidence = document.getElementById("summary-confidence");
const summaryStops = document.getElementById("summary-stops");
const recommendedName = document.getElementById("recommended-name");
const recommendedExplanation = document.getElementById("recommended-explanation");
const pitStopTags = document.getElementById("pit-stop-tags");
const timelineTrack = document.getElementById("timeline-track");
const timelineCaption = document.getElementById("timeline-caption");
const degradationNote = document.getElementById("degradation-note");
const degradationBias = document.getElementById("degradation-bias");
const scProbability = document.getElementById("sc-probability");
const optimizerStatus = document.getElementById("optimizer-status");
const resultsLoading = document.getElementById("results-loading");
const optimizerDriver = document.getElementById("optimizer-driver");
const optimizerRanked = document.getElementById("optimizer-ranked");
const engineerDriver = document.getElementById("engineer-driver");
const engineerGridPosition = document.getElementById("engineer-grid-position");
const engineerGapAhead = document.getElementById("engineer-gap-ahead");
const engineerGapBehind = document.getElementById("engineer-gap-behind");
const engineerWeatherRisk = document.getElementById("engineer-weather-risk");
const engineerTrafficRisk = document.getElementById("engineer-traffic-risk");
const engineerWeatherLabel = document.getElementById("engineer-weather-label");
const engineerTrafficLabel = document.getElementById("engineer-traffic-label");
const engineerScWindowStart = document.getElementById("engineer-sc-window-start");
const engineerScWindowEnd = document.getElementById("engineer-sc-window-end");
const runRaceEngineerButton = document.getElementById("run-race-engineer");
const raceEngineerStatus = document.getElementById("race-engineer-status");
const engineerPushLap = document.getElementById("engineer-push-lap");
const engineerHeadline = document.getElementById("engineer-headline");
const engineerDriverHero = document.getElementById("engineer-driver-hero");
const engineerConfidence = document.getElementById("engineer-confidence");
const engineerPrimaryTrigger = document.getElementById("engineer-primary-trigger");
const engineerFallbackTrigger = document.getElementById("engineer-fallback-trigger");
const engineerPrimaryName = document.getElementById("engineer-primary-name");
const engineerPrimaryTime = document.getElementById("engineer-primary-time");
const engineerPrimaryTags = document.getElementById("engineer-primary-tags");
const engineerFallbackName = document.getElementById("engineer-fallback-name");
const engineerFallbackTime = document.getElementById("engineer-fallback-time");
const engineerFallbackTags = document.getElementById("engineer-fallback-tags");
const engineerAssumptions = document.getElementById("engineer-assumptions");
const engineerCallouts = document.getElementById("engineer-callouts");
const engineerSensitivities = document.getElementById("engineer-sensitivities");
const scenarioCompareGrid = document.getElementById("scenario-compare-grid");

const heroWinProbability = document.getElementById("hero-win-probability");
const heroImprovement = document.getElementById("hero-improvement");
const heroRiskLevel = document.getElementById("hero-risk-level");
const heroDriver = document.getElementById("hero-driver");
const baselineName = document.getElementById("baseline-name");
const baselineTime = document.getElementById("baseline-time");
const optimizedTime = document.getElementById("optimized-time");
const optimizedDelta = document.getElementById("optimized-delta");
const changeHeadline = document.getElementById("change-headline");
const changeDriverChip = document.getElementById("change-driver-chip");
const changeTimeChip = document.getElementById("change-time-chip");
const changePlanChip = document.getElementById("change-plan-chip");
const resultsPanel = document.getElementById("results-panel");

const pitstopTitle = document.getElementById("pitstop-title");
const pitstopSubtitle = document.getElementById("pitstop-subtitle");
const pitstopTotal = document.getElementById("pitstop-total");
const pitstopBias = document.getElementById("pitstop-bias");
const boardScale = document.getElementById("board-scale");
const pitstopBoard = document.getElementById("pitstop-board");

const simulationGrid = document.getElementById("simulation-grid");
const simulationStatus = document.getElementById("simulation-status");
const simDriver = document.getElementById("sim-driver");
const simCount = document.getElementById("sim-count");
const simCountLabel = document.getElementById("sim-count-label");
const gridPosition = document.getElementById("grid-position");
const gridPositionLabel = document.getElementById("grid-position-label");
const runSimulationButton = document.getElementById("run-simulation");

const archiveCount = document.getElementById("archive-count");
const archiveSeasonFilter = document.getElementById("archive-season-filter");
const archiveCircuitFilter = document.getElementById("archive-circuit-filter");
const archiveSearch = document.getElementById("archive-search");
const archiveTableBody = document.getElementById("archive-table-body");
const archiveDetail = document.getElementById("archive-detail");
const degradationSpecs = document.getElementById("degradation-specs");
const modelLabGeneratedAt = document.getElementById("model-lab-generated-at");
const modelLabCards = document.getElementById("model-lab-cards");
const modelLabBacktestBody = document.getElementById("model-lab-backtest-body");
const modelLabCalibration = document.getElementById("model-lab-calibration");
const runModelLabButton = document.getElementById("run-model-lab");
const modelLabStatus = document.getElementById("model-lab-status");

const compoundClasses = {
  SOFT: "soft",
  MEDIUM: "medium",
  HARD: "hard",
};

let catalog = null;
let currentRaceDetail = null;
let latestResult = null;
let latestPayload = null;
let currentCompoundFilter = "ALL";
let selectedArchiveRaceId = null;
let currentDrivers = [];
let modelLabLoaded = false;
let activeViewName = "pitstops";
let liveRaceSocket = null;
let platformSummary = null;
const contextUsageByView = {
  live: {
    label: "Live Race",
    scope: "direct",
    summary: "Streams telemetry-aware strategy calls for the selected race and driver in a race-wall style view.",
  },
  raceengineer: {
    label: "Race Engineer",
    scope: "direct",
    summary: "Uses the selected race to set the strategy window, pit loss, lap count, and scenario assumptions.",
  },
  pitstops: {
    label: "Pit Stops",
    scope: "direct",
    summary: "Loads the exact selected race board, driver rows, and pit-stop history.",
  },
  optimizer: {
    label: "Optimizer",
    scope: "direct",
    summary: "Pre-fills the optimizer with the selected race defaults, tyre assumptions, and timing model inputs.",
  },
  simulation: {
    label: "Simulation",
    scope: "context",
    summary: "Uses the selected race context for lap count, field profile, and scenario tuning before Monte Carlo runs.",
  },
  degradation: {
    label: "Degradation",
    scope: "context",
    summary: "Adapts the tyre trend lines to the selected race pace and compound profile.",
  },
  archive: {
    label: "Race Archive",
    scope: "direct",
    summary: "Shows the selected race as the active archive reference and detail panel.",
  },
  modellab: {
    label: "Model Lab",
    scope: "reference",
    summary: "Trains and evaluates on all historical data, while the selected race acts as the reference lens for interpretation.",
  },
};

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainder = (seconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${remainder}`;
}

function setActiveView(name) {
  activeViewName = name;
  navPills.forEach((pill) => pill.classList.toggle("active", pill.dataset.tab === name));
  views.forEach((view) => view.classList.toggle("active", view.dataset.view === name));
  if (window.location.hash !== `#${name}`) {
    window.history.replaceState(null, "", `#${name}`);
  }
  renderContextGuide();
}

function getInitialViewName() {
  const hashView = window.location.hash.replace("#", "").trim().toLowerCase();
  const supportedViews = new Set(Array.from(views).map((view) => view.dataset.view));
  return supportedViews.has(hashView) ? hashView : "pitstops";
}

function scopeLabel(scope) {
  if (scope === "direct") {
    return "Direct";
  }
  if (scope === "context") {
    return "Context";
  }
  return "Reference";
}

function renderContextGuide() {
  if (!contextRaceSummary || !contextRaceNote || !contextUsageChips) {
    return;
  }

  if (!currentRaceDetail) {
    contextRaceSummary.textContent = "Waiting for race load";
    contextRaceNote.textContent = "Choose a season, Grand Prix, and circuit to update linked sections.";
    contextUsageChips.innerHTML = "";
    if (contextTrackTitle) {
      contextTrackTitle.textContent = "Waiting for race load";
      contextTrackMeta.textContent = "Circuit profile, risk balance, and race characteristics will appear here.";
      contextTrackBias.textContent = "--";
      contextTrackPitloss.textContent = "--";
      contextTrackSc.textContent = "--";
      contextTrackOvertake.textContent = "--";
    }
    if (contextSectionMap) {
      contextSectionMap.innerHTML = "";
    }
    return;
  }

  contextRaceSummary.textContent = `${currentRaceDetail.season} ${currentRaceDetail.grand_prix} - ${currentRaceDetail.circuit}`;
  contextRaceNote.textContent = "This race selection updates shared defaults, race history, simulation context, and archive reference data across the dashboard.";

  const chipOrder = ["live", "pitstops", "optimizer", "simulation", "degradation", "raceengineer", "archive", "modellab"];
  contextUsageChips.innerHTML = chipOrder.map((view) => {
    const config = contextUsageByView[view];
    return `<span class="context-chip ${config.scope}">${config.label}</span>`;
  }).join("");

  if (contextTrackTitle) {
    contextTrackTitle.textContent = `${currentRaceDetail.grand_prix}`;
    contextTrackMeta.textContent = `${currentRaceDetail.circuit} • ${currentRaceDetail.country} • ${currentRaceDetail.laps} laps`;
    contextTrackBias.textContent = currentRaceDetail.strategy_bias;
    contextTrackPitloss.textContent = `${Number(currentRaceDetail.pit_loss_seconds).toFixed(1)}s`;
    contextTrackSc.textContent = `${Math.round(Number(currentRaceDetail.safety_car_probability) * 100)}%`;
    contextTrackOvertake.textContent = currentRaceDetail.overtake_difficulty;
  }

  if (contextSectionMap) {
    contextSectionMap.innerHTML = "";
  }
}

function setLoading(isLoading, label = "Running") {
  resultsLoading.hidden = !isLoading;
  optimizerStatus.textContent = isLoading ? label : "Ready";
}

function closeLiveRaceSocket() {
  if (liveRaceSocket) {
    liveRaceSocket.close();
    liveRaceSocket = null;
  }
}

function renderLiveRaceSnapshot(snapshot) {
  if (!snapshot) {
    return;
  }
  liveHeadline.textContent = snapshot.recommendation.headline;
  liveSubheadline.textContent = snapshot.recommendation.reasons[0] || "Telemetry-aware recommendation updated.";
  liveAction.textContent = snapshot.recommendation.action;
  liveLap.textContent = `L${snapshot.telemetry.lap}`;
  liveConfidence.textContent = `${Math.round(snapshot.recommendation.confidence * 100)}%`;
  livePlanB.textContent = `L${snapshot.recommendation.pit_window_start}-${snapshot.recommendation.pit_window_end}`;
  liveUndercut.textContent = `${snapshot.recommendation.undercut_gain_seconds.toFixed(2)}s`;
  liveTrafficLoss.textContent = `${snapshot.recommendation.traffic_loss_seconds.toFixed(2)}s`;
  liveTyreCliff.textContent = snapshot.recommendation.tyre_cliff_risk;

  liveTelemetryGrid.innerHTML = [
    ["Last Lap", `${snapshot.telemetry.last_lap_seconds.toFixed(3)}s`],
    ["S1", `${snapshot.telemetry.sector_1_seconds.toFixed(3)}s`],
    ["S2", `${snapshot.telemetry.sector_2_seconds.toFixed(3)}s`],
    ["S3", `${snapshot.telemetry.sector_3_seconds.toFixed(3)}s`],
    ["Gap Ahead", `${snapshot.telemetry.gap_ahead_seconds.toFixed(2)}s`],
    ["Gap Behind", `${snapshot.telemetry.gap_behind_seconds.toFixed(2)}s`],
    ["Tyre Age", `${snapshot.telemetry.tyre_age_laps} laps`],
    ["Traffic", `${Math.round(snapshot.telemetry.traffic_index * 100)}%`],
    ["SC Risk", `${Math.round(snapshot.telemetry.safety_car_probability * 100)}%`],
  ].map(([label, value]) => `
    <div class="detail-box">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `).join("");

  liveWeatherGrid.innerHTML = [
    ["Air Temp", `${snapshot.weather.air_temperature_c.toFixed(1)} C`],
    ["Track Temp", `${snapshot.weather.track_temperature_c.toFixed(1)} C`],
    ["Rain Risk", `${Math.round(snapshot.weather.rain_probability * 100)}%`],
    ["Humidity", `${Math.round(snapshot.weather.humidity * 100)}%`],
    ["Wind", `${snapshot.weather.wind_speed_kph.toFixed(1)} kph`],
    ["Condition", snapshot.weather.condition],
  ].map(([label, value]) => `
    <div class="detail-box">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `).join("");

  liveEventLog.innerHTML = snapshot.events.map((event) => `<li><strong>${event.title}:</strong> ${event.detail}</li>`).join("");
  liveReasons.innerHTML = snapshot.recommendation.reasons.map((reason) => `<li>${reason}</li>`).join("");
  liveScenarioNotes.innerHTML = snapshot.scenario_notes.map((note) => `<li>${note}</li>`).join("");
}

function startLiveRaceFeed() {
  if (!currentRaceDetail || !liveDriver) {
    return;
  }
  closeLiveRaceSocket();
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const params = new URLSearchParams({
    race_id: currentRaceDetail.race_id,
    driver_code: liveDriver.value,
    start_lap: String(Number(liveStartLap.value || 14)),
    sample_size: String(Number(liveSampleSize.value || 8)),
  });
  const backendLabel = platformSummary ? `${platformSummary.engine} / ${platformSummary.live_provider}` : "live provider";
  liveRaceStatus.textContent = `Connecting to ${backendLabel} telemetry stream...`;
  liveStatusChip.textContent = "Connecting";
  liveRaceSocket = new WebSocket(`${protocol}://${window.location.host}/ws/live-race?${params.toString()}`);
  liveRaceSocket.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    if (payload.event === "complete") {
      liveRaceStatus.textContent = "Live feed complete. Restart to replay the race wall stream.";
      liveStatusChip.textContent = "Complete";
      return;
    }
    if (payload.event === "error") {
      liveRaceStatus.textContent = `Live feed failed: ${payload.detail}`;
      liveStatusChip.textContent = "Error";
      return;
    }
    renderLiveRaceSnapshot(payload);
    liveRaceStatus.textContent = `${payload.driver_code} live update received for lap ${payload.telemetry.lap}.`;
    liveStatusChip.textContent = "Streaming";
  };
  liveRaceSocket.onerror = () => {
    liveRaceStatus.textContent = "Live feed connection failed.";
    liveStatusChip.textContent = "Error";
  };
  liveRaceSocket.onclose = () => {
    if (liveStatusChip.textContent === "Streaming") {
      liveStatusChip.textContent = "Closed";
    }
  };
}

async function fetchJson(url, timeoutMs = 8000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  const response = await fetch(url, { signal: controller.signal });
  clearTimeout(timeoutId);
  if (!response.ok) {
    throw new Error(`Request failed: ${url}`);
  }
  return response.json();
}

function buildPayload() {
  const formData = new FormData(form);
  return {
    driver_code: String(formData.get("driver_code") || ""),
    current_lap: Number(formData.get("current_lap")),
    total_laps: Number(formData.get("total_laps")),
    current_compound: String(formData.get("current_compound")),
    tire_age_laps: Number(formData.get("tire_age_laps")),
    pit_loss_seconds: Number(formData.get("pit_loss_seconds")),
    base_lap_time_seconds: Number(formData.get("base_lap_time_seconds")),
    fuel_penalty_per_lap: Number(formData.get("fuel_penalty_per_lap")),
    safety_car_probability: Number(formData.get("safety_car_probability")),
    degradation_per_lap: Number(formData.get("degradation_per_lap")),
    max_pit_stops: Number(formData.get("max_pit_stops")),
    compound_delta_seconds: Number(formData.get("compound_delta_seconds")),
  };
}

function describeDriver(code) {
  const driver = currentDrivers.find((item) => item.code === code);
  return driver ? `${driver.code} ${driver.name.split(" ").slice(-1)[0]}` : code || "--";
}

function markResultsUpdated() {
  resultsPanel.classList.remove("result-updated");
  void resultsPanel.offsetWidth;
  resultsPanel.classList.add("result-updated");
}

function updateChangeBanner(previousPayload, previousResult, payload, result) {
  const driverLabel = describeDriver(result.driver_code || payload.driver_code);
  const paceDelta = result.driver_pace_delta_seconds || 0;
  const paceDirection = paceDelta <= 0 ? "quicker" : "slower";

  if (!previousResult || !previousPayload) {
    changeHeadline.textContent = `Primary recommendation loaded for ${driverLabel}`;
    changeDriverChip.textContent = `Driver pace ${Math.abs(paceDelta).toFixed(2)}s/lap ${paceDirection}`;
    changeTimeChip.textContent = `Expected time ${formatTime(result.recommended.expected_race_time_seconds)}`;
    changePlanChip.textContent = `Plan ${result.recommended.plan.name}`;
    return;
  }

  const timeShift = result.recommended.expected_race_time_seconds - previousResult.recommended.expected_race_time_seconds;
  const driverChanged = previousPayload.driver_code !== payload.driver_code;
  const planChanged = previousResult.recommended.plan.name !== result.recommended.plan.name;
  const timeVerb = timeShift < 0 ? "faster" : timeShift > 0 ? "slower" : "unchanged";

  changeHeadline.textContent = driverChanged
    ? `Optimizer updated from ${describeDriver(previousPayload.driver_code)} to ${driverLabel}`
    : `Optimizer refreshed for ${driverLabel}`;
  changeDriverChip.textContent = driverChanged
    ? `Driver swap ${describeDriver(previousPayload.driver_code)} -> ${driverLabel}`
    : `Driver pace ${Math.abs(paceDelta).toFixed(2)}s/lap ${paceDirection}`;
  changeTimeChip.textContent = `Race time ${Math.abs(timeShift).toFixed(2)}s ${timeVerb}`;
  changePlanChip.textContent = planChanged
    ? `Plan changed to ${result.recommended.plan.name}`
    : `Plan unchanged: ${result.recommended.plan.name}`;
}

function getSeasonRaces(season) {
  return catalog.races.filter((race) => String(race.season) === String(season));
}

function populateGlobalSelectors(preferredRaceId = null) {
  const seasons = catalog.seasons.map(String);
  if (!globalSeason.options.length) {
    globalSeason.innerHTML = seasons.map((season) => `<option value="${season}">${season}</option>`).join("");
  }

  const seasonRaces = getSeasonRaces(globalSeason.value || seasons[seasons.length - 1]);
  globalRace.innerHTML = seasonRaces.map((race) => `<option value="${race.race_id}">${race.round}. ${race.grand_prix}</option>`).join("");

  const activeRace = seasonRaces.find((race) => race.race_id === preferredRaceId) || seasonRaces[0];
  if (activeRace) {
    globalRace.value = activeRace.race_id;
  }

  globalCircuit.innerHTML = seasonRaces
    .map((race) => `<option value="${race.race_id}">${race.circuit}</option>`)
    .join("");

  if (activeRace) {
    globalCircuit.value = activeRace.race_id;
  }
}

function populateDriverDropdowns() {
  const options = currentDrivers
    .map((driver) => `<option value="${driver.code}">${driver.code} - ${driver.name} (${driver.team})</option>`)
    .join("");
  simDriver.innerHTML = options;
  optimizerDriver.innerHTML = options;
  engineerDriver.innerHTML = options;
  if (liveDriver) {
    liveDriver.innerHTML = options;
  }
}

function renderPitstopBoard() {
  if (!currentRaceDetail) {
    return;
  }

  boardScale.innerHTML = ["", "1", "10", "20", "30", "40", "50", "60", String(currentRaceDetail.laps), ""]
    .map((item) => `<span>${item}</span>`)
    .join("");

  pitstopBoard.innerHTML = "";
  let totalStops = 0;

  currentRaceDetail.pitstop_rows.forEach((row) => {
    const shownStints = row.stints.filter((stint) => currentCompoundFilter === "ALL" || stint.compound === currentCompoundFilter);
    if (!shownStints.length) {
      return;
    }

    totalStops += Math.max(0, row.stints.length - 1);
    const totalLaps = row.stints.reduce((sum, stint) => sum + stint.laps, 0);
    const tooltipLabel = currentDrivers.find((driver) => driver.code === row.driver_code);
    const tooltipTitle = tooltipLabel ? `${tooltipLabel.name}` : row.driver_code;
    const tooltipTeam = tooltipLabel ? tooltipLabel.team : "Historical race reference";
    const tooltipStints = row.stints
      .map((stint, index) => `L${index === 0 ? 1 : row.stints.slice(0, index).reduce((sum, item) => sum + item.laps, 0) + 1}-L${row.stints.slice(0, index + 1).reduce((sum, item) => sum + item.laps, 0)}  ${stint.compound}  ${stint.laps} laps`)
      .join("");
    const stintHtml = shownStints.map((stint) => {
      const width = (stint.laps / totalLaps) * 100;
      return `<div class="stint ${compoundClasses[stint.compound]} ${stint.used ? "used" : ""}" style="width:${width}%">${stint.laps}</div>`;
    }).join("");

    const node = document.createElement("div");
    node.className = "pitstop-row";
    node.innerHTML = `
      <div class="driver-code">${row.driver_code}</div>
      <div class="stint-row-wrap">
        <div class="stint-row">${stintHtml}</div>
        <div class="pitstop-tooltip">
          <strong>${tooltipTitle}</strong>
          <span>${tooltipTeam}</span>
          <div class="tooltip-stints">${row.stints.map((stint, index) => {
            const startLap = index === 0 ? 1 : row.stints.slice(0, index).reduce((sum, item) => sum + item.laps, 0) + 1;
            const endLap = row.stints.slice(0, index + 1).reduce((sum, item) => sum + item.laps, 0);
            return `<div><em class="${compoundClasses[stint.compound]}"></em><span>L${startLap}-L${endLap}</span><strong>${stint.laps} laps</strong></div>`;
          }).join("")}</div>
        </div>
      </div>
      <div class="laps-finish">${row.finish_lap}</div>
    `;
    pitstopBoard.appendChild(node);
  });

  pitstopTotal.textContent = totalStops;
  pitstopBias.textContent = `${currentRaceDetail.strategy_bias} • ${currentRaceDetail.overtake_difficulty} overtaking`;
}

function renderPitStops(stops) {
  pitStopTags.innerHTML = "";
  stops.forEach((stop, index) => {
    const tag = document.createElement("div");
    tag.className = `pit-tag ${compoundClasses[stop.new_compound]}`;
    tag.textContent = `Stop ${index + 1}: Lap ${stop.lap} to ${stop.new_compound}`;
    pitStopTags.appendChild(tag);
  });
}

function renderTimeline(payload, plan) {
  timelineTrack.innerHTML = "";
  const stops = [...plan.pit_stops].sort((a, b) => a.lap - b.lap);
  const boundaries = [payload.current_lap, ...stops.map((stop) => stop.lap), payload.total_laps + 1];
  const compounds = [payload.current_compound, ...stops.map((stop) => stop.new_compound)];

  for (let index = 0; index < compounds.length; index += 1) {
    const startLap = boundaries[index];
    const endLap = boundaries[index + 1] - 1;
    const span = Math.max(1, endLap - startLap + 1);
    const segment = document.createElement("div");
    segment.className = `timeline-segment segment-${compoundClasses[compounds[index]]}`;
    segment.style.flex = `${span} 1 0`;
    segment.innerHTML = `<span>${compounds[index]}</span><small>L${startLap}-L${endLap}</small>`;
    timelineTrack.appendChild(segment);
  }

  timelineCaption.textContent = `${plan.pit_stops.length} stop${plan.pit_stops.length === 1 ? "" : "s"} across laps ${payload.current_lap}-${payload.total_laps}`;
}

function renderSimulationCards(cards) {
  if (!cards || !cards.length) {
    return;
  }

  simulationGrid.innerHTML = "";

  cards.forEach((item, index) => {
    const stops = item.pit_laps.join(", ");
    const compounds = item.compounds.join("-");
    const node = document.createElement("article");
    node.className = "sim-card";
    node.innerHTML = `
      <div class="sim-card-header">
        <div>
          <div class="sim-rank">Rank ${index + 1}</div>
          <div class="sim-time">${formatTime(item.predicted_race_time_seconds)}</div>
        </div>
        <div class="sim-dots"><span></span><span></span><span></span></div>
      </div>
      <div class="sim-card-body">
        <div>
          <p class="panel-kicker">Finishing Position Distribution</p>
          <div class="dist-bars">${item.distribution.map((value, bucketIndex) => {
            const tone = bucketIndex < 3 ? "best" : bucketIndex > 11 ? "worst" : bucketIndex < 8 ? "mid" : "";
            return `<span class="${tone}" style="height:${value}%;" title="P${bucketIndex + 1}: ${value}%"></span>`;
          }).join("")}</div>
          <div class="sim-axis"><span>P1</span><span>P5</span><span>P10</span><span>P15</span><span>P20</span></div>
        </div>
        <div class="sim-metrics">
          <div class="sim-metric"><strong>P${item.p10_best}</strong><small>P10 best</small></div>
          <div class="sim-metric"><strong>P${item.p50_median}</strong><small>P50 median</small></div>
          <div class="sim-metric"><strong>P${item.p90_worst}</strong><small>P90 worst</small></div>
        </div>
        <div class="sim-footer">
          <div><span>SC During Stop</span><strong>${Math.round(item.sc_during_stop_probability * 100)}%</strong></div>
          <div><span>Win Probability</span><strong>${Math.round(item.win_probability * 100)}%</strong></div>
          <div><span>Pit Laps</span><strong>${stops || "None"}</strong></div>
          <div><span>Compounds</span><strong>${compounds || currentRaceDetail?.current_compound || "MEDIUM"}</strong></div>
        </div>
      </div>
    `;
    simulationGrid.appendChild(node);
  });
}

function renderOptimizerRankedPlans(result) {
  const plans = [result.recommended, ...result.alternatives].slice(0, 3);
  optimizerRanked.innerHTML = plans.map((plan, index) => `
    <article class="optimizer-plan-card">
      <span class="small-label">Rank ${index + 1}</span>
      <h3>${plan.plan.name}</h3>
      <div class="spec-list">
        <div class="spec-row"><span>Race Time</span><strong>${formatTime(plan.expected_race_time_seconds)}</strong></div>
        <div class="spec-row"><span>Confidence</span><strong>${Math.round(plan.confidence * 100)}%</strong></div>
        <div class="spec-row"><span>Pit Stops</span><strong>${plan.plan.pit_stops.length}</strong></div>
        <div class="spec-row"><span>Stints</span><strong>${plan.plan.pit_stops.map((stop) => stop.new_compound).join("-") || "Stay out"}</strong></div>
      </div>
    </article>
  `).join("");
}

function renderCompoundTags(container, pitLaps, compounds) {
  const tags = compounds.map((compound, index) => {
    const lap = pitLaps[index];
    return `<span class="pit-tag ${compoundClasses[compound] || "hard"}">L${lap} ${compound}</span>`;
  }).join("");
  container.innerHTML = tags || '<span class="pit-tag hard">No stop</span>';
}

function renderRaceEngineer(result) {
  engineerPushLap.textContent = `${result.predicted_push_lap_time_seconds.toFixed(3)}s`;
  engineerHeadline.textContent = `${result.primary.strategy_name} is the leading call, with ${result.fallback.strategy_name} prepared as the fallback scenario.`;
  engineerDriverHero.textContent = describeDriver(result.driver_code);
  engineerConfidence.textContent = `${Math.round(result.confidence * 100)}%`;
  engineerPrimaryTrigger.textContent = result.primary.trigger;
  engineerFallbackTrigger.textContent = result.fallback.trigger;
  engineerPrimaryName.textContent = result.primary.strategy_name;
  engineerPrimaryTime.textContent = formatTime(result.primary.expected_race_time_seconds);
  engineerFallbackName.textContent = result.fallback.strategy_name;
  engineerFallbackTime.textContent = formatTime(result.fallback.expected_race_time_seconds);
  renderCompoundTags(engineerPrimaryTags, result.primary.pit_laps, result.primary.compounds);
  renderCompoundTags(engineerFallbackTags, result.fallback.pit_laps, result.fallback.compounds);
  engineerAssumptions.innerHTML = result.assumptions.map((item) => `<li>${item}</li>`).join("");
  engineerCallouts.innerHTML = result.lap_by_lap_callouts.map((item) => `<li>${item}</li>`).join("");
  engineerSensitivities.innerHTML = result.sensitivities.map((item) => `
    <article class="sensitivity-card">
      <span class="small-label">${item.factor}</span>
      <strong>${item.level}</strong>
      <p>${item.effect}</p>
    </article>
  `).join("");
}

function renderScenarioComparison(result) {
  scenarioCompareGrid.innerHTML = result.scenarios.map((item) => `
    <article class="scenario-card">
      <span class="small-label">${item.title}</span>
      <strong>${item.strategy_name}</strong>
      <p>${item.trigger}</p>
      <div class="spec-list">
        <div class="spec-row"><span>Race Time</span><strong>${formatTime(item.expected_race_time_seconds)}</strong></div>
        <div class="spec-row"><span>Win Probability</span><strong>${Math.round(item.win_probability * 100)}%</strong></div>
        <div class="spec-row"><span>Confidence</span><strong>${Math.round(item.confidence * 100)}%</strong></div>
        <div class="spec-row"><span>Risk</span><strong>${item.risk_level}</strong></div>
      </div>
      <div class="tag-stack">
        ${item.compounds.map((compound, index) => `<span class="pit-tag ${compoundClasses[compound] || "hard"}">L${item.pit_laps[index]} ${compound}</span>`).join("")}
      </div>
      <p class="recommendation-copy">${item.summary}</p>
    </article>
  `).join("");
}

function renderModelLab(result) {
  modelLabGeneratedAt.textContent = `Generated ${new Date(result.generated_at).toLocaleString()}`;
  modelLabCards.innerHTML = result.models.map((model) => `
    <article class="model-card">
      <div class="panel-title-row">
        <p class="panel-kicker">${model.title}</p>
        <span class="status-dot">${model.algorithm} • ${model.version}</span>
      </div>
      <div class="spec-list">
        <div class="spec-row"><span>Target</span><strong>${model.target}</strong></div>
        <div class="spec-row"><span>Samples</span><strong>${model.sample_count}</strong></div>
        <div class="spec-row"><span>MAE</span><strong>${model.mae}</strong></div>
        <div class="spec-row"><span>RMSE</span><strong>${model.rmse}</strong></div>
        <div class="spec-row"><span>R2</span><strong>${model.r2}</strong></div>
      </div>
      <div class="feature-list">
        ${model.feature_importance.slice(0, 6).map((item) => `<div class="feature-chip">${item.feature}: ${item.importance}</div>`).join("")}
      </div>
    </article>
  `).join("");
  modelLabCalibration.innerHTML = result.calibration.map((item) => {
    const delta = Math.abs(item.predicted_mean - item.actual_mean);
    const height = Math.max(18, Math.min(110, delta * 24 + 18));
    return `
      <article class="calibration-card">
        <span class="small-label">${item.label}</span>
        <div class="calibration-bars">
          <div>
            <span>Predicted</span>
            <div class="calibration-bar predicted" style="height:${height}px"></div>
            <strong>${item.predicted_mean.toFixed(2)}</strong>
          </div>
          <div>
            <span>Actual</span>
            <div class="calibration-bar actual" style="height:${Math.max(18, Math.min(110, item.actual_mean * 0.9))}px"></div>
            <strong>${item.actual_mean.toFixed(2)}</strong>
          </div>
        </div>
        <p>${item.count} samples</p>
      </article>
    `;
  }).join("");
  modelLabBacktestBody.innerHTML = result.backtest.map((row) => `
    <tr>
      <td>${row.season}</td>
      <td>${row.grand_prix}</td>
      <td>${row.driver_code}</td>
      <td>${row.actual_lap_time_seconds.toFixed(3)}s</td>
      <td>${row.predicted_lap_time_seconds.toFixed(3)}s</td>
      <td>${row.absolute_error_seconds.toFixed(3)}s</td>
      <td>${row.actual_pit_stops.toFixed(1)} / ${row.predicted_pit_stops.toFixed(1)}</td>
    </tr>
  `).join("");
  modelLabBacktestBody.insertAdjacentHTML("afterbegin", result.backtest_summary.map((item) => `
    <tr class="summary-row">
      <td colspan="2">${item.label}</td>
      <td colspan="2"><strong>${item.value}</strong></td>
      <td colspan="3">${item.description}</td>
    </tr>
  `).join(""));
  modelLabBacktestBody.insertAdjacentHTML("afterbegin", result.summary.map((item) => `
    <tr class="summary-row">
      <td colspan="7">${item}</td>
    </tr>
  `).join(""));
}

function renderDegradation(payload) {
  const chart = document.getElementById("degradation-chart");
  const grid = chart.querySelector(".grid");
  const lines = chart.querySelector(".lines");
  const markers = chart.querySelector(".markers");

  grid.innerHTML = "";
  lines.innerHTML = "";
  markers.innerHTML = "";

  const chartWidth = 640;
  const chartHeight = 260;
  const padding = { top: 28, right: 20, bottom: 32, left: 52 };
  const innerWidth = chartWidth - padding.left - padding.right;
  const innerHeight = chartHeight - padding.top - padding.bottom;
  const maxLaps = 32;
  const maxTime = payload.base_lap_time_seconds + maxLaps * (payload.degradation_per_lap + 0.12) + 1.6;
  const minTime = payload.base_lap_time_seconds - 1.4;

  function xScale(lap) {
    return padding.left + (lap / maxLaps) * innerWidth;
  }

  function yScale(time) {
    return padding.top + ((maxTime - time) / (maxTime - minTime)) * innerHeight;
  }

  for (let i = 0; i <= 4; i += 1) {
    const y = padding.top + (innerHeight / 4) * i;
    const labelValue = (maxTime - ((maxTime - minTime) / 4) * i).toFixed(1);
    grid.insertAdjacentHTML("beforeend", `<line x1="${padding.left}" y1="${y}" x2="${chartWidth - padding.right}" y2="${y}"></line><text x="${padding.left - 38}" y="${y + 4}">${labelValue}s</text>`);
  }

  for (let i = 0; i <= 4; i += 1) {
    const lap = (maxLaps / 4) * i;
    const x = xScale(lap);
    grid.insertAdjacentHTML("beforeend", `<line x1="${x}" y1="${padding.top}" x2="${x}" y2="${chartHeight - padding.bottom}"></line><text x="${x - 8}" y="${chartHeight - 10}">${Math.round(lap)}</text>`);
  }

  const compounds = [
    { name: "HARD", color: "#f4f5f7", offset: 1.1, slope: payload.degradation_per_lap * 0.78, model: "Quadratic + fuel", cliff: 38, samples: 284 },
    { name: "MEDIUM", color: "#ffd60a", offset: 0.6, slope: payload.degradation_per_lap, model: "Quadratic + fuel", cliff: 25, samples: 321 },
    { name: "SOFT", color: "#ff1037", offset: 0.0, slope: payload.degradation_per_lap * 1.35, model: "Aggressive thermal", cliff: 18, samples: 244 },
  ];

  compounds.forEach((compound) => {
    const path = [];
    for (let lap = 0; lap <= maxLaps; lap += 1) {
      const time = payload.base_lap_time_seconds + compound.offset + lap * compound.slope;
      path.push(`${lap === 0 ? "M" : "L"} ${xScale(lap)} ${yScale(time)}`);
    }
    lines.insertAdjacentHTML("beforeend", `<path d="${path.join(" ")}" fill="none" stroke="${compound.color}" stroke-width="3.5" stroke-linecap="round"></path>`);
  });

  const selected = compounds.find((item) => item.name === payload.current_compound);
  const markerLap = Math.min(28, Math.max(6, payload.tire_age_laps));
  const markerTime = payload.base_lap_time_seconds + selected.offset + markerLap * selected.slope;
  const markerX = xScale(markerLap);
  const markerY = yScale(markerTime);
  const labelWidth = 108;
  const labelHeight = 24;
  const labelX = Math.min(chartWidth - padding.right - labelWidth, markerX + 14);
  const labelY = Math.max(padding.top + 6, markerY - 28);
  markers.insertAdjacentHTML(
    "beforeend",
    `
      <circle cx="${markerX}" cy="${markerY}" r="5.5" fill="${selected.color}" stroke="#0b0d12" stroke-width="3"></circle>
      <rect x="${labelX}" y="${labelY}" rx="12" ry="12" width="${labelWidth}" height="${labelHeight}" fill="rgba(9, 11, 16, 0.92)" stroke="${selected.color}" stroke-width="1.5"></rect>
      <text x="${labelX + 12}" y="${labelY + 15}" fill="#f5f6f8" font-size="11.5" font-family="'JetBrains Mono', monospace" font-weight="700">Current stint</text>
    `,
  );

  degradationNote.textContent = `${payload.current_compound} is the selected current compound with ${payload.tire_age_laps} laps already completed on the tyre.`;
  degradationBias.textContent = currentRaceDetail ? currentRaceDetail.strategy_bias : "Heuristic Model";

  degradationSpecs.innerHTML = compounds.map((compound) => `
    <article class="spec-card">
      <h3 style="color:${compound.color}">${compound.name}</h3>
      <div class="spec-list">
        <div class="spec-row"><span>Model Type</span><strong>${compound.model}</strong></div>
        <div class="spec-row"><span>a (quadratic)</span><strong>${(compound.slope * 2).toFixed(3)}</strong></div>
        <div class="spec-row"><span>b (linear)</span><strong>${(compound.slope * 1000).toFixed(1)} ms/lap</strong></div>
        <div class="spec-row"><span>Cliff Lap</span><strong>Lap ${compound.cliff}</strong></div>
        <div class="spec-row"><span>Samples</span><strong>${compound.samples}</strong></div>
      </div>
    </article>
  `).join("");
}

function renderArchiveTable() {
  const season = archiveSeasonFilter.value || "All";
  const circuit = archiveCircuitFilter.value || "All";
  const query = (archiveSearch.value || "").toLowerCase().trim();

  const rows = catalog.races.filter((race) => {
    const seasonMatch = season === "All" || String(race.season) === season;
    const circuitMatch = circuit === "All" || race.circuit === circuit;
    const searchMatch = !query || `${race.grand_prix} ${race.circuit} ${race.country}`.toLowerCase().includes(query);
    return seasonMatch && circuitMatch && searchMatch;
  });

  archiveCount.textContent = rows.length;
  archiveTableBody.innerHTML = "";

  rows.forEach((race) => {
    const tr = document.createElement("tr");
    tr.className = race.race_id === selectedArchiveRaceId ? "active" : "";
    tr.innerHTML = `<td>${race.season}</td><td>${race.round}</td><td>${race.grand_prix}</td><td>${race.circuit}</td><td>${race.country}</td>`;
    tr.addEventListener("click", async () => {
      selectedArchiveRaceId = race.race_id;
      const detail = await fetchJson(`/api/races/${race.race_id}`);
      renderArchiveDetail(detail);
      renderArchiveTable();
    });
    archiveTableBody.appendChild(tr);
  });
}

function renderArchiveDetail(detail) {
  archiveDetail.innerHTML = `
    <h3>${detail.season} ${detail.grand_prix}</h3>
    <p class="recommendation-copy">${detail.archive_note}</p>
    <div class="archive-detail-grid">
      <div class="detail-box"><span>Circuit</span><strong>${detail.circuit}</strong></div>
      <div class="detail-box"><span>Country</span><strong>${detail.country}</strong></div>
      <div class="detail-box"><span>Laps</span><strong>${detail.laps}</strong></div>
      <div class="detail-box"><span>Strategy Bias</span><strong>${detail.strategy_bias}</strong></div>
      <div class="detail-box"><span>Pit Loss</span><strong>${detail.pit_loss_seconds}s</strong></div>
      <div class="detail-box"><span>Overtaking</span><strong>${detail.overtake_difficulty}</strong></div>
      <div class="detail-box"><span>Safety Car Risk</span><strong>${Math.round(detail.safety_car_probability * 100)}%</strong></div>
      <div class="detail-box"><span>Weather Risk</span><strong>${detail.weather_risk}</strong></div>
    </div>
  `;
}

function populateArchiveFilters() {
  archiveSeasonFilter.innerHTML = ['<option value="All">All</option>', ...catalog.seasons.map((season) => `<option value="${season}">${season}</option>`)].join("");
  archiveCircuitFilter.innerHTML = ['<option value="All">All</option>', ...catalog.circuits.map((circuit) => `<option value="${circuit}">${circuit}</option>`)].join("");
}

function applyRaceDetail(detail) {
  currentRaceDetail = detail;
  selectedArchiveRaceId = detail.race_id;
  seasonTag.textContent = `${detail.season} ${detail.grand_prix}`;
  pitstopTitle.textContent = `${detail.circuit} Pit Stops`;
  pitstopSubtitle.textContent = `${detail.season} ${detail.grand_prix} • ${detail.country} • ${detail.laps} laps`;
  renderPitstopBoard();
  renderArchiveDetail(detail);
  renderArchiveTable();
  renderContextGuide();

  form.total_laps.value = detail.laps;
  form.current_lap.value = Math.min(18, detail.laps - 8);
  form.current_compound.value = detail.current_compound;
  form.tire_age_laps.value = detail.tire_age_laps;
  form.pit_loss_seconds.value = detail.pit_loss_seconds;
  form.base_lap_time_seconds.value = detail.base_lap_time_seconds;
  form.fuel_penalty_per_lap.value = detail.fuel_penalty_per_lap;
  form.safety_car_probability.value = detail.safety_car_probability;
  form.degradation_per_lap.value = detail.degradation_per_lap;
  form.compound_delta_seconds.value = detail.compound_delta_seconds;
  scProbability.textContent = `${Math.round(detail.safety_car_probability * 100)}%`;

  if (currentDrivers.length) {
    const preferredDriver = currentDrivers.find((driver) => detail.drivers.includes(driver.code)) || currentDrivers[0];
    simDriver.value = preferredDriver.code;
    optimizerDriver.value = preferredDriver.code;
    engineerDriver.value = preferredDriver.code;
    if (liveDriver) {
      liveDriver.value = preferredDriver.code;
    }
  }
  gridPosition.value = Math.min(20, 3 + detail.round);
  gridPositionLabel.textContent = `P${gridPosition.value}`;
  engineerGridPosition.value = gridPosition.value;
  engineerScWindowStart.value = Math.min(detail.laps - 8, 18);
  engineerScWindowEnd.value = Math.min(detail.laps - 2, 24);
}

function renderResult(payload, result) {
  const previousPayload = latestPayload;
  const previousResult = latestResult;
  latestResult = result;
  latestPayload = payload;
  summaryTime.textContent = formatTime(result.recommended.expected_race_time_seconds);
  summaryConfidence.textContent = `${Math.round(result.recommended.confidence * 100)}%`;
  summaryStops.textContent = String(result.recommended.plan.pit_stops.length);
  recommendedName.textContent = result.recommended.plan.name;
  recommendedExplanation.textContent = result.recommended.explanation;
  heroDriver.textContent = describeDriver(result.driver_code || payload.driver_code);
  heroWinProbability.textContent = `${Math.round(result.win_probability * 100)}%`;
  heroImprovement.textContent = `-${result.improvement_seconds.toFixed(2)}s`;
  heroRiskLevel.textContent = result.risk_level;
  baselineName.textContent = result.baseline.plan.name;
  baselineTime.textContent = formatTime(result.baseline.expected_race_time_seconds);
  optimizedTime.textContent = formatTime(result.recommended.expected_race_time_seconds);
  optimizedDelta.textContent = `${result.improvement_seconds.toFixed(2)}s faster than baseline`;
  updateChangeBanner(previousPayload, previousResult, payload, result);
  renderOptimizerRankedPlans(result);
  renderPitStops(result.recommended.plan.pit_stops);
  renderTimeline(payload, result.recommended.plan);
  renderDegradation(payload);
  markResultsUpdated();
}

async function runOptimizer(event) {
  if (event) {
    event.preventDefault();
  }

  setLoading(true, "Computing");

  let timeoutId;
  try {
    const payload = buildPayload();
    const controller = new AbortController();
    timeoutId = window.setTimeout(() => controller.abort(), 8000);
    const response = await fetch("/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error("Optimizer request failed");
    }

    const result = await response.json();
    renderResult(payload, result);
  } catch (error) {
    console.error("Optimizer failed:", error);
    recommendedName.textContent = "Optimization failed";
    recommendedExplanation.textContent = "The optimizer request failed or timed out. Results were not returned for this configuration.";
    heroDriver.textContent = "--";
    heroWinProbability.textContent = "--";
    heroImprovement.textContent = "--";
    heroRiskLevel.textContent = "--";
    summaryTime.textContent = "--";
    summaryConfidence.textContent = "--";
    summaryStops.textContent = "--";
    baselineName.textContent = "--";
    baselineTime.textContent = "--";
    optimizedTime.textContent = "--";
    optimizedDelta.textContent = "--";
    changeHeadline.textContent = "Optimizer request failed";
    changeDriverChip.textContent = "Driver delta unavailable";
    changeTimeChip.textContent = "Race time delta unavailable";
    changePlanChip.textContent = "Plan delta unavailable";
    pitStopTags.innerHTML = "";
    timelineTrack.innerHTML = "";
    timelineCaption.textContent = "No plan loaded";
    optimizerRanked.innerHTML = "";
  } finally {
    if (timeoutId) {
      window.clearTimeout(timeoutId);
    }
    setLoading(false);
  }
}

async function runSimulation() {
  if (!latestResult) {
    await runOptimizer();
  }

  const selectedDriver = simDriver.value || optimizerDriver.value;
  const raceState = buildPayload();
  raceState.driver_code = selectedDriver;
  simulationStatus.textContent = "Running Monte Carlo simulation...";
  simulationStatus.className = "panel simulation-status status-running";
  runSimulationButton.disabled = true;
  simulationGrid.innerHTML = "";

  try {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 10000);
    const payload = {
      race_state: raceState,
      driver_code: selectedDriver,
      simulation_count: Number(simCount.value),
      grid_position: Number(gridPosition.value),
    };
    const response = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    window.clearTimeout(timeoutId);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Simulation request failed");
    }
    const result = await response.json();
    renderSimulationCards(result.cards);
    simulationStatus.className = "panel simulation-status status-success";
    simulationStatus.textContent = `${result.simulation_count.toLocaleString()} simulations completed for ${result.driver_code}. Ranked outcomes are shown below.`;
  } catch (error) {
    console.error("Simulation failed:", error);
    simulationStatus.className = "panel simulation-status status-error";
    simulationStatus.textContent = `Simulation failed: ${error.message || "Please retry with the selected race context."}`;
  } finally {
    runSimulationButton.disabled = false;
  }
}

async function runRaceEngineer() {
  if (!currentRaceDetail) {
    raceEngineerStatus.className = "panel simulation-status status-error";
    raceEngineerStatus.textContent = "Race data is not loaded yet. Select a race first.";
    return;
  }

  runRaceEngineerButton.disabled = true;
  engineerHeadline.textContent = "Running race engineer analysis...";
  raceEngineerStatus.className = "panel simulation-status status-running";
  raceEngineerStatus.textContent = "Running primary, fallback, and scenario comparison analysis...";

  try {
    const payload = {
      race_id: currentRaceDetail.race_id,
      driver_code: engineerDriver.value || optimizerDriver.value,
      grid_position: Number(engineerGridPosition.value),
      gap_ahead_seconds: Number(engineerGapAhead.value),
      gap_behind_seconds: Number(engineerGapBehind.value),
      weather_risk: Number(engineerWeatherRisk.value),
      traffic_risk: Number(engineerTrafficRisk.value),
      safety_car_window_start: Number(engineerScWindowStart.value),
      safety_car_window_end: Number(engineerScWindowEnd.value),
      race_state: {
        ...buildPayload(),
        driver_code: engineerDriver.value || optimizerDriver.value,
      },
    };
    const response = await fetch("/race-engineer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error("Race Engineer request failed");
    }
    const result = await response.json();
    renderRaceEngineer(result);
    const compareResponse = await fetch("/race-engineer/scenarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!compareResponse.ok) {
      throw new Error("Scenario comparison request failed");
    }
    const compareResult = await compareResponse.json();
    renderScenarioComparison(compareResult);
    raceEngineerStatus.className = "panel simulation-status status-success";
    raceEngineerStatus.textContent = `Race Engineer updated for ${result.driver_code}. Primary and fallback plans are ready.`;
  } catch (error) {
    console.error("Race engineer failed:", error);
    engineerHeadline.textContent = "Race engineer analysis failed for this configuration.";
    scenarioCompareGrid.innerHTML = "";
    raceEngineerStatus.className = "panel simulation-status status-error";
    raceEngineerStatus.textContent = `Race Engineer failed: ${error.message || "Unable to generate recommendations."}`;
  } finally {
    runRaceEngineerButton.disabled = false;
  }
}

async function loadModelLab(force = false) {
  if (modelLabLoaded && !force) {
    modelLabStatus.className = "panel simulation-status status-success";
    modelLabStatus.textContent = "Model Lab is already loaded. Click Run Model Lab again to refresh.";
    return;
  }
  runModelLabButton.disabled = true;
  modelLabStatus.className = "panel simulation-status status-running";
  modelLabStatus.textContent = "Training summaries, calibration bins, and backtesting are loading...";
  try {
    const result = await fetchJson("/api/model-lab", 15000);
    renderModelLab(result);
    modelLabLoaded = true;
    modelLabStatus.className = "panel simulation-status status-success";
    modelLabStatus.textContent = "Model Lab loaded. Metrics and backtesting are ready below.";
  } catch (error) {
    console.error("Model lab failed:", error);
    modelLabStatus.className = "panel simulation-status status-error";
    modelLabStatus.textContent = `Model Lab failed: ${error.message || "Unable to load evaluation outputs."}`;
  } finally {
    runModelLabButton.disabled = false;
  }
}

async function loadRaceDetail(raceId) {
  const detail = await fetchJson(`/api/races/${raceId}`);
  globalRace.value = raceId;
  globalCircuit.value = raceId;
  applyRaceDetail(detail);
  await runOptimizer();
  await runRaceEngineer();
}

function syncGlobalSelectorsFromRaceId(raceId) {
  globalRace.value = raceId;
  globalCircuit.value = raceId;
}

async function initializeCatalog() {
  const [catalogResponse, driversResponse, platformResponse] = await Promise.all([
    fetchJson("/api/catalog"),
    fetchJson("/api/drivers/current"),
    fetchJson("/api/platform"),
  ]);
  catalog = catalogResponse;
  currentDrivers = driversResponse;
  platformSummary = platformResponse;
  globalSeason.value = String(catalog.seasons[catalog.seasons.length - 1]);
  populateGlobalSelectors();
  populateArchiveFilters();
  populateDriverDropdowns();
  renderContextGuide();
  if (liveRaceStatus) {
    liveRaceStatus.textContent = `Platform ready: ${platformSummary.engine} warehouse mode with ${platformSummary.live_provider} provider.`;
  }
  if (liveStatusChip) {
    liveStatusChip.textContent = platformSummary.engine === "duckdb" ? "DuckDB" : "Fallback";
  }
  if (liveProviderName) {
    liveProviderName.value = platformSummary.live_provider;
  }
  await loadRaceDetail(globalRace.value);
  await runRaceEngineer();
}

navPills.forEach((pill) => pill.addEventListener("click", async () => {
  setActiveView(pill.dataset.tab);
  if (pill.dataset.tab === "modellab") {
    modelLabStatus.className = "panel simulation-status";
    modelLabStatus.textContent = modelLabLoaded
      ? "Model Lab is loaded. Click Run Model Lab to refresh."
      : "Click Run Model Lab to load training metrics, calibration, and backtesting.";
  }
}));

compoundPills.forEach((pill) => {
  pill.addEventListener("click", () => {
    compoundPills.forEach((item) => item.classList.remove("active"));
    pill.classList.add("active");
    currentCompoundFilter = pill.dataset.filter;
    renderPitstopBoard();
  });
});

globalSeason.addEventListener("change", async () => {
  populateGlobalSelectors();
  await loadRaceDetail(globalRace.value);
});

globalRace.addEventListener("change", async () => {
  syncGlobalSelectorsFromRaceId(globalRace.value);
  await loadRaceDetail(globalRace.value);
});

globalCircuit.addEventListener("change", async () => {
  syncGlobalSelectorsFromRaceId(globalCircuit.value);
  await loadRaceDetail(globalCircuit.value);
});

form.addEventListener("submit", runOptimizer);
form.querySelector('[name="safety_car_probability"]').addEventListener("input", (event) => {
  scProbability.textContent = `${Math.round(Number(event.target.value) * 100)}%`;
});

simCount.addEventListener("input", () => {
  simCountLabel.textContent = Number(simCount.value).toLocaleString();
});

gridPosition.addEventListener("input", () => {
  gridPositionLabel.textContent = `P${gridPosition.value}`;
});

archiveSeasonFilter.addEventListener("change", renderArchiveTable);
archiveCircuitFilter.addEventListener("change", renderArchiveTable);
archiveSearch.addEventListener("input", renderArchiveTable);
engineerWeatherRisk.addEventListener("input", () => {
  engineerWeatherLabel.textContent = `${Math.round(Number(engineerWeatherRisk.value) * 100)}%`;
});
engineerTrafficRisk.addEventListener("input", () => {
  engineerTrafficLabel.textContent = `${Math.round(Number(engineerTrafficRisk.value) * 100)}%`;
});

initializeCatalog().catch(() => {
  recommendedName.textContent = "Initialization failed";
  recommendedExplanation.textContent = "The dashboard could not load the historical race catalog from the backend.";
  renderContextGuide();
});

runSimulationButton.addEventListener("click", runSimulation);
runRaceEngineerButton.addEventListener("click", runRaceEngineer);
runModelLabButton.addEventListener("click", () => loadModelLab(true));
if (liveSampleSize) {
  liveSampleSize.addEventListener("input", () => {
    liveSampleSizeLabel.textContent = `${liveSampleSize.value} snapshots`;
  });
}
if (startLiveRaceButton) {
  startLiveRaceButton.addEventListener("click", startLiveRaceFeed);
}
setActiveView(getInitialViewName());
