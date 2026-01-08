"""Telemetry sandbox analyzer demo."""

import argparse
import json
import os


def build_out_path(inp_path: str) -> str:
    inp_dir = os.path.dirname(inp_path)
    base = os.path.basename(inp_path)

    session_id = "session"
    if base.startswith("telemetry_") and base.endswith(".jsonl"):
        session_id = base[len("telemetry_") : -len(".jsonl")]

    return os.path.join(inp_dir, f"report_{session_id}.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze telemetry sandbox data.")
    parser.add_argument("--inp", "--input", dest="inp", required=True)
    parser.add_argument("--write_json", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.write_json:
        out_path = build_out_path(args.inp)
        with open(out_path, "w", encoding="utf-8") as output_file:
            json.dump({"input": args.inp}, output_file, indent=2)


if __name__ == "__main__":
    main()
