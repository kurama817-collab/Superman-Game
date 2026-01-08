using System.Collections;
using UnityEngine;

public class DemoTelemetryDriver : MonoBehaviour
{
    [SerializeField] private float emissionIntervalSeconds = 0.25f;

    private void Start()
    {
        StartCoroutine(EmitLoop());
    }

    private IEnumerator EmitLoop()
    {
        var wait = new WaitForSeconds(emissionIntervalSeconds);
        while (true)
        {
            TelemetryEmitter.Emit("W_EVALUATION_TICK", "{\"tick\":" + Time.frameCount + "}");
            TelemetryEmitter.Emit("CCS_PRECISION_SAMPLE", "{\"precision\":" + Random.Range(0.9f, 1.0f).ToString("F3") + "}");
            TelemetryEmitter.Emit("COST_LEDGER_APPEND", "{\"cost\":" + Random.Range(0.01f, 0.2f).ToString("F4") + "}");

            yield return wait;
        }
    }
}
