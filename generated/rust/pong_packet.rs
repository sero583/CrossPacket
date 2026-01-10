// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PongPacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub original_timestamp: DateTime<Utc>,
    pub response_timestamp: DateTime<Utc>,
    pub latency_ms: i64,
}

impl PongPacket {
    pub const TYPE: &'static str = "/example/PongPacket";

    pub fn new(
        original_timestamp: DateTime<Utc>,
        response_timestamp: DateTime<Utc>,
        latency_ms: i64,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            original_timestamp,
            response_timestamp,
            latency_ms,
        }
    }

    pub fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string(self)
    }

    pub fn from_json(json: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(json)
    }

    pub fn to_msgpack(&self) -> Result<Vec<u8>, rmp_serde::encode::Error> {
        rmp_serde::to_vec(self)
    }

    pub fn from_msgpack(bytes: &[u8]) -> Result<Self, rmp_serde::decode::Error> {
        rmp_serde::from_slice(bytes)
    }
}