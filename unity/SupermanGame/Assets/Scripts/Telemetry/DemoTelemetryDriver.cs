using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    /// <summary>
    /// Simple Play Mode driver that emits representative telemetry every 250ms.
    /// Emits: W_EVALUATION_TICK, CCS_PRECISION_SAMPLE, COST_LEDGER_APPEND
    /// </summary>
    public class DemoTelemetryDriver : MonoBehaviour
    {
        private float _accum;
        private const float TickInterval = 0.25f; // 250ms

        void Start()
        {
            Debug.Log("[DemoTelemetryDriver] Writing telemetry to: " + TelemetryEmitter.GetOutputPath());
        }

        void Update()
        {
            _accum += Time.deltaTime;
            if (_accum < TickInterval) return;
            _accum = 0f;

            // 1) W(x) tick
            float gain = Mathf.Clamp01(Random.Range(0.4f, 0.95f));
            float cost = Mathf.Clamp01(Random.Range(0.2f, 0.9f));
            float w = gain - cost;
            string state = (w >= 0.1f) ? "STABLE" : (w >= 0f ? "CRITICAL" : "PRUNE_RISK");

            TelemetryEmitter.Emit(
                "W_EVALUATION_TICK",
                $"{{\"gain\":{gain:F3},\"cost\":{cost:F3},\"lambda\":1.0,\"W_value\":{w:F3},\"state\":\"{state}\"}}"
            );

            // 2) CCS sample
            float precision = Mathf.Clamp01(Random.Range(0.45f, 0.90f));
            float shockwave = Random.Range(0.55f, 1.20f);
            string band = (shockwave > 1.0f) ? "SUPERSONIC" : "SUBSONIC";

            TelemetryEmitter.Emit(
                "CCS_PRECISION_SAMPLE",
                $"{{\"precision_index\":{precision:F3},\"shockwave_radius\":{shockwave:F3},\"speed_band\":\"{band}\"}}"
            );

            // 3) Ledger append (smoke test)
            float weight = Random.Range(0.2f, 1.0f);
            TelemetryEmitter.Emit(
                "COST_LEDGER_APPEND",
                $"{{\"source\":\"STRUCTURAL\",\"category\":\"SONIC_DEBT\",\"weight\":{weight:F3}}}"
            );
        }
    }
}
