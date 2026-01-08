using System.Collections;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public sealed class DemoTelemetryDriver : MonoBehaviour
    {
        [SerializeField]
        private TelemetryEmitter telemetryEmitter;

        private void Awake()
        {
            if (telemetryEmitter == null)
            {
                telemetryEmitter = GetComponent<TelemetryEmitter>();
            }
        }

        private void Start()
        {
            if (telemetryEmitter == null)
            {
                Debug.LogWarning("DemoTelemetryDriver requires a TelemetryEmitter reference.");
                return;
            }

            StartCoroutine(EmitLoop());
        }

        private IEnumerator EmitLoop()
        {
            var wait = new WaitForSeconds(0.25f);
            while (true)
            {
                telemetryEmitter.Emit("W_EVALUATION_TICK", "{\"tick\":1}");
                telemetryEmitter.Emit("CCS_PRECISION_SAMPLE", "{\"precision\":0.98}");
                telemetryEmitter.Emit("COST_LEDGER_APPEND", "{\"cost\":12.5}");
                yield return wait;
            }
        }
    }
}
