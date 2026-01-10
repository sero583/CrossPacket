// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserProfilePacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub user_id: i64,
    pub username: String,
    pub email: String,
    pub bio: Option<String>,
    pub age: Option<i64>,
    pub balance: f64,
    pub tags: Vec<String>,
    pub preferences: HashMap<String, serde_json::Value>,
    pub avatar: Option<Vec<u8>>,
    pub created_at: DateTime<Utc>,
    pub last_login: Option<DateTime<Utc>>,
}

impl UserProfilePacket {
    pub const TYPE: &'static str = "/example/UserProfilePacket";

    pub fn new(
        user_id: i64,
        username: String,
        email: String,
        bio: Option<String>,
        age: Option<i64>,
        balance: f64,
        tags: Vec<String>,
        preferences: HashMap<String, serde_json::Value>,
        avatar: Option<Vec<u8>>,
        created_at: DateTime<Utc>,
        last_login: Option<DateTime<Utc>>,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            user_id,
            username,
            email,
            bio,
            age,
            balance,
            tags,
            preferences,
            avatar,
            created_at,
            last_login,
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