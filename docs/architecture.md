# Architecture

## Overview

The MVP uses a layered architecture so we can improve simulation fidelity and ML quality independently.

```text
Client/API Request
    ->
Strategy Service
    ->
Strategy Optimizer
    ->
Race Simulator + ML Predictors
    ->
Ranked Strategy Response
```

## Core Modules

### `domain`

Typed data models:

- race state
- tire compounds
- pit events
- strategy plans
- simulation results

### `optimizer`

Searches legal strategies and scores them.

- candidate generation
- race-time estimation
- Monte Carlo evaluation
- ranking and confidence estimation

### `ml`

Contains prediction interfaces.

- lap time predictor
- tire degradation predictor
- safety car predictor

The MVP includes baseline heuristic models and clear hooks for trained replacements.

### `services`

Coordinates request handling, optimizer execution, and response formatting.

### `api`

FastAPI endpoints for health and optimization requests.

## Why This Is F1-Level In Spirit

The system mirrors the structure used in professional race strategy stacks:

- simulation-driven decision making
- uncertainty-aware evaluation
- modular predictive models
- explainability for race-wall decisions

It is not full F1 telemetry software yet, but it is pointed in the right direction technically.

## Future Extensions

- live telemetry ingestion
- reinforcement learning policy search
- game-theoretic opponent modeling
- weather model integration
- differentiable simulation for parameter tuning

