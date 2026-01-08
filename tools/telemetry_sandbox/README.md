# Telemetry Sandbox

This sandbox emits deterministic demo telemetry events and a companion analyzer to summarize them.

## Usage

Run the generator with deterministic session IDs based on minutes and seed:

```bash
python3 tools/telemetry_sandbox/sandbox_run.py --minutes 1 --seed 1337
```

This writes:

```
tools/telemetry_sandbox/out/telemetry_demo_01min_seed1337.jsonl
```

W(x) tick frequency: 250ms.

Analyze the output and optionally write a JSON report:

```bash
python3 tools/telemetry_sandbox/analyze_demo.py \
  --input tools/telemetry_sandbox/out/telemetry_demo_01min_seed1337.jsonl \
  --write_json
```

## Output ordering

Analyzer output is normalized for stable diffs: ledger sources and W(x) state counts are sorted,
with JSON rendered using `sort_keys=True`.
