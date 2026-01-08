# Telemetry Sandbox

This sandbox generates deterministic, engine-agnostic telemetry for validating Protocol Ψ demo analytics.

## Run a 5-minute sandbox

```bash
python3 tools/telemetry_sandbox/sandbox_run.py --minutes 5
```

Telemetry is written to `tools/telemetry_sandbox/out/telemetry_<session>.jsonl`.

## Analyze results

```bash
python3 tools/telemetry_sandbox/analyze_demo.py \
  --input tools/telemetry_sandbox/out/telemetry_<session>.jsonl
```

Optionally emit a JSON report:

```bash
python3 tools/telemetry_sandbox/analyze_demo.py \
  --input tools/telemetry_sandbox/out/telemetry_<session>.jsonl \
  --write-report
```

Reports are written to `tools/telemetry_sandbox/out/report_<session>.json`.

## Simulated systems

- W(x) ticks every 250 ms
- CCS precision and shockwave sampling
- HCE Impossible Splits with commit timing
- CCIP branch density and pruning
- Immutable Ledger appends including Cost-of-Absence
