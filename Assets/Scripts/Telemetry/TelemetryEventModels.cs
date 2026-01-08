using System;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    [Serializable]
    public class TelemetryEnvelope
    {
        public string @event;
        public long ts_ms;
        public string session_id;
        public string payload_json;
        // We store payload as JSON string to avoid JsonUtility limitations with nested objects.
        // Analyzer can parse payload_json as JSON.
    }

    public static class TelemetryTime
    {
        public static long NowMs()
        {
            // Unix epoch ms
            var dt = DateTimeOffset.UtcNow;
            return dt.ToUnixTimeMilliseconds();
        }
    }
}
