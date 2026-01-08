using System;
using System.IO;
using System.Text;
using UnityEngine;

public class TelemetryEmitter : MonoBehaviour
{
    private static readonly object WriteLock = new object();
    private static TelemetryEmitter instance;

    [SerializeField] private string fileName = "telemetry.jsonl";

    private string filePath;

    private void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        filePath = Path.Combine(Application.persistentDataPath, fileName);
    }

    public static void Emit(string eventName, string payloadJson = "{}")
    {
        if (instance == null)
        {
            Debug.LogWarning("TelemetryEmitter is not present in the scene. Add it to a GameObject before emitting.");
            return;
        }

        instance.AppendEventLine(eventName, payloadJson);
    }

    private void AppendEventLine(string eventName, string payloadJson)
    {
        if (string.IsNullOrWhiteSpace(eventName))
        {
            Debug.LogWarning("TelemetryEmitter received an empty event name.");
            return;
        }

        if (string.IsNullOrWhiteSpace(payloadJson))
        {
            payloadJson = "{}";
        }

        string line = BuildJsonLine(eventName, payloadJson);
        lock (WriteLock)
        {
            File.AppendAllText(filePath, line + Environment.NewLine, Encoding.UTF8);
        }
    }

    private static string BuildJsonLine(string eventName, string payloadJson)
    {
        string timestamp = DateTime.UtcNow.ToString("O");
        var builder = new StringBuilder(256);
        builder.Append("{\"event\":\"")
            .Append(EscapeJson(eventName))
            .Append("\",\"timestamp\":\"")
            .Append(timestamp)
            .Append("\",\"payload\":");
        builder.Append(payloadJson);
        builder.Append('}');
        return builder.ToString();
    }

    private static string EscapeJson(string value)
    {
        return value
            .Replace("\\", "\\\\")
            .Replace("\"", "\\\"")
            .Replace("\n", "\\n")
            .Replace("\r", "\\r")
            .Replace("\t", "\\t");
    }
}
