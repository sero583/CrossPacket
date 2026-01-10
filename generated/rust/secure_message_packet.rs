// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SecureMessagePacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub message_id: String,
    pub sender_id: i64,
    pub recipient_id: i64,
    pub subject: String,
    pub body: String,
    pub attachments: Vec<serde_json::Value>,
    pub encrypted_payload: Option<Vec<u8>>,
    pub priority: i64,
    pub is_read: bool,
    pub sent_at: DateTime<Utc>,
}

impl SecureMessagePacket {
    pub const TYPE: &'static str = "/example/SecureMessagePacket";

    pub fn new(
        message_id: String,
        sender_id: i64,
        recipient_id: i64,
        subject: String,
        body: String,
        attachments: Vec<serde_json::Value>,
        encrypted_payload: Option<Vec<u8>>,
        priority: i64,
        is_read: bool,
        sent_at: DateTime<Utc>,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            message_id,
            sender_id,
            recipient_id,
            subject,
            body,
            attachments,
            encrypted_payload,
            priority,
            is_read,
            sent_at,
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