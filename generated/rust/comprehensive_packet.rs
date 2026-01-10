// Auto-generated - do not modify manually
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc, NaiveTime};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ComprehensivePacket {
    #[serde(rename = "packetType")]
    pub packet_type: String,
    pub int_field: i64,
    pub float_field: f64,
    pub double_field: f64,
    pub string_field: String,
    pub bool_field: bool,
    pub datetime_field: DateTime<Utc>,
    pub time_field: NaiveTime,
    pub list_field: Vec<serde_json::Value>,
    pub list_int_field: Vec<i64>,
    pub list_string_field: Vec<String>,
    pub map_field: HashMap<String, serde_json::Value>,
    pub embedded_map_field: HashMap<String, serde_json::Value>,
    pub map_string_dynamic_field: HashMap<String, serde_json::Value>,
    pub bytes_field: Vec<u8>,
}

impl ComprehensivePacket {
    pub const TYPE: &'static str = "/test/ComprehensivePacket";

    pub fn new(
        int_field: i64,
        float_field: f64,
        double_field: f64,
        string_field: String,
        bool_field: bool,
        datetime_field: DateTime<Utc>,
        time_field: NaiveTime,
        list_field: Vec<serde_json::Value>,
        list_int_field: Vec<i64>,
        list_string_field: Vec<String>,
        map_field: HashMap<String, serde_json::Value>,
        embedded_map_field: HashMap<String, serde_json::Value>,
        map_string_dynamic_field: HashMap<String, serde_json::Value>,
        bytes_field: Vec<u8>,
    ) -> Self {
        Self {
            packet_type: Self::TYPE.to_string(),
            int_field,
            float_field,
            double_field,
            string_field,
            bool_field,
            datetime_field,
            time_field,
            list_field,
            list_int_field,
            list_string_field,
            map_field,
            embedded_map_field,
            map_string_dynamic_field,
            bytes_field,
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