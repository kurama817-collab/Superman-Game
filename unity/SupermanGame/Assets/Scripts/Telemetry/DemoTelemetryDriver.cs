using System.Collections.Generic;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public class DemoTelemetryDriver : MonoBehaviour
    {
        [SerializeField] private TelemetryEmitter emitter;
        [SerializeField] private float heartbeatIntervalSeconds = 5f;

        private float nextHeartbeatTime;

        private void Start()
        {
            if (emitter == null)
            {
                emitter = FindObjectOfType<TelemetryEmitter>();
            }

            EmitBootEvent();
            ScheduleNextHeartbeat();
        }

        private void Update()
        {
            if (emitter == null)
            {
                return;
            }

            if (Time.time >= nextHeartbeatTime)
            {
                emitter.Emit("demo_heartbeat", new Dictionary<string, object>
                {
                    { "time", Time.time },
                    { "position", transform.position.ToString() }
                });

                ScheduleNextHeartbeat();
            }
        }

        private void EmitBootEvent()
        {
            if (emitter == null)
            {
                Debug.LogWarning("DemoTelemetryDriver could not find a TelemetryEmitter.");
                return;
            }

            emitter.Emit("demo_boot", new Dictionary<string, object>
            {
                { "scene", gameObject.scene.name },
                { "frame", Time.frameCount }
            });
        }

        private void ScheduleNextHeartbeat()
        {
            nextHeartbeatTime = Time.time + heartbeatIntervalSeconds;
        }
    }
}
