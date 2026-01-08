# System Stubs Reference

This section maps the placeholder scripts/classes to their responsibilities.

## Collateral Control System
- **File:** `src/systems/collateral_control_system.py`
- **Class:** `CollateralControlSystem`
- **Role:** Track damage events, compute city health score, and expose district summaries.

## Heroic Choice Engine
- **File:** `src/systems/heroic_choice_engine.py`
- **Class:** `HeroicChoiceEngine`
- **Role:** Build choice prompts, resolve consequences, and queue narrative tags.

## Villain Philosophy Engine
- **File:** `src/systems/villain_philosophy_engine.py`
- **Class:** `VillainPhilosophyEngine`
- **Role:** Evaluate doctrine weights and produce villain actions and messaging.

## Telemetry Client
- **File:** `src/telemetry/telemetry_client.py`
- **Class:** `TelemetryClient`
- **Role:** Record structured telemetry events and provide summary snapshots.
