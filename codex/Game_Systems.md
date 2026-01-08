# Game Systems Overview

## Collateral Control System (CCS)
- **Purpose:** Tracks environmental damage, civilian safety, and restoration progress.
- **Inputs:** Physics impacts, heat vision surfaces, thrown object trajectories, time-to-rescue metrics.
- **Outputs:** City health score, localized danger level, and mission consequence flags.
- **Key loops:** Damage accumulation, emergency response timers, and repair recovery ticks.

## Heroic Choice Engine (HCE)
- **Purpose:** Presents player decisions under pressure with moral and strategic consequences.
- **Inputs:** Active crisis queue, villain prompts, civilian requests, and world state thresholds.
- **Outputs:** Choice prompts, reputation modifiers, branching mission tags.
- **Key loops:** Choice generation, urgency escalation, and consequence resolution.

## Villain Philosophy Engine (VPE)
- **Purpose:** Drives antagonist behavior aligned to a philosophical archetype.
- **Inputs:** Player actions, city health, narrative timeline, villain doctrine weights.
- **Outputs:** Villain tactics, propaganda messages, and scenario mutations.
- **Key loops:** Doctrine evaluation, escalation triggers, and ideology reinforcement.
