# MVP Backlog

## Foundation

- [ ] define race-state and strategy-response contracts
- [ ] add synthetic race scenario fixtures
- [ ] create configurable race rules and tire definitions

## Optimization

- [ ] generate legal one-stop and two-stop strategies
- [ ] compute stint lap-time curves
- [ ] model pit-loss and out-lap penalties
- [ ] support Monte Carlo scenario rollouts
- [ ] rank strategies by expected race time and robustness

## ML

- [ ] baseline degradation regressor
- [ ] baseline lap-time predictor
- [ ] safety car probability estimator
- [ ] evaluation pipeline for calibration error

## API

- [ ] `POST /optimize`
- [ ] `GET /health`
- [ ] OpenAPI examples

## Validation

- [ ] unit tests for simulator and optimizer
- [ ] contract tests for API schema
- [ ] benchmark target under 2 seconds

