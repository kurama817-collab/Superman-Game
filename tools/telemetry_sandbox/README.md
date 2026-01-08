# Protocol Ψ Telemetry Sandbox (Engine-Agnostic)

Purpose:
- Generate deterministic JSONL telemetry events for demo analytics without Unity/Unreal.
- Validate metrics pipelines (W(x), CCS, HCE, CCIP, Ledger) locally.

## Output
All runs write to:
- tools/telemetry_sandbox/out/telemetry_<session_id>.jsonl

Analyzer can write:
- tools/telemetry_sandbox/out/report_<session_id>.json

## Run a deterministic demo session
From repo root:

python tools/telemetry_sandbox/sandbox_run.py --minutes 1 --seed 1337
python tools/telemetry_sandbox/analyze_demo.py --in tools/telemetry_sandbox/out/telemetry_demo_01min_seed1337.jsonl --write_json

## Determinism Rules
- Same --minutes and --seed => byte-identical JSONL output
- Output file is overwritten each run (not appended)
- Timestamps are derived from seed (no wall-clock time)
