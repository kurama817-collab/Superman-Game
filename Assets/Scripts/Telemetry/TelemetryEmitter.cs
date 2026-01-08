using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    public class TelemetryEmitter : MonoBehaviour
    {
        [Header("Session")]
        public int minutes = 5;
        public int seed = 1337;
        public string sessionOverride = ""; // optional
        public bool validateAgainstContract = true;

        [Header("Output")]
        public string outputFolderName = "ProtocolPsiTelemetry"; // under persistentDataPath

        private HashSet<string> _allowedEvents;
        private JsonlTelemetryWriter _writer;
        private string _sessionId;

        public string SessionId => _sessionId;
        public string OutputPath => _writer?.FilePath;

        void Awake()
        {
            _sessionId = string.IsNullOrWhiteSpace(sessionOverride)
                ? $"demo_{minutes:00}min_seed{seed}"
                : sessionOverride.Trim();

            if (validateAgainstContract)
                _allowedEvents = TelemetryContractLoader.LoadEventNames();
            else
                _allowedEvents = new HashSet<string>(StringComparer.Ordinal);

            string outDir = Path.Combine(Application.persistentDataPath, outputFolderName);
            string outPath = Path.Combine(outDir, $"telemetry_{_sessionId}.jsonl");

            _writer = new JsonlTelemetryWriter(outPath);

            Debug.Log($"[Telemetry] Session={_sessionId}");
            Debug.Log($"[Telemetry] Output={outPath}");
        }

        /// <summary>
        /// Emit an event in JSONL format.
        /// payloadJson should be a JSON object string, e.g. {"gain":0.5,"cost":0.2,...}
        /// </summary>
        public void Emit(string eventName, string payloadJson)
        {
            if (string.IsNullOrWhiteSpace(eventName))
                return;

            eventName = eventName.Trim();

            if (validateAgainstContract && _allowedEvents != null && _allowedEvents.Count > 0)
            {
                if (!_allowedEvents.Contains(eventName))
                {
                    Debug.LogError($"[Telemetry] Event name not in contract: {eventName}");
                    return;
                }
            }

            var env = new TelemetryEnvelope
            {
                @event = eventName,
                ts_ms = TelemetryTime.NowMs(),
                session_id = _sessionId,
                payload_json = string.IsNullOrWhiteSpace(payloadJson) ? "{}" : payloadJson
            };

            // JsonUtility can't serialize reserved keyword "event" properly, so we used @event.
            // Output uses "event" as JSON key.
            string json = JsonUtility.ToJson(env);

            // Patch keys: @event -> event, payload_json -> payload
            // We want final envelope fields: event, ts_ms, session_id, payload
            json = json.Replace("\"@event\":", "\"event\":");
            json = json.Replace("\"payload_json\":", "\"payload\":");

            _writer.AppendLine(json);
        }
    }
}
