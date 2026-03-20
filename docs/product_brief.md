# Product Brief

## Product

F1 Race Strategy Optimization Engine

## Problem

Race strategy depends on uncertain, fast-moving conditions:

- tire degradation is nonlinear
- pit stops trade track position for clean air
- safety cars reshape the optimal plan instantly
- traffic can destroy a nominally faster strategy

Teams solve this with simulation, analyst judgment, and historical pattern recognition. The MVP recreates that workflow in a focused, software-first way.

## Core User

- motorsport strategy analyst
- race engineer
- performance engineer
- serious motorsport data science team

## MVP Goal

Recommend the best strategy from the current race state for the next decision window, while making the tradeoffs visible.

## Primary User Story

As a strategy engineer, I want to input the current race state and receive ranked strategy options with projected finishing impact so I can choose the best pit and tire plan.

## Inputs

- current lap
- total laps
- current compound
- tire age
- fuel effect estimate
- pit loss estimate
- degradation profile
- opponent positions and pit status
- safety-car probability assumptions

## Outputs

- recommended strategy
- ranked alternatives
- expected race time
- expected position delta
- sensitivity under neutralization scenarios
- textual explanation

## Success Metrics

- strategy recommendation returned in under 2 seconds for MVP-scale scenarios
- optimizer evaluates at least 50 candidate strategies per request
- recommendation includes a confidence band and assumptions
- model interfaces support historical calibration later without API redesign

