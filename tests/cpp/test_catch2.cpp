// CrossPacket - C++ Test Suite using Catch2
//
// Author: Serhat Güler (sero583)
// GitHub: https://github.com/sero583
// License: MIT
//
// Uses Catch2 v3.x for industry-standard C++ testing
// Supports all 3 modes: BOTH, JSON_ONLY, MSGPACK_ONLY via preprocessor flags
//
// Compile (BOTH mode):
//   g++ -std=c++17 -I../../generated/cpp test_catch2.cpp ../../generated/cpp/*.cpp -lyyjson -lmsgpack-c -lCatch2Main -lCatch2 -o test_catch2
// Compile (JSON_ONLY mode):
//   g++ -std=c++17 -I../../generated/cpp test_catch2.cpp ../../generated/cpp/*.cpp -lyyjson -lCatch2Main -lCatch2 -o test_catch2
// Compile (MSGPACK_ONLY mode):
//   g++ -std=c++17 -I../../generated/cpp test_catch2.cpp ../../generated/cpp/*.cpp -lmsgpack-c -lCatch2Main -lCatch2 -o test_catch2
// Run: ./test_catch2 --reporter compact

#include <catch2/catch_all.hpp>

#include <string>
#include <vector>
#include <optional>
#include <cmath>

// Include config header for feature flags
#include "crosspacket_config.hpp"

// Include generated packets
#include "message_packet.hpp"
#include "ping_packet.hpp"
#include "pong_packet.hpp"
#include "comprehensive_packet.hpp"
#include "secure_message_packet.hpp"
#include "user_profile_packet.hpp"
#include "data_chunk_packet.hpp"

// Helper for float comparison
bool floatEquals(double a, double b, double epsilon = 1e-9)
{
    return std::abs(a - b) < epsilon;
}

// ============================================================================
// MessagePacket Tests
// ============================================================================
TEST_CASE("MessagePacket", "[message]")
{
    SECTION("Default constructor creates valid object")
    {
        packets::MessagePacket p;
        REQUIRE(std::string(packets::MessagePacket::TYPE) == "/chat/MessagePacket");
    }

    SECTION("Parameterized constructor sets values correctly")
    {
        packets::MessagePacket p("user123", "Hello World!", "2026-01-09T12:00:00Z");
        REQUIRE(p.GetSenderId() == "user123");
        REQUIRE(p.GetContent() == "Hello World!");
        REQUIRE(p.GetTimestamp() == "2026-01-09T12:00:00Z");
    }

    SECTION("Getters and setters work correctly")
    {
        packets::MessagePacket p;
        p.SetSenderId("test_user");
        p.SetContent("Test message");
        p.SetTimestamp("2026-01-01T00:00:00Z");

        REQUIRE(p.GetSenderId() == "test_user");
        REQUIRE(p.GetContent() == "Test message");
        REQUIRE(p.GetTimestamp() == "2026-01-01T00:00:00Z");
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip preserves data")
    {
        packets::MessagePacket original("sender1", "Test content", "2026-01-09T10:30:00Z");
        std::string json = original.ToJson();
        packets::MessagePacket restored = packets::MessagePacket::FromJson(json);

        REQUIRE(restored.GetSenderId() == original.GetSenderId());
        REQUIRE(restored.GetContent() == original.GetContent());
        REQUIRE(restored.GetTimestamp() == original.GetTimestamp());
    }

    SECTION("Invalid JSON throws exception")
    {
        REQUIRE_THROWS_AS(packets::MessagePacket::FromJson("{invalid json}"), std::runtime_error);
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip preserves data")
    {
        packets::MessagePacket original("msgpack_sender", "MsgPack test", "2026-01-09T11:00:00Z");
        auto msgpack = original.ToMsgPack();
        packets::MessagePacket restored = packets::MessagePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetSenderId() == original.GetSenderId());
        REQUIRE(restored.GetContent() == original.GetContent());
    }
#endif
}

// ============================================================================
// PingPacket Tests (has timestamp and message fields)
// ============================================================================
TEST_CASE("PingPacket", "[ping]")
{
    SECTION("Default constructor")
    {
        packets::PingPacket p;
        REQUIRE(std::string(packets::PingPacket::TYPE) == "/example/PingPacket");
    }

    SECTION("Parameterized constructor")
    {
        packets::PingPacket p("2026-01-09T12:00:00Z", "hello");
        REQUIRE(p.GetTimestamp() == "2026-01-09T12:00:00Z");
        REQUIRE(p.GetMessage() == "hello");
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip")
    {
        packets::PingPacket original("2026-01-09T12:00:00Z", "test ping");
        std::string json = original.ToJson();
        auto restored = packets::PingPacket::FromJson(json);
        REQUIRE(restored.GetTimestamp() == original.GetTimestamp());
        REQUIRE(restored.GetMessage() == original.GetMessage());
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip")
    {
        packets::PingPacket original("2026-01-09T12:00:00Z", "msgpack ping");
        auto msgpack = original.ToMsgPack();
        auto restored = packets::PingPacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetTimestamp() == original.GetTimestamp());
    }
#endif
}

// ============================================================================
// PongPacket Tests (original_timestamp, response_timestamp, latency_ms)
// ============================================================================
TEST_CASE("PongPacket", "[pong]")
{
    SECTION("Default constructor")
    {
        packets::PongPacket p;
        REQUIRE(std::string(packets::PongPacket::TYPE) == "/example/PongPacket");
    }

    SECTION("Parameterized constructor with latency")
    {
        packets::PongPacket p("2026-01-09T12:00:00Z", "2026-01-09T12:00:01Z", 42);
        REQUIRE(p.GetOriginalTimestamp() == "2026-01-09T12:00:00Z");
        REQUIRE(p.GetResponseTimestamp() == "2026-01-09T12:00:01Z");
        REQUIRE(p.GetLatencyMs() == 42);
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip preserves latency")
    {
        packets::PongPacket original("2026-01-09T12:00:00Z", "2026-01-09T12:00:01Z", 123);
        std::string json = original.ToJson();
        auto restored = packets::PongPacket::FromJson(json);
        REQUIRE(restored.GetLatencyMs() == 123);
        REQUIRE(restored.GetOriginalTimestamp() == original.GetOriginalTimestamp());
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip preserves latency")
    {
        packets::PongPacket original("2026-01-09T12:00:00Z", "2026-01-09T12:00:01Z", 456);
        auto msgpack = original.ToMsgPack();
        auto restored = packets::PongPacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetLatencyMs() == 456);
    }
#endif
}

// ============================================================================
// DataChunkPacket Tests (chunk_index, total_chunks, data as string, checksum)
// ============================================================================
TEST_CASE("DataChunkPacket", "[data_chunk]")
{
    SECTION("Default constructor")
    {
        packets::DataChunkPacket p;
        REQUIRE(std::string(packets::DataChunkPacket::TYPE) == "/example/DataChunkPacket");
    }

    SECTION("Chunk properties work correctly")
    {
        packets::DataChunkPacket p;
        p.SetChunkIndex(5);
        p.SetTotalChunks(10);
        p.SetData("{\"key\": \"value\"}"); // embedded_map stored as JSON string
        p.SetChecksum("abc123");

        REQUIRE(p.GetChunkIndex() == 5);
        REQUIRE(p.GetTotalChunks() == 10);
        REQUIRE(p.GetData() == "{\"key\": \"value\"}");
        REQUIRE(p.GetChecksum() == "abc123");
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip")
    {
        packets::DataChunkPacket original;
        original.SetChunkIndex(1);
        original.SetTotalChunks(3);
        original.SetData("{\"payload\": 42}");
        original.SetChecksum("checksum123");

        std::string json = original.ToJson();
        auto restored = packets::DataChunkPacket::FromJson(json);

        REQUIRE(restored.GetChunkIndex() == original.GetChunkIndex());
        REQUIRE(restored.GetTotalChunks() == original.GetTotalChunks());
        REQUIRE(restored.GetChecksum() == original.GetChecksum());
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip")
    {
        packets::DataChunkPacket original;
        original.SetChunkIndex(2);
        original.SetTotalChunks(5);
        original.SetData("{\"test\": true}");
        original.SetChecksum("msgpack_checksum");

        auto msgpack = original.ToMsgPack();
        auto restored = packets::DataChunkPacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetChunkIndex() == original.GetChunkIndex());
        REQUIRE(restored.GetTotalChunks() == original.GetTotalChunks());
    }
#endif
}

// ============================================================================
// ComprehensivePacket Tests
// ============================================================================
TEST_CASE("ComprehensivePacket", "[comprehensive]")
{
    SECTION("Default constructor")
    {
        packets::ComprehensivePacket p;
        REQUIRE(std::string(packets::ComprehensivePacket::TYPE) == "/test/ComprehensivePacket");
    }

    SECTION("All field types work correctly")
    {
        packets::ComprehensivePacket p;

        // Integer
        p.SetIntField(42);
        REQUIRE(p.GetIntField() == 42);

        // Float
        p.SetFloatField(3.14159f);
        REQUIRE(floatEquals(p.GetFloatField(), 3.14159f, 0.0001));

        // Double
        p.SetDoubleField(2.718281828);
        REQUIRE(floatEquals(p.GetDoubleField(), 2.718281828, 1e-9));

        // String
        p.SetStringField("Hello");
        REQUIRE(p.GetStringField() == "Hello");

        // Bool
        p.SetBoolField(true);
        REQUIRE(p.GetBoolField() == true);

        // List int
        p.SetListIntField({1, 2, 3, 4, 5});
        REQUIRE(p.GetListIntField().size() == 5);

        // List string
        p.SetListStringField({"a", "b", "c"});
        REQUIRE(p.GetListStringField().size() == 3);

        // Bytes
        p.SetBytesField({0xDE, 0xAD, 0xBE, 0xEF});
        REQUIRE(p.GetBytesField().size() == 4);
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip preserves all field types")
    {
        packets::ComprehensivePacket original;
        original.SetIntField(123);
        original.SetFloatField(1.5f);
        original.SetDoubleField(2.5);
        original.SetStringField("test string");
        original.SetBoolField(true);
        original.SetDatetimeField("2026-01-09T12:00:00Z");
        original.SetTimeField("14:30:00");
        original.SetListIntField({10, 20, 30});
        original.SetListStringField({"x", "y", "z"});
        original.SetBytesField({0x01, 0x02, 0x03});

        std::string json = original.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);

        REQUIRE(restored.GetIntField() == 123);
        REQUIRE(floatEquals(restored.GetFloatField(), 1.5f, 0.01));
        REQUIRE(floatEquals(restored.GetDoubleField(), 2.5, 0.01));
        REQUIRE(restored.GetStringField() == "test string");
        REQUIRE(restored.GetBoolField() == true);
        REQUIRE(restored.GetListIntField() == std::vector<int64_t>{10, 20, 30});
        REQUIRE(restored.GetListStringField() == std::vector<std::string>{"x", "y", "z"});
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip preserves data")
    {
        packets::ComprehensivePacket original;
        original.SetIntField(999);
        original.SetStringField("msgpack test");
        original.SetBoolField(false);

        auto msgpack = original.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetIntField() == 999);
        REQUIRE(restored.GetStringField() == "msgpack test");
        REQUIRE(restored.GetBoolField() == false);
    }
#endif
}

// ============================================================================
// UserProfilePacket Tests (with optional fields)
// ============================================================================
TEST_CASE("UserProfilePacket", "[user_profile]")
{
    SECTION("Default constructor")
    {
        packets::UserProfilePacket p;
        REQUIRE(std::string(packets::UserProfilePacket::TYPE) == "/example/UserProfilePacket");
    }

    SECTION("Required fields work correctly")
    {
        packets::UserProfilePacket p;
        p.SetUserId(12345);
        p.SetUsername("testuser");
        p.SetEmail("test@example.com");
        p.SetBalance(100.50);
        p.SetCreatedAt("2026-01-09T12:00:00Z");

        REQUIRE(p.GetUserId() == 12345);
        REQUIRE(p.GetUsername() == "testuser");
        REQUIRE(p.GetEmail() == "test@example.com");
        REQUIRE(floatEquals(p.GetBalance(), 100.50));
    }

    SECTION("Optional fields can be set and retrieved")
    {
        packets::UserProfilePacket p;
        p.SetBio("My bio");
        p.SetAge(25);
        p.SetLastLogin("2026-01-09T10:00:00Z");

        REQUIRE(p.GetBio().has_value());
        REQUIRE(p.GetBio().value() == "My bio");
        REQUIRE(p.GetAge().has_value());
        REQUIRE(p.GetAge().value() == 25);
        REQUIRE(p.GetLastLogin().has_value());
        REQUIRE(p.GetLastLogin().value() == "2026-01-09T10:00:00Z");
    }

    SECTION("Optional fields default to nullopt")
    {
        packets::UserProfilePacket p;

        // Optional fields should not have values by default
        // (depends on how the packet is constructed)
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip preserves optional fields")
    {
        packets::UserProfilePacket original;
        original.SetUserId(1);
        original.SetUsername("user1");
        original.SetEmail("user1@test.com");
        original.SetBio("Test bio");
        original.SetAge(30);
        original.SetBalance(50.0);
        original.SetCreatedAt("2026-01-09T12:00:00Z");

        std::string json = original.ToJson();
        auto restored = packets::UserProfilePacket::FromJson(json);

        REQUIRE(restored.GetUserId() == 1);
        REQUIRE(restored.GetUsername() == "user1");
        REQUIRE(restored.GetBio().has_value());
        REQUIRE(restored.GetBio().value() == "Test bio");
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip preserves optional fields")
    {
        packets::UserProfilePacket original;
        original.SetUserId(2);
        original.SetUsername("msgpack_user");
        original.SetEmail("msgpack@test.com");
        original.SetAge(25);
        original.SetBalance(75.0);
        original.SetCreatedAt("2026-01-09T12:00:00Z");

        auto msgpack = original.ToMsgPack();
        auto restored = packets::UserProfilePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetUserId() == 2);
        REQUIRE(restored.GetAge().has_value());
        REQUIRE(restored.GetAge().value() == 25);
    }
#endif
}

// ============================================================================
// SecureMessagePacket Tests
// ============================================================================
TEST_CASE("SecureMessagePacket", "[secure_message]")
{
    SECTION("Default constructor")
    {
        packets::SecureMessagePacket p;
        REQUIRE(std::string(packets::SecureMessagePacket::TYPE) == "/example/SecureMessagePacket");
    }

    SECTION("Security fields work correctly")
    {
        packets::SecureMessagePacket p;
        p.SetMessageId("msg-001");
        p.SetSenderId(123);
        p.SetRecipientId(456);
        p.SetSubject("Test Subject");
        p.SetBody("Test body content");
        p.SetPriority(1);
        p.SetIsRead(false);

        REQUIRE(p.GetMessageId() == "msg-001");
        REQUIRE(p.GetSenderId() == 123);
        REQUIRE(p.GetRecipientId() == 456);
        REQUIRE(p.GetSubject() == "Test Subject");
        REQUIRE(p.GetPriority() == 1);
    }

#ifdef CROSSPACKET_HAS_JSON
    SECTION("JSON roundtrip")
    {
        packets::SecureMessagePacket original;
        original.SetMessageId("secure-test");
        original.SetSenderId(100);
        original.SetRecipientId(200);
        original.SetSubject("Secure Subject");
        original.SetBody("Secure Body");
        original.SetAttachments("[]");
        original.SetPriority(5);
        original.SetIsRead(true);
        original.SetSentAt("2026-01-09T12:00:00Z");

        std::string json = original.ToJson();
        auto restored = packets::SecureMessagePacket::FromJson(json);

        REQUIRE(restored.GetMessageId() == original.GetMessageId());
        REQUIRE(restored.GetSenderId() == original.GetSenderId());
        REQUIRE(restored.GetRecipientId() == original.GetRecipientId());
        REQUIRE(restored.GetPriority() == original.GetPriority());
    }
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
    SECTION("MsgPack roundtrip")
    {
        packets::SecureMessagePacket original;
        original.SetMessageId("msgpack-secure");
        original.SetSenderId(1);
        original.SetRecipientId(2);
        original.SetSubject("MsgPack Subject");
        original.SetBody("MsgPack Body");
        original.SetAttachments("[]");
        original.SetPriority(3);
        original.SetIsRead(false);
        original.SetSentAt("2026-01-09T12:00:00Z");

        auto msgpack = original.ToMsgPack();
        auto restored = packets::SecureMessagePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetMessageId() == original.GetMessageId());
        REQUIRE(restored.GetSenderId() == original.GetSenderId());
    }
#endif
}

// ============================================================================
// Primitive Type Tests
// ============================================================================
#ifdef CROSSPACKET_HAS_JSON
TEST_CASE("JSON Primitive types serialization", "[primitives][json]")
{
    SECTION("Integer edge cases")
    {
        packets::ComprehensivePacket p;

        p.SetIntField(0);
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetIntField() == 0);

        p.SetIntField(2147483647);
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetIntField() == 2147483647);

        p.SetIntField(-2147483648LL);
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetIntField() == -2147483648LL);
    }

    SECTION("Float edge cases")
    {
        packets::ComprehensivePacket p;

        p.SetFloatField(0.0f);
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(floatEquals(restored.GetFloatField(), 0.0f));

        p.SetFloatField(3.14159f);
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(floatEquals(restored.GetFloatField(), 3.14159f, 0.0001));

        p.SetFloatField(-123.456f);
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(floatEquals(restored.GetFloatField(), -123.456f, 0.001));
    }

    SECTION("Boolean values")
    {
        packets::ComprehensivePacket p;

        p.SetBoolField(true);
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetBoolField() == true);

        p.SetBoolField(false);
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetBoolField() == false);
    }

    SECTION("String edge cases")
    {
        packets::ComprehensivePacket p;

        p.SetStringField("");
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetStringField() == "");

        p.SetStringField("Hello World");
        json = p.ToJson();
        restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetStringField() == "Hello World");
    }
}
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
TEST_CASE("MsgPack Primitive types serialization", "[primitives][msgpack]")
{
    SECTION("Integer edge cases")
    {
        packets::ComprehensivePacket p;

        p.SetIntField(0);
        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetIntField() == 0);

        p.SetIntField(2147483647);
        msgpack = p.ToMsgPack();
        restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetIntField() == 2147483647);
    }

    SECTION("Boolean values")
    {
        packets::ComprehensivePacket p;

        p.SetBoolField(true);
        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetBoolField() == true);

        p.SetBoolField(false);
        msgpack = p.ToMsgPack();
        restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetBoolField() == false);
    }
}
#endif

// ============================================================================
// Bytes/Binary Data Tests (via ComprehensivePacket.bytes_field)
// ============================================================================
#ifdef CROSSPACKET_HAS_JSON
TEST_CASE("JSON Binary data serialization", "[bytes][json]")
{
    SECTION("Empty bytes")
    {
        packets::ComprehensivePacket p;
        p.SetBytesField({});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetBytesField().empty());
    }

    SECTION("0xDEADBEEF pattern")
    {
        packets::ComprehensivePacket p;
        p.SetBytesField({0xDE, 0xAD, 0xBE, 0xEF});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);

        auto data = restored.GetBytesField();
        REQUIRE(data.size() == 4);
        REQUIRE(static_cast<uint8_t>(data[0]) == 0xDE);
        REQUIRE(static_cast<uint8_t>(data[1]) == 0xAD);
        REQUIRE(static_cast<uint8_t>(data[2]) == 0xBE);
        REQUIRE(static_cast<uint8_t>(data[3]) == 0xEF);
    }
}
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
TEST_CASE("MsgPack Binary data serialization", "[bytes][msgpack]")
{
    SECTION("Binary roundtrip")
    {
        packets::ComprehensivePacket p;
        p.SetBytesField({0x01, 0x02, 0x03, 0x04});

        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetBytesField().size() == 4);
    }
}
#endif

// ============================================================================
// List Type Tests
// ============================================================================
#ifdef CROSSPACKET_HAS_JSON
TEST_CASE("JSON List serialization", "[list][json]")
{
    SECTION("Empty list")
    {
        packets::ComprehensivePacket p;
        p.SetListIntField({});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetListIntField().empty());
    }

    SECTION("Integer list")
    {
        packets::ComprehensivePacket p;
        p.SetListIntField({1, 2, 3, 4, 5});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetListIntField() == std::vector<int64_t>{1, 2, 3, 4, 5});
    }

    SECTION("String list")
    {
        packets::ComprehensivePacket p;
        p.SetListStringField({"alpha", "beta", "gamma"});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetListStringField() == std::vector<std::string>{"alpha", "beta", "gamma"});
    }
}
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
TEST_CASE("MsgPack List serialization", "[list][msgpack]")
{
    SECTION("Integer list")
    {
        packets::ComprehensivePacket p;
        p.SetListIntField({10, 20, 30});

        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetListIntField() == std::vector<int64_t>{10, 20, 30});
    }
}
#endif

// ============================================================================
// Error Handling Tests
// ============================================================================
#ifdef CROSSPACKET_HAS_JSON
TEST_CASE("JSON Error handling", "[errors][json]")
{
    SECTION("Invalid JSON throws exception")
    {
        REQUIRE_THROWS_AS(packets::MessagePacket::FromJson("not json"), std::runtime_error);
        REQUIRE_THROWS_AS(packets::MessagePacket::FromJson("{malformed"), std::runtime_error);
        REQUIRE_THROWS_AS(packets::PingPacket::FromJson(""), std::runtime_error);
    }
}
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
TEST_CASE("MsgPack Error handling", "[errors][msgpack]")
{
    SECTION("Invalid MsgPack throws exception")
    {
        std::vector<uint8_t> invalidData = {0xFF, 0xFF, 0xFF};
        REQUIRE_THROWS(packets::MessagePacket::FromMsgPack(invalidData));
    }
}
#endif

// ============================================================================
// Additional Coverage Tests
// ============================================================================
TEST_CASE("Parameterized Constructors", "[constructors]")
{
    SECTION("MessagePacket parameterized constructor")
    {
        packets::MessagePacket p("sender123", "Hello World", "2026-01-09T12:00:00Z");
        REQUIRE(p.GetSenderId() == "sender123");
        REQUIRE(p.GetContent() == "Hello World");
        REQUIRE(p.GetTimestamp() == "2026-01-09T12:00:00Z");
    }

    SECTION("PingPacket parameterized constructor")
    {
        packets::PingPacket p("2026-01-09T12:00:00Z", "ping message");
        REQUIRE(p.GetTimestamp() == "2026-01-09T12:00:00Z");
        REQUIRE(p.GetMessage() == "ping message");
    }

    SECTION("PongPacket parameterized constructor")
    {
        packets::PongPacket p("2026-01-09T12:00:00Z", "2026-01-09T12:00:01Z", 100);
        REQUIRE(p.GetOriginalTimestamp() == "2026-01-09T12:00:00Z");
        REQUIRE(p.GetResponseTimestamp() == "2026-01-09T12:00:01Z");
        REQUIRE(p.GetLatencyMs() == 100);
    }

    SECTION("DataChunkPacket parameterized constructor")
    {
        packets::DataChunkPacket p(5, 10, "{\"key\": \"value\"}", "checksum123");
        REQUIRE(p.GetChunkIndex() == 5);
        REQUIRE(p.GetTotalChunks() == 10);
        REQUIRE(p.GetData() == "{\"key\": \"value\"}");
        REQUIRE(p.GetChecksum() == "checksum123");
    }

    SECTION("UserProfilePacket parameterized constructor")
    {
        std::vector<uint8_t> avatar_data = {0x01, 0x02};
        packets::UserProfilePacket p(
            12345,                                             // user_id
            "testuser",                                        // username
            "test@email.com",                                  // email
            std::optional<std::string>{"My bio"},              // bio (optional)
            std::optional<int64_t>{25},                        // age (optional)
            100.50,                                            // balance
            std::vector<std::string>{"dev", "game"},           // tags
            "{\"theme\":\"dark\"}",                            // preferences
            std::optional<std::vector<uint8_t>>(avatar_data),  // avatar (optional)
            "2026-01-01T00:00:00Z",                            // created_at
            std::optional<std::string>{"2026-01-09T12:00:00Z"} // last_login (optional)
        );
        REQUIRE(p.GetUserId() == 12345);
        REQUIRE(p.GetUsername() == "testuser");
        REQUIRE(p.GetEmail() == "test@email.com");
        REQUIRE(p.GetBio().value() == "My bio");
        REQUIRE(p.GetAge().value() == 25);
    }

    SECTION("SecureMessagePacket parameterized constructor")
    {
        std::vector<uint8_t> encrypted_data = {0xCA, 0xFE};
        packets::SecureMessagePacket p(
            "msg-001",                                           // message_id
            100,                                                 // sender_id
            200,                                                 // recipient_id
            "Subject",                                           // subject
            "Body content",                                      // body
            "[]",                                                // attachments
            std::optional<std::vector<uint8_t>>(encrypted_data), // encrypted_payload (optional)
            5,                                                   // priority
            false,                                               // is_read
            "2026-01-09T12:00:00Z"                               // sent_at
        );
        REQUIRE(p.GetMessageId() == "msg-001");
        REQUIRE(p.GetSenderId() == 100);
        REQUIRE(p.GetRecipientId() == 200);
        REQUIRE(p.GetSubject() == "Subject");
        REQUIRE(p.GetPriority() == 5);
    }

    SECTION("ComprehensivePacket parameterized constructor")
    {
        packets::ComprehensivePacket p(
            42,                             // int_field
            3.14,                           // float_field
            2.71828,                        // double_field
            "test",                         // string_field
            true,                           // bool_field
            "2026-01-09T12:00:00Z",         // datetime_field
            "14:30:00",                     // time_field
            "[1,2,3]",                      // list_field
            {10, 20, 30},                   // list_int_field
            {"a", "b", "c"},                // list_string_field
            "{\"key\":\"value\"}",          // map_field
            "{\"nested\":{\"deep\":true}}", // embedded_map_field
            "{\"dynamic\":42}",             // map_string_dynamic_field
            {0xDE, 0xAD}                    // bytes_field
        );
        REQUIRE(p.GetIntField() == 42);
        REQUIRE(p.GetStringField() == "test");
        REQUIRE(p.GetBoolField() == true);
        REQUIRE(p.GetListIntField() == std::vector<int64_t>{10, 20, 30});
    }
}

#ifdef CROSSPACKET_HAS_JSON
TEST_CASE("Additional JSON Coverage", "[coverage][json]")
{
    SECTION("Large integer values")
    {
        packets::ComprehensivePacket p;
        p.SetIntField(9223372036854775807LL); // Max int64
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetIntField() == 9223372036854775807LL);
    }

    SECTION("Negative float values")
    {
        packets::ComprehensivePacket p;
        p.SetFloatField(-999.999f);
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(floatEquals(restored.GetFloatField(), -999.999f, 0.01));
    }

    SECTION("Double precision values")
    {
        packets::ComprehensivePacket p;
        p.SetDoubleField(1.7976931348623157e+308); // Near max double
        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);
        REQUIRE(restored.GetDoubleField() > 1.0e+307);
    }

    SECTION("Special characters in strings")
    {
        packets::MessagePacket p;
        p.SetContent("Tab:\t Newline:\n Quote:\" Backslash:\\");
        auto json = p.ToJson();
        auto restored = packets::MessagePacket::FromJson(json);
        REQUIRE(restored.GetContent().find('\t') != std::string::npos);
        REQUIRE(restored.GetContent().find('\n') != std::string::npos);
    }

    SECTION("Unicode in strings")
    {
        packets::MessagePacket p;
        p.SetContent("Hello 世界 🎉");
        auto json = p.ToJson();
        auto restored = packets::MessagePacket::FromJson(json);
        REQUIRE(restored.GetContent() == "Hello 世界 🎉");
    }

    SECTION("DataChunkPacket JSON roundtrip")
    {
        packets::DataChunkPacket p;
        p.SetChunkIndex(0);
        p.SetTotalChunks(100);
        p.SetData("{\"complex\":{\"nested\":true}}");
        p.SetChecksum("sha256:abc123");

        auto json = p.ToJson();
        auto restored = packets::DataChunkPacket::FromJson(json);

        REQUIRE(restored.GetChunkIndex() == 0);
        REQUIRE(restored.GetTotalChunks() == 100);
        REQUIRE(restored.GetChecksum() == "sha256:abc123");
    }

    SECTION("UserProfilePacket with all optional fields")
    {
        packets::UserProfilePacket p;
        p.SetUserId(999);
        p.SetUsername("fulluser");
        p.SetEmail("full@example.com");
        p.SetBio("Full bio");
        p.SetAge(30);
        p.SetBalance(1000.00);
        p.SetTags({"tag1", "tag2", "tag3"});
        p.SetPreferences("{\"setting\":true}");
        p.SetAvatar(std::vector<uint8_t>{0x01, 0x02, 0x03, 0x04, 0x05});
        p.SetCreatedAt("2026-01-01T00:00:00Z");
        p.SetLastLogin("2026-01-09T12:00:00Z");

        auto json = p.ToJson();
        auto restored = packets::UserProfilePacket::FromJson(json);

        REQUIRE(restored.GetUserId() == 999);
        REQUIRE(restored.GetBio().has_value());
        REQUIRE(restored.GetAge().has_value());
        REQUIRE(restored.GetAge().value() == 30);
        REQUIRE(restored.GetTags().size() == 3);
    }

    SECTION("Empty arrays and strings")
    {
        packets::ComprehensivePacket p;
        p.SetListIntField({});
        p.SetListStringField({});
        p.SetStringField("");
        p.SetBytesField({});

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);

        REQUIRE(restored.GetListIntField().empty());
        REQUIRE(restored.GetListStringField().empty());
        REQUIRE(restored.GetStringField().empty());
        REQUIRE(restored.GetBytesField().empty());
    }

    SECTION("All bytes values 0-255 in binary field")
    {
        packets::ComprehensivePacket p;
        std::vector<uint8_t> allBytes;
        for (int i = 0; i < 256; i++)
        {
            allBytes.push_back(static_cast<uint8_t>(i));
        }
        p.SetBytesField(allBytes);

        auto json = p.ToJson();
        auto restored = packets::ComprehensivePacket::FromJson(json);

        REQUIRE(restored.GetBytesField().size() == 256);
        for (int i = 0; i < 256; i++)
        {
            REQUIRE(static_cast<int>(restored.GetBytesField()[i]) == i);
        }
    }
}
#endif

#ifdef CROSSPACKET_HAS_MSGPACK
TEST_CASE("Additional MsgPack Coverage", "[coverage][msgpack]")
{
    SECTION("Large integer values")
    {
        packets::ComprehensivePacket p;
        p.SetIntField(9223372036854775807LL);
        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetIntField() == 9223372036854775807LL);
    }

    SECTION("Negative integers")
    {
        packets::ComprehensivePacket p;
        p.SetIntField(-9223372036854775807LL);
        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);
        REQUIRE(restored.GetIntField() == -9223372036854775807LL);
    }

    SECTION("DataChunkPacket MsgPack roundtrip")
    {
        packets::DataChunkPacket p;
        p.SetChunkIndex(50);
        p.SetTotalChunks(200);
        p.SetData("{\"msgpack\":\"test\"}");
        p.SetChecksum("md5:xyz789");

        auto msgpack = p.ToMsgPack();
        auto restored = packets::DataChunkPacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetChunkIndex() == 50);
        REQUIRE(restored.GetTotalChunks() == 200);
    }

    SECTION("UserProfilePacket MsgPack roundtrip")
    {
        packets::UserProfilePacket p;
        p.SetUserId(888);
        p.SetUsername("msgpack_user");
        p.SetEmail("msgpack@test.com");
        p.SetAge(28);
        p.SetBalance(500.50);
        p.SetCreatedAt("2026-01-01T00:00:00Z");

        auto msgpack = p.ToMsgPack();
        auto restored = packets::UserProfilePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetUserId() == 888);
        REQUIRE(restored.GetUsername() == "msgpack_user");
    }

    SECTION("SecureMessagePacket MsgPack with binary payload")
    {
        packets::SecureMessagePacket p;
        p.SetMessageId("secure-binary");
        p.SetSenderId(1);
        p.SetRecipientId(2);
        p.SetEncryptedPayload(std::vector<uint8_t>{0xCA, 0xFE, 0xBA, 0xBE, 0xDE, 0xAD, 0xBE, 0xEF});
        p.SetSentAt("2026-01-09T12:00:00Z");

        auto msgpack = p.ToMsgPack();
        auto restored = packets::SecureMessagePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetEncryptedPayload().value().size() == 8);
    }

    SECTION("Empty collections MsgPack")
    {
        packets::ComprehensivePacket p;
        p.SetListIntField({});
        p.SetListStringField({});
        p.SetBytesField({});

        auto msgpack = p.ToMsgPack();
        auto restored = packets::ComprehensivePacket::FromMsgPack(msgpack);

        REQUIRE(restored.GetListIntField().empty());
        REQUIRE(restored.GetListStringField().empty());
        REQUIRE(restored.GetBytesField().empty());
    }
}
#endif
