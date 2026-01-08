using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    public class DemoTelemetryDriver : MonoBehaviour
    {
        public TelemetryEmitter emitter;

        private float _t;
        private float _tickInterval = 0.25f; // 250ms

        void Start()
        {
            if (!emitter) emitter = GetComponent<TelemetryEmitter>();
            if (!emitter) Debug.LogError("[DemoTelemetryDriver] TelemetryEmitter missing.");
        }

        void Update()
        {
            if (!emitter) return;

            _t += Time.deltaTime;
            if (_t >= _tickInterval)
            {
                _t = 0f;

                // Example W tick
                float gain = Mathf.Clamp01(Random.Range(0.4f, 0.95f));
                float cost = Mathf.Clamp01(Random.Range(0.2f, 0.9f));
                float W = gain - cost;

                string state = (W >= 0.1f) ? "STABLE" : (W >= 0f ? "CRITICAL" : "PRUNE_RISK");

                emitter.Emit("W_EVALUATION_TICK",
                    $"{{\"gain\":{gain:F3},\"cost\":{cost:F3},\"lambda\":1.0,\"W_value\":{W:F3},\"state\":\"{state}\"}}"
                );

                // Example CCS sample
                float precision = Mathf.Clamp01(Random.Range(0.45f, 0.9f));
                float shockwave = Random.Range(0.55f, 1.2f);
                string band = (shockwave > 1.0f) ? "SUPERSONIC" : "SUBSONIC";

                emitter.Emit("CCS_PRECISION_SAMPLE",
                    $"{{\"precision_index\":{precision:F3},\"shockwave_radius\":{shockwave:F3},\"speed_band\":\"{band}\"}}"
                );
            }
        }
    }
}
