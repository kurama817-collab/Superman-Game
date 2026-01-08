using UnityEngine;

namespace SupermanGame.Telemetry
{
    public class DemoTelemetryDriver : MonoBehaviour
    {
        private const float EmitIntervalSeconds = 0.25f;
        private float _elapsed;

        private void Start()
        {
            Debug.Log($"Telemetry output path: {TelemetryEmitter.GetOutputPath()}");
        }

        private void Update()
        {
            _elapsed += Time.deltaTime;
            if (_elapsed < EmitIntervalSeconds)
            {
                return;
            }

            _elapsed = 0f;

            TelemetryEmitter.Emit(
                "W_EVALUATION_TICK",
                "{\"tick\":" + Time.frameCount + ",\"source\":\"demo\"}"
            );

            TelemetryEmitter.Emit(
                "CCS_PRECISION_SAMPLE",
                "{\"precision\":" + Random.Range(0.8f, 1.0f).ToString("F3") + ",\"sample\":\"demo\"}"
            );

            TelemetryEmitter.Emit(
                "COST_LEDGER_APPEND",
                "{\"cost\":" + Random.Range(0.01f, 0.1f).ToString("F4") + ",\"currency\":\"demo\"}"
            );
        }
    }
}
