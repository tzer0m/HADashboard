# HADashboard

A Home Assistant custom integration that exposes service health and GitHub Actions deploy status from the [Dashboard](https://github.com/tzer0m/Dashboard) as native Home Assistant entities.

## Requirements

This integration is a client only — it does not run anything on its own. You need an instance of the [Dashboard](https://github.com/tzer0m/Dashboard) app running and reachable from your Home Assistant instance, with its `api/status` endpoint enabled and an API key configured.

## What it does

For each service configured in the dashboard, this integration creates:

- A **binary sensor** reflecting whether the service is currently online.
- A **sensor** showing the latest GitHub Actions deploy status (`passing`, `failing`, `running`, or `unknown`), for services with a deploy badge configured.

All entities update on a 60 second polling interval, matching the dashboard's own health check and badge cache intervals.

## Installation

### Via HACS (recommended)

1. In Home Assistant, go to HACS → the three-dot menu → **Custom repositories**.
2. Add `https://github.com/tzer0m/HADashboard`, category **Integration**.
3. Find **HADashboard** in HACS and install it.
4. Restart Home Assistant.

### Manual

1. Copy the `custom_components/tzer0m_dashboard` folder into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.

## Setup

1. In Home Assistant, go to **Settings → Devices & Services → Add Integration**.
2. Search for **HADashboard**.
3. Enter the base URL of your dashboard instance (e.g. `https://tzer0m.co.uk`) and the configured API key.

## License

Personal project, provided as-is.

type: custom:hadashboard-card