using System.IO;
using System.Text;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    public class JsonlTelemetryWriter
    {
        private readonly string _filePath;

        public JsonlTelemetryWriter(string filePath)
        {
            _filePath = filePath;
            var dir = Path.GetDirectoryName(_filePath);
            if (!string.IsNullOrEmpty(dir))
                Directory.CreateDirectory(dir);
        }

        public void AppendLine(string jsonLine)
        {
            // Append-only write
            File.AppendAllText(_filePath, jsonLine + "\n", Encoding.UTF8);
        }

        public string FilePath => _filePath;
    }
}
