using System;
using System.IO;
using System.Text;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public sealed class TelemetryEmitter : MonoBehaviour
    {
        private static readonly object WriteLock = new object();
        private static readonly string SessionId = Guid.NewGuid().ToString("N");

        private string _telemetryPath;

        private void Awake()
        {
            var telemetryDir = Path.Combine(Application.persistentDataPath, "ProtocolPsiTelemetry");
            Directory.CreateDirectory(telemetryDir);
            _telemetryPath = Path.Combine(telemetryDir, "telemetry_demo_01min_seed1337.jsonl");
        }

        public void Emit(string eventName, string payloadJson = null)
        {
            if (string.IsNullOrWhiteSpace(eventName))
            {
                Debug.LogWarning("TelemetryEmitter.Emit called with empty eventName.");
                return;
            }

            var line = BuildEnvelopeJsonLine(eventName, payloadJson);
            lock (WriteLock)
            {
                File.AppendAllText(_telemetryPath, line + "\n");
            }
        }

        public static string BuildEnvelopeJsonLine(string eventName, string payloadJson = null)
        {
            var tsMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var payload = string.IsNullOrWhiteSpace(payloadJson) ? "{}" : payloadJson;

            var builder = new StringBuilder(256);
            builder.Append('{');
            builder.Append("\"event\":\"").Append(EscapeJsonString(eventName)).Append("\",");
            builder.Append("\"ts_ms\":").Append(tsMs).Append(',');
            builder.Append("\"session_id\":\"").Append(EscapeJsonString(SessionId)).Append("\",");
            builder.Append("\"payload\":").Append(payload);
            builder.Append('}');

            return builder.ToString();
        }

        private static string EscapeJsonString(string value)
        {
            if (string.IsNullOrEmpty(value))
            {
                return string.Empty;
            }

            var builder = new StringBuilder(value.Length + 8);
            foreach (var ch in value)
            {
                switch (ch)
                {
                    case '\\':
                        builder.Append("\\\\");
                        break;
                    case '"':
                        builder.Append("\\\"");
                        break;
                    case '\n':
                        builder.Append("\\n");
                        break;
                    case '\r':
                        builder.Append("\\r");
                        break;
                    case '\t':
                        builder.Append("\\t");
                        break;
                    default:
                        builder.Append(ch);
                        break;
                }
            }

            return builder.ToString();
        }
    }
}
