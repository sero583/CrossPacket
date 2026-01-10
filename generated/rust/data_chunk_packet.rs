// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataChunkPacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub chunk_index: i64,
    pub total_chunks: i64,
    pub data: HashMap<String, serde_json::Value>,
    pub checksum: String,
}

impl DataChunkPacket {
    pub const TYPE: &'static str = "/example/DataChunkPacket";

    pub fn new(
        chunk_index: i64,
        total_chunks: i64,
        data: HashMap<String, serde_json::Value>,
        checksum: String,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            chunk_index,
            total_chunks,
            data,
            checksum,
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