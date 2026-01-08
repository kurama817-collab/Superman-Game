using System;
using System.IO;
using System.Text;
using UnityEngine;

namespace SupermanGame.Telemetry
{
    public static class TelemetryEmitter
    {
        private const string SessionId = "demo_01min_seed1337";
        private const string FileName = "telemetry_demo_01min_seed1337.jsonl";
        private const string OutputDirectoryName = "ProtocolPsiTelemetry";

        public static void Emit(string eventName, string payloadJson)
        {
            string normalizedEventName = string.IsNullOrEmpty(eventName) ? "UNKNOWN" : eventName;
            string normalizedPayload = NormalizePayload(payloadJson);
            long timestampMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

            string envelope = BuildEnvelope(normalizedEventName, timestampMs, SessionId, normalizedPayload);
            string outputPath = GetOutputPath();

            Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? Application.persistentDataPath);
            File.AppendAllText(outputPath, envelope + "\n", Encoding.UTF8);
        }

        public static string GetOutputPath()
        {
            return Path.Combine(Application.persistentDataPath, OutputDirectoryName, FileName);
        }

        private static string BuildEnvelope(string eventName, long timestampMs, string sessionId, string payloadJson)
        {
            return "{" +
                   "\"event\":\"" + JsonEscape(eventName) + "\"," +
                   "\"ts_ms\":" + timestampMs + "," +
                   "\"session_id\":\"" + JsonEscape(sessionId) + "\"," +
                   "\"payload\":" + payloadJson +
                   "}";
        }

        private static string NormalizePayload(string payloadJson)
        {
            if (string.IsNullOrWhiteSpace(payloadJson))
            {
                return "{}";
            }

            string trimmed = payloadJson.Trim();
            if (!trimmed.StartsWith("{") || !trimmed.EndsWith("}"))
            {
                return "{}";
            }

            return trimmed;
        }

        private static string JsonEscape(string value)
        {
            if (value == null)
            {
                return string.Empty;
            }

            StringBuilder builder = new StringBuilder(value.Length + 8);
            foreach (char character in value)
            {
                switch (character)
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
                        if (character < ' ')
                        {
                            builder.Append("\\u");
                            builder.Append(((int)character).ToString("x4"));
                        }
                        else
                        {
                            builder.Append(character);
                        }
                        break;
                }
            }

            return builder.ToString();
        }
    }
}
