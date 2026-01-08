using System;
using System.IO;
using System.Text;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    /// <summary>
    /// Minimal, dependency-free JSONL telemetry emitter for local demo/testing.
    /// Append-only writes to a deterministic file path.
    /// </summary>
    public static class TelemetryEmitter
    {
        private const string OutputFolderName = "ProtocolPsiTelemetry";
        private const string OutputFileName = "telemetry_demo_01min_seed1337.jsonl";
        private const string SessionId = "demo_01min_seed1337";

        private static string _cachedPath;

        public static string GetOutputPath()
        {
            if (!string.IsNullOrEmpty(_cachedPath)) return _cachedPath;

            string dir = Path.Combine(Application.persistentDataPath, OutputFolderName);
            Directory.CreateDirectory(dir);
            _cachedPath = Path.Combine(dir, OutputFileName);
            return _cachedPath;
        }

        /// <summary>
        /// Appends one JSON envelope per line (JSONL).
        /// Envelope keys: event, ts_ms, session_id, payload
        /// payloadJson must be a JSON object string (e.g. "{}" or "{\"k\":1}").
        /// </summary>
        public static void Emit(string eventName, string payloadJson = "{}")
        {
            if (string.IsNullOrWhiteSpace(eventName)) return;

            string safeEvent = JsonEscape(eventName.Trim());
            string safeSession = JsonEscape(SessionId);

            if (string.IsNullOrWhiteSpace(payloadJson))
                payloadJson = "{}";

            // Ensure payload is an object-like string; if not, fall back.
            payloadJson = payloadJson.Trim();
            if (!payloadJson.StartsWith("{") || !payloadJson.EndsWith("}"))
                payloadJson = "{}";

            long tsMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

            // Write stable envelope with required keys:
            // {"event":"...","ts_ms":123,"session_id":"...","payload":{...}}
            string line =
                "{\"event\":\"" + safeEvent +
                "\",\"ts_ms\":" + tsMs +
                ",\"session_id\":\"" + safeSession +
                "\",\"payload\":" + payloadJson +
                "}";

            string path = GetOutputPath();
            File.AppendAllText(path, line + "\n", Encoding.UTF8);
        }

        /// <summary>
        /// Minimal JSON string escape for event/session_id values.
        /// </summary>
        private static string JsonEscape(string s)
        {
            if (s == null) return "";
            return s
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t");
        }
    }
}
