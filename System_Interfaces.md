# Engine-Agnostic System Interfaces (Stubs)

These interfaces are **engine-agnostic contracts** for core systems. They define expected behaviors
without prescribing implementation details or data storage. Use them as integration targets for
Unity, Unreal, or custom engines.

```csharp
public interface IProtocolPsi
{
    float EvaluateWorldSustainability(float gain, float cost);
    void RecordLedgerEvent(LedgerEvent evt);
}

public interface ICollateralControlSystem
{
    float EvaluateCollateralRisk(float projectedForce, float populationDensity);
    void RecordCollateralEvent(CollateralEvent evt);
}

public interface IHeroicChoiceEngine
{
    float EvaluateChoiceWeight(HeroicChoice choice);
    void RecordChoiceOutcome(HeroicChoiceOutcome outcome);
}

public interface ITelemetrySink
{
    void RecordTelemetryEvent(TelemetryEvent evt);
    void Flush();
}
```

> **Note:** The types shown above (e.g., `LedgerEvent`, `CollateralEvent`) are placeholders and
> may be mapped to engine-specific data structures.
