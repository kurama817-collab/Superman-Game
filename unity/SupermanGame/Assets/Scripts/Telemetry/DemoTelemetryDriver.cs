using UnityEngine;

namespace SupermanGame.Telemetry
{
    public class DemoTelemetryDriver : MonoBehaviour
    {
        private const float EmitIntervalSeconds = 0.25f;
        private float _timeUntilNextEmit = EmitIntervalSeconds;

        private void Update()
        {
            _timeUntilNextEmit -= Time.deltaTime;
            if (_timeUntilNextEmit > 0f)
            {
                return;
            }

            _timeUntilNextEmit += EmitIntervalSeconds;

            TelemetryEmitter.Emit("W_EVALUATION_TICK");
            TelemetryEmitter.Emit("CCS_PRECISION_SAMPLE");
            TelemetryEmitter.Emit("COST_LEDGER_APPEND");
        }
    }
}
