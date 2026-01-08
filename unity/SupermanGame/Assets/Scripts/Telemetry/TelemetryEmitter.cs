using System;
using System.IO;
using System.Text;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public static class TelemetryEmitter
    {
        private const string FileName = "telemetry_demo_01min_seed1337.jsonl";
        private static readonly string SessionId = Guid.NewGuid().ToString("N");

        public static void Emit(string eventName, string payloadJson = "{}")
        {
            string directoryPath = Path.Combine(Application.persistentDataPath, "ProtocolPsiTelemetry");
            Directory.CreateDirectory(directoryPath);

            string filePath = Path.Combine(directoryPath, FileName);
            long timestampMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

            string escapedEvent = EscapeJsonString(eventName);
            string escapedSessionId = EscapeJsonString(SessionId);
            string payload = string.IsNullOrWhiteSpace(payloadJson) ? "{}" : payloadJson;

            string line = $"{{\"event\":\"{escapedEvent}\",\"ts_ms\":{timestampMs},\"session_id\":\"{escapedSessionId}\",\"payload\":{payload}}}";
            File.AppendAllText(filePath, line + "\n", Encoding.UTF8);
        }

        private static string EscapeJsonString(string value)
        {
            if (string.IsNullOrEmpty(value))
            {
                return string.Empty;
            }

            return value.Replace("\\", "\\\\").Replace("\"", "\\\"");
        }
    }
}
