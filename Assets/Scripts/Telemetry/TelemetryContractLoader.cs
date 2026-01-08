using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    public static class TelemetryContractLoader
    {
        public const string ContractRelativePath = "telemetry/telemetry_events_v1.json";

        public static HashSet<string> LoadEventNames()
        {
            string path = Path.Combine(Application.streamingAssetsPath, ContractRelativePath);

            if (!File.Exists(path))
            {
                Debug.LogError($"[Telemetry] Contract not found at: {path}");
                return new HashSet<string>();
            }

            string json = File.ReadAllText(path);
            var root = JsonUtility.FromJson<TelemetryContractRoot>(json);

            var set = new HashSet<string>(StringComparer.Ordinal);
            if (root?.events != null)
            {
                foreach (var ev in root.events)
                {
                    if (!string.IsNullOrWhiteSpace(ev.name))
                        set.Add(ev.name.Trim());
                }
            }

            if (set.Count == 0)
                Debug.LogError("[Telemetry] Loaded contract but found zero event names.");

            return set;
        }
    }
}
