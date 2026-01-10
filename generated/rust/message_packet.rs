// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MessagePacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub sender_id: String,
    pub content: String,
    pub timestamp: DateTime<Utc>,
}

impl MessagePacket {
    pub const TYPE: &'static str = "/chat/MessagePacket";

    pub fn new(
        sender_id: String,
        content: String,
        timestamp: DateTime<Utc>,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            sender_id,
            content,
            timestamp,
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