# Telemetry Plan

## Goals
- Capture how players resolve crises and what trade-offs they choose.
- Measure collateral impact over time and identify friction in controls.
- Validate performance targets for the 30-minute demo.

## Event Streams
- **Player choices:** Choice prompt ID, option selected, response time, location.
- **Collateral impact:** Damage magnitude, affected district, civilian count, recovery time.
- **Combat outcomes:** Villain encounter result, time-to-neutralize, collateral score delta.
- **Traversal metrics:** Flight speed bands, altitude distribution, collision frequency.
- **Performance telemetry:** Frame time, memory usage, load times, streaming hitches.

## Metrics to Track
- Choice distribution by scenario type and urgency.
- City health deltas per encounter and per minute.
- Heat vision usage: burst length, overheat rate, collateral ignition events.
- Strength interactions: lift/throw counts, stabilization success rate.
- Average FPS and worst 1% frame times per scene.

## Storage & Review
- Store telemetry as structured JSON events with timestamps.
- Daily export to analytics dashboards for heatmaps and trend reports.
- Post-demo review checklist to highlight balance adjustments.
