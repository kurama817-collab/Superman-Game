# Telemetry Sandbox (Engine-Agnostic)

This folder provides a runnable telemetry sandbox for the Protocol Ψ 30-minute demo metrics.
It emits JSONL telemetry events and generates a summary report.

## Requirements
- Python 3.10+ (works on 3.9+ in most cases)

## Run a 5-minute sandbox
From repo root:

python3 tools/telemetry_sandbox/sandbox_run.py --minutes 5

## Output locations
- Telemetry JSONL: tools/telemetry_sandbox/out/telemetry_<session>.jsonl
- Summary report: printed to stdout
- Optional JSON report: tools/telemetry_sandbox/out/report_<session>.json

## Analyze an existing run
python3 tools/telemetry_sandbox/analyze_demo.py --input tools/telemetry_sandbox/out/<file>.jsonl

## What it simulates
- W(x) ticks every 250ms
- HCE impossible splits periodically
- CCIP prune events after commitment latch
- CCS precision + shockwave samples
- Immutable Ledger append-only entries, including Cost-of-Absence
