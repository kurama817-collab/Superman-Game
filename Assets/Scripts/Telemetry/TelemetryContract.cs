using System;
using System.Collections.Generic;
using UnityEngine;

namespace ProtocolPsi.Telemetry
{
    [Serializable]
    public class TelemetryContractRoot
    {
        public ContractVersion version;
        public ContractEnvelope envelope;
        public ContractCadence cadence;
        public List<ContractEvent> events;
    }

    [Serializable]
    public class ContractVersion
    {
        public int major;
        public int minor;
        public string tag;
    }

    [Serializable]
    public class ContractEnvelope
    {
        public string format;
        public List<string> required_fields;
    }

    [Serializable]
    public class ContractCadence
    {
        public int W_EVALUATION_TICK_ms;
    }

    [Serializable]
    public class ContractEvent
    {
        public string name;
        public string domain;
        public string description;
        // payload is a schema map; we don't strongly type it here.
        public SerializableDictionary payload;
    }

    /// <summary>
    /// Minimal serializable dictionary for JsonUtility limitations.
    /// We store payload schema as key/value pairs.
    /// </summary>
    [Serializable]
    public class SerializableDictionary
    {
        public List<string> keys = new List<string>();
        public List<string> values = new List<string>();
    }
}
