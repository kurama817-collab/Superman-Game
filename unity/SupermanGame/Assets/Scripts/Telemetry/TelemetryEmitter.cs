using System;
using System.Collections.Generic;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public class TelemetryEmitter : MonoBehaviour
    {
        public static TelemetryEmitter Instance { get; private set; }

        public event Action<string, IReadOnlyDictionary<string, object>> TelemetryEmitted;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
        }

        public void Emit(string eventName, IReadOnlyDictionary<string, object> payload)
        {
            if (string.IsNullOrWhiteSpace(eventName))
            {
                Debug.LogWarning("TelemetryEmitter received an empty event name.");
                return;
            }

            TelemetryEmitted?.Invoke(eventName, payload ?? new Dictionary<string, object>());
            Debug.Log($"[Telemetry] {eventName}");
        }
    }
}
