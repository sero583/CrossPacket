// CrossPacket - Rust Unit Tests
//
// Author: Serhat Gueler (sero583)
// GitHub: https://github.com/sero583
// License: MIT

use chrono::{Utc, NaiveTime};
use std::collections::HashMap;

// Import generated packets from output/rust
use crosspacket_generated::{
    PingPacket,
    PongPacket,
    MessagePacket,
    DataChunkPacket,
    ComprehensivePacket,
    UserProfilePacket,
    SecureMessagePacket,
};

// ============================================================================
// PingPacket Tests
// ============================================================================

#[test]
fn test_ping_packet_constructor() {
    let ts = Utc::now();
    let p = PingPacket::new(ts, "test".to_string());
    assert_eq!(p.packet_type, PingPacket::TYPE);
    assert_eq!(p.message, "test");
}

#[test]
fn test_ping_packet_type_constant() {
    assert_eq!(PingPacket::TYPE, "/example/PingPacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_ping_packet_json_roundtrip() {
    let p = PingPacket::new(Utc::now(), "hello".to_string());
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = PingPacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.message, "hello");
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_ping_packet_msgpack_roundtrip() {
    let p = PingPacket::new(Utc::now(), "msgpack test".to_string());
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = PingPacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.message, "msgpack test");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_ping_invalid_json() {
    let result = PingPacket::from_json("not valid json");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_ping_invalid_msgpack() {
    let result = PingPacket::from_msgpack(&[0xFF, 0xFE, 0xFD]);
    assert!(result.is_err());
}

// ============================================================================
// PongPacket Tests (latency_ms field)
// ============================================================================

#[test]
fn test_pong_packet_constructor() {
    let orig = Utc::now();
    let resp = orig;
    let p = PongPacket::new(orig, resp, 42);
    assert_eq!(p.packet_type, PongPacket::TYPE);
    assert_eq!(p.latency_ms, 42);
}

#[test]
fn test_pong_packet_type_constant() {
    assert_eq!(PongPacket::TYPE, "/example/PongPacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_pong_packet_json_roundtrip() {
    let p = PongPacket::new(Utc::now(), Utc::now(), 100);
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = PongPacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.latency_ms, 100);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_pong_packet_msgpack_roundtrip() {
    let p = PongPacket::new(Utc::now(), Utc::now(), 200);
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = PongPacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.latency_ms, 200);
}

#[cfg(all(not(feature = "no_json"), not(feature = "no_msgpack")))]
#[test]
fn test_pong_invalid_json() {
    let result = PongPacket::from_json("{{invalid");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_pong_invalid_msgpack() {
    let result = PongPacket::from_msgpack(&[0x00, 0x01]);
    assert!(result.is_err());
}

// ============================================================================
// MessagePacket Tests (sender_id, content, timestamp)
// ============================================================================

#[test]
fn test_message_packet_constructor() {
    let p = MessagePacket::new(
        "sender1".to_string(),
        "Hello!".to_string(),
        Utc::now(),
    );
    assert_eq!(p.packet_type, MessagePacket::TYPE);
    assert_eq!(p.content, "Hello!");
}

#[test]
fn test_message_packet_type_constant() {
    assert_eq!(MessagePacket::TYPE, "/chat/MessagePacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_message_packet_json_roundtrip() {
    let p = MessagePacket::new(
        "sender".to_string(),
        "Test content".to_string(),
        Utc::now(),
    );
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = MessagePacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.content, "Test content");
    assert_eq!(decoded.sender_id, "sender");
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_message_packet_msgpack_roundtrip() {
    let p = MessagePacket::new(
        "s".to_string(),
        "MsgPack content".to_string(),
        Utc::now(),
    );
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = MessagePacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.content, "MsgPack content");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_message_invalid_json() {
    let result = MessagePacket::from_json("");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_message_invalid_msgpack() {
    let result = MessagePacket::from_msgpack(&[]);
    assert!(result.is_err());
}

// ============================================================================
// DataChunkPacket Tests (chunk_index, total_chunks, data, checksum)
// ============================================================================

#[test]
fn test_data_chunk_constructor() {
    let p = DataChunkPacket::new(
        0,
        10,
        HashMap::new(),
        "abc123".to_string(),
    );
    assert_eq!(p.packet_type, DataChunkPacket::TYPE);
    assert_eq!(p.chunk_index, 0);
}

#[test]
fn test_data_chunk_type_constant() {
    assert_eq!(DataChunkPacket::TYPE, "/example/DataChunkPacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_data_chunk_json_roundtrip() {
    let mut data = HashMap::new();
    data.insert("key".to_string(), serde_json::json!("value"));
    let p = DataChunkPacket::new(
        5,
        20,
        data,
        "checksum".to_string(),
    );
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = DataChunkPacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.chunk_index, 5);
    assert_eq!(decoded.total_chunks, 20);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_data_chunk_msgpack_roundtrip() {
    let p = DataChunkPacket::new(
        1,
        5,
        HashMap::new(),
        "cs".to_string(),
    );
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = DataChunkPacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.chunk_index, 1);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_data_chunk_invalid_json() {
    let result = DataChunkPacket::from_json("null");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_data_chunk_invalid_msgpack() {
    let result = DataChunkPacket::from_msgpack(&[0x80]);
    assert!(result.is_err());
}

// ============================================================================
// ComprehensivePacket Tests
// ============================================================================

#[test]
fn test_comprehensive_constructor() {
    let p = ComprehensivePacket::new(
        42,                                           // int_field
        3.14,                                         // float_field
        2.718,                                        // double_field
        "test".to_string(),                           // string_field
        true,                                         // bool_field
        Utc::now(),                                   // datetime_field
        NaiveTime::from_hms_opt(12, 30, 0).unwrap(),  // time_field
        vec![serde_json::json!(1)],                   // list_field
        vec![1, 2, 3],                                // list_int_field
        vec!["a".to_string(), "b".to_string()],       // list_string_field
        HashMap::new(),                               // map_field
        HashMap::new(),                               // embedded_map_field
        HashMap::new(),                               // map_string_dynamic_field
        vec![0xDE, 0xAD],                             // bytes_field
    );
    assert_eq!(p.packet_type, ComprehensivePacket::TYPE);
    assert_eq!(p.int_field, 42);
}

#[test]
fn test_comprehensive_type_constant() {
    assert_eq!(ComprehensivePacket::TYPE, "/test/ComprehensivePacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_comprehensive_json_roundtrip() {
    let mut map = HashMap::new();
    map.insert("key".to_string(), serde_json::json!("value"));
    
    let p = ComprehensivePacket::new(
        100, 99.99, 88.88, "comprehensive".to_string(), false,
        Utc::now(), NaiveTime::from_hms_opt(10, 0, 0).unwrap(),
        vec![serde_json::json!("item")], vec![10, 20], vec!["x".to_string()],
        map, HashMap::new(), HashMap::new(), vec![1, 2, 3, 4],
    );
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = ComprehensivePacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.int_field, 100);
    assert_eq!(decoded.string_field, "comprehensive");
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_comprehensive_msgpack_roundtrip() {
    let p = ComprehensivePacket::new(
        999, 1.5, 2.5, "mp".to_string(), true,
        Utc::now(), NaiveTime::from_hms_opt(15, 30, 45).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = ComprehensivePacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.int_field, 999);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_comprehensive_invalid_json() {
    let result = ComprehensivePacket::from_json("[]");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_comprehensive_invalid_msgpack() {
    let result = ComprehensivePacket::from_msgpack(&[0xC1]);
    assert!(result.is_err());
}

// ============================================================================
// UserProfilePacket Tests
// user_id: i64, username: String, email: String, bio: Option<String>,
// age: Option<i64>, balance: f64, tags: Vec<String>,
// preferences: HashMap<String, Value>, avatar: Option<Vec<u8>>,
// created_at: DateTime<Utc>, last_login: Option<DateTime<Utc>>
// ============================================================================

#[test]
fn test_user_profile_constructor() {
    let p = UserProfilePacket::new(
        123,                              // user_id: i64
        "john_doe".to_string(),           // username
        "john@example.com".to_string(),   // email
        Some("Hello!".to_string()),       // bio
        Some(30),                         // age
        100.50,                           // balance
        vec!["admin".to_string()],        // tags
        HashMap::new(),                   // preferences
        None,                             // avatar
        Utc::now(),                       // created_at
        None,                             // last_login
    );
    assert_eq!(p.packet_type, UserProfilePacket::TYPE);
    assert_eq!(p.username, "john_doe");
}

#[test]
fn test_user_profile_type_constant() {
    assert_eq!(UserProfilePacket::TYPE, "/example/UserProfilePacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_user_profile_json_roundtrip() {
    let p = UserProfilePacket::new(
        1, "alice".to_string(), "alice@test.com".to_string(),
        None, Some(25), 50.0, vec!["user".to_string()],
        HashMap::new(), None, Utc::now(), None,
    );
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = UserProfilePacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.username, "alice");
    assert_eq!(decoded.age, Some(25));
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_user_profile_msgpack_roundtrip() {
    let p = UserProfilePacket::new(
        2, "bob".to_string(), "bob@test.com".to_string(),
        Some("Bio".to_string()), Some(35), 999.99, vec![],
        HashMap::new(), None, Utc::now(), Some(Utc::now()),
    );
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = UserProfilePacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.username, "bob");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_user_profile_invalid_json() {
    let result = UserProfilePacket::from_json("123");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_user_profile_invalid_msgpack() {
    let result = UserProfilePacket::from_msgpack(&[0xFF, 0xFF]);
    assert!(result.is_err());
}

// ============================================================================
// SecureMessagePacket Tests
// message_id: String, sender_id: i64, recipient_id: i64, subject: String,
// body: String, attachments: Vec<Value>, encrypted_payload: Option<Vec<u8>>,
// priority: i64, is_read: bool, sent_at: DateTime<Utc>
// ============================================================================

#[test]
fn test_secure_message_constructor() {
    let p = SecureMessagePacket::new(
        "msg-001".to_string(),             // message_id
        1,                                 // sender_id
        2,                                 // recipient_id
        "Subject".to_string(),             // subject
        "Body text".to_string(),           // body
        vec![],                            // attachments
        Some(vec![0x01, 0x02, 0x03]),       // encrypted_payload
        1,                                 // priority
        false,                             // is_read
        Utc::now(),                        // sent_at
    );
    assert_eq!(p.packet_type, SecureMessagePacket::TYPE);
    assert_eq!(p.message_id, "msg-001");
}

#[test]
fn test_secure_message_type_constant() {
    assert_eq!(SecureMessagePacket::TYPE, "/example/SecureMessagePacket");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_secure_message_json_roundtrip() {
    let p = SecureMessagePacket::new(
        "sec-123".to_string(), 10, 20, "Hello".to_string(), "World".to_string(),
        vec![serde_json::json!({"file": "doc.pdf"})], None, 5, true, Utc::now(),
    );
    let json = p.to_json().expect("JSON serialize failed");
    let decoded = SecureMessagePacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded.message_id, "sec-123");
    assert_eq!(decoded.subject, "Hello");
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_secure_message_msgpack_roundtrip() {
    let p = SecureMessagePacket::new(
        "mp-sec".to_string(), 100, 200, "Test".to_string(), "Content".to_string(),
        vec![], Some(vec![0xDE, 0xAD]), 3, false, Utc::now(),
    );
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded = SecureMessagePacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded.message_id, "mp-sec");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_secure_message_invalid_json() {
    let result = SecureMessagePacket::from_json("{}");
    assert!(result.is_err());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_secure_message_invalid_msgpack() {
    let result = SecureMessagePacket::from_msgpack(&[0xC0]);
    assert!(result.is_err());
}

// ============================================================================
// Edge Case Tests - Integers
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_int_zero() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.int_field, 0);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_int_positive() {
    let p = ComprehensivePacket::new(
        42, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.int_field, 42);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_int_negative() {
    let p = ComprehensivePacket::new(
        -999, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.int_field, -999);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_int_large_positive() {
    let p = ComprehensivePacket::new(
        9223372036854775807i64, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert_eq!(decoded.int_field, 9223372036854775807i64);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_int_large_negative() {
    let p = ComprehensivePacket::new(
        -9223372036854775808i64, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert_eq!(decoded.int_field, -9223372036854775808i64);
}

// ============================================================================
// Edge Case Tests - Floats
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_zero() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!((decoded.float_field - 0.0).abs() < f64::EPSILON);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_pi() {
    let p = ComprehensivePacket::new(
        0, std::f64::consts::PI, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!((decoded.float_field - std::f64::consts::PI).abs() < 1e-10);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_euler() {
    let p = ComprehensivePacket::new(
        0, std::f64::consts::E, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!((decoded.float_field - std::f64::consts::E).abs() < 1e-10);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_negative() {
    let p = ComprehensivePacket::new(
        0, -123.456, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!((decoded.float_field - (-123.456)).abs() < 1e-10);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_very_small() {
    let p = ComprehensivePacket::new(
        0, 1e-100, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.float_field > 0.0 && decoded.float_field < 1e-50);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_float_very_large() {
    let p = ComprehensivePacket::new(
        0, 1e100, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.float_field > 1e50);
}

// ============================================================================
// Edge Case Tests - Strings
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_string_empty() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.string_field, "");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_string_unicode() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "Hello 世界 🌍 مرحبا".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.string_field, "Hello 世界 🌍 مرحبا");
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_string_special_chars() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "Quote: \"test\" Backslash: \\ Tab: \t".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.string_field.contains("Quote"));
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_string_newlines() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "line1\nline2\r\nline3".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.string_field.contains("line1"));
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_string_whitespace() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "   spaces   ".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.string_field, "   spaces   ");
}

// ============================================================================
// Edge Case Tests - Booleans
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_bool_true() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), true, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.bool_field);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_bool_false() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(!decoded.bool_field);
}

// ============================================================================
// Edge Case Tests - Lists
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_list_empty() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.list_field.is_empty());
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_list_int() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![1, 2, 3, 4, 5], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.list_int_field.len(), 5);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_list_string() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec!["a".to_string(), "b".to_string(), "c".to_string()],
        HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.list_string_field.len(), 3);
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_list_mixed_values() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![serde_json::json!(1), serde_json::json!("two"), serde_json::json!(3.0)],
        vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.list_field.len(), 3);
}

// ============================================================================
// Edge Case Tests - Maps
// ============================================================================

#[cfg(not(feature = "no_json"))]
#[test]
fn test_map_empty() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert!(decoded.map_field.is_empty());
}

#[cfg(not(feature = "no_json"))]
#[test]
fn test_map_with_entries() {
    let mut map = HashMap::new();
    map.insert("key1".to_string(), serde_json::json!("value1"));
    map.insert("key2".to_string(), serde_json::json!(42));
    map.insert("key3".to_string(), serde_json::json!(true));
    
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], map, HashMap::new(), HashMap::new(), vec![],
    );
    let json = p.to_json().unwrap();
    let decoded = ComprehensivePacket::from_json(&json).unwrap();
    assert_eq!(decoded.map_field.len(), 3);
}

// ============================================================================
// Edge Case Tests - Bytes
// ============================================================================

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_bytes_empty() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(), vec![],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert!(decoded.bytes_field.is_empty());
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_bytes_deadbeef() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(),
        vec![0xDE, 0xAD, 0xBE, 0xEF],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert_eq!(decoded.bytes_field, vec![0xDE, 0xAD, 0xBE, 0xEF]);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_bytes_all_zeros() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(),
        vec![0x00, 0x00, 0x00, 0x00],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert_eq!(decoded.bytes_field, vec![0x00, 0x00, 0x00, 0x00]);
}

#[cfg(not(feature = "no_msgpack"))]
#[test]
fn test_bytes_all_ones() {
    let p = ComprehensivePacket::new(
        0, 0.0, 0.0, "".to_string(), false, Utc::now(),
        NaiveTime::from_hms_opt(0, 0, 0).unwrap(),
        vec![], vec![], vec![], HashMap::new(), HashMap::new(), HashMap::new(),
        vec![0xFF, 0xFF, 0xFF, 0xFF],
    );
    let bytes = p.to_msgpack().unwrap();
    let decoded = ComprehensivePacket::from_msgpack(&bytes).unwrap();
    assert_eq!(decoded.bytes_field, vec![0xFF, 0xFF, 0xFF, 0xFF]);
}

// ============================================================================
// Security-Critical Payload Test
// ============================================================================

#[cfg(all(not(feature = "no_json"), not(feature = "no_msgpack")))]
#[test]
fn test_security_critical_payload() {
    let mut secure_map = HashMap::new();
    secure_map.insert("source_account".to_string(), serde_json::json!("ACC-12345"));
    secure_map.insert("dest_account".to_string(), serde_json::json!("ACC-67890"));
    secure_map.insert("amount_cents".to_string(), serde_json::json!(9999999));

    let p = ComprehensivePacket::new(
        1234567890123456789i64, 99999.99, 88888.88,
        "TRANSFER:ACC-12345→ACC-67890".to_string(), true,
        Utc::now(), NaiveTime::from_hms_opt(12, 0, 0).unwrap(),
        vec![serde_json::json!("audit1"), serde_json::json!("audit2")],
        vec![1, 2, 3], vec!["log1".to_string()],
        secure_map, HashMap::new(), HashMap::new(),
        vec![0xDE, 0xAD, 0xBE, 0xEF],
    );

    // Test JSON roundtrip
    let json = p.to_json().expect("JSON serialize failed");
    let decoded_json = ComprehensivePacket::from_json(&json).expect("JSON deserialize failed");
    assert_eq!(decoded_json.int_field, 1234567890123456789i64);
    assert_eq!(decoded_json.string_field, "TRANSFER:ACC-12345→ACC-67890");
    assert!(decoded_json.bool_field);
    
    // Test MsgPack roundtrip
    let bytes = p.to_msgpack().expect("MsgPack serialize failed");
    let decoded_mp = ComprehensivePacket::from_msgpack(&bytes).expect("MsgPack deserialize failed");
    assert_eq!(decoded_mp.int_field, 1234567890123456789i64);
    assert_eq!(decoded_mp.string_field, "TRANSFER:ACC-12345→ACC-67890");
}
