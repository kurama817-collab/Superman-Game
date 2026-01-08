# Telemetry Sandbox

## Motivation
Provide a runnable, engine-agnostic telemetry sandbox so Protocol Ψ demo analytics can be generated and validated without Unity or Unreal dependencies.
Ensure telemetry is append-only, deterministic, and analyzable from the CLI as JSONL so analytics pipelines can be validated before integration.
Simulate the core demo systems (W(x), CCS, HCE, CCIP, Ledger) to produce representative events for downstream analytics and validation.

## Description
W(x) tick frequency: 250ms.
Add sandbox folder and output tracking with `tools/telemetry_sandbox/out/.gitkeep` and documentation in `tools/telemetry_sandbox/README.md` describing CLI usage and report locations.
Introduce `tools/telemetry_sandbox/telemetry_schema.py` defining `EventType`, `TelemetryEvent`, `now_ms()`, and `JsonlTelemetryWriter` which emits one JSON event per line.
Implement `tools/telemetry_sandbox/sandbox_run.py`, a CLI (`--minutes`, `--seed`) deterministic generator that emits `W_EVALUATION_TICK`, `CCS_PRECISION_SAMPLE`, `HCE_SIMULTANEOUS_GOODS_PRESENTED`, `HCE_FIRST_COMMITMENT_LATCHED`, `CCIP_BRANCH_DENSITY`, `CCIP_PRUNE_EXECUTED`, and `COST_LEDGER_APPEND` events to `tools/telemetry_sandbox/out/telemetry_<session>.jsonl`.
Add `tools/telemetry_sandbox/analyze_demo.py` which ingests telemetry JSONL and computes and prints W(x), CCS, Ledger, HCE, and CCIP metrics and optionally writes `tools/telemetry_sandbox/out/report_<session>.json`.

## Usage

Generate telemetry:

```bash
python3 tools/telemetry_sandbox/sandbox_run.py --minutes 1
```

Analyze telemetry:

```bash
python3 tools/telemetry_sandbox/analyze_demo.py --input tools/telemetry_sandbox/out/telemetry_<session>.jsonl
```

Reports are written to `tools/telemetry_sandbox/out/report_<session>.json` by default.
