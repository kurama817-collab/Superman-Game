# Telemetry Sandbox

This sandbox generates a deterministic JSONL stream of representative telemetry events and
includes a small analyzer for summary metrics.

## Generate telemetry

```bash
python3 tools/telemetry_sandbox/sandbox_run.py --minutes 5
```

Output path:

```
tools/telemetry_sandbox/out/telemetry_<session>.jsonl
```

## Analyze telemetry

```bash
python3 tools/telemetry_sandbox/analyze_demo.py --input <jsonl>
```

Optional JSON report:

```bash
python3 tools/telemetry_sandbox/analyze_demo.py --input <jsonl> --write_json
```
