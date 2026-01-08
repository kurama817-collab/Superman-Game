# Protocol Ψ Overview

## Game Systems Detail

### Collateral Control System (CCS)
**Purpose:** Measure and manage the hero’s effect on the living city instead of the hero’s health.

**Core Loop**
1. **Threat Emerges** → A crisis spawns with an initial **Collateral Risk Profile**.
2. **Player Response** → Player chooses approach, scale, and timing.
3. **World Reaction** → Systems simulate damage, panic, recovery, and reputation shifts.
4. **Ledger Update** → Persistent world state records successes, failures, and lasting scars.

**Key Components**
- **Collateral Risk Profile**
  - **Fragility Index:** how easily the environment is damaged.
  - **Population Density:** stakes for civilian harm or rescue.
  - **Critical Infrastructure Weight:** power grid, hospitals, transit nodes.
- **Control Actions**
  - **Precision:** focus and finesse of the hero’s intervention.
  - **Containment:** ability to isolate damage from spreading.
  - **Stabilization:** after-action recovery (structural repairs, crowd calming).
- **World Ledger**
  - Tracks **Scar Severity**, **Recovery Timelines**, and **Trust Shifts** per district.

**Signals to the Player**
- **City Stability Meter:** aggregated district stability and recovery pace.
- **Damage Readouts:** real-time collateral outcomes (structural damage, civilian safety).
- **Trust Delta:** public confidence moving up or down per incident.

---

### Heroic Choice Engine (HCE)
**Purpose:** Translate ethical dilemmas and opportunity costs into systemic outcomes.

**Choice Architecture**
- **Dual-Track Dilemmas:** save many vs. save a critical few.
- **Tradeoffs Over Time:** short-term heroics vs. long-term stability.
- **Reputation & Trust:** decisions shift public sentiment and institutional cooperation.

**Key Inputs**
- **Scenario Stakes:** severity, time pressure, visibility, and political sensitivity.
- **Player Capabilities:** powers available, cooldowns, and fatigue of the city itself.
- **World Context:** prior scars, community trust, and unresolved story arcs.

**Outcome Model**
- **Immediate Outcome:** success/failure, collateral, and urgency resolution.
- **Ripple Effects:** follow-up crisis probability and stakeholder response.
- **Narrative Flags:** unlock or lock future missions and alliances.

**Player Feedback**
- **After-Action Brief:** transparent report on what was saved, lost, and changed.
- **Community Pulse:** headlines, NPC reactions, and institutional support updates.

---

## Telemetry Plan (Early Scope)

### Goals
- Validate if players *feel* more responsible for the world than for themselves.
- Measure whether choices create meaningful, memorable tradeoffs.
- Track where players struggle with control vs. power.

### Event Categories
- **Incident Lifecycle**
  - `incident_spawned`, `incident_resolved`, `incident_failed`
- **Collateral Outcomes**
  - `collateral_damage_incurred`, `civilians_rescued`, `infrastructure_saved`
- **Heroic Choice Engine**
  - `choice_presented`, `choice_selected`, `choice_outcome`
- **Trust & Reputation**
  - `trust_delta_applied`, `district_trust_threshold_crossed`

### Required Context Fields
- `district_id`
- `incident_id`
- `choice_id`
- `collateral_score`
- `trust_score`
- `time_to_resolve`

### Analysis Questions
- Which choice archetypes create the strongest trust shifts?
- Do players overuse brute-force approaches when collateral risk is high?
- What is the median time-to-resolve vs. collateral in high-density zones?

---

## Demo Outline (Early Target)

### Demo Goal
Showcase **world vulnerability**, **ethical tension**, and **persistent consequences** in a 20–30 minute playable slice.

### Demo Structure
1. **Intro Incident — “Bridge Lockdown”**
   - Fast, visible stakes: stalled transit and growing crowd panic.
   - Teach containment and precision.
2. **Choice Dilemma — “Hospital Grid”**
   - Save patients with a risky quick fix, or prevent a citywide blackout.
   - Introduce trust shifts and district scars.
3. **Escalation — “High-Rise Collapse”**
   - Multiple targets, competing rescue vectors.
   - Demonstrate collateral control pressure.
4. **After-Action Briefing**
   - Show scars, reputation outcomes, and future mission shifts.

### Success Criteria
- Players can explain the **world health** concept after the demo.
- At least one choice feels **personally costly** or **ethically tense**.
- Players notice and react to **persistent environmental change**.
