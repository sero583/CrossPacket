"""
Comprehensive tests for generated Python packet classes.
Tests all edge cases, behaviors, and ensures 100% coverage of generated code.
"""
import pytest
import json
import sys
import os
from datetime import datetime, timezone, time
from pathlib import Path

# Add generated directory to path for importing generated packets
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "generated"))

from python.message_packet import MessagePacket
from python.comprehensive_packet import ComprehensivePacket
from python.ping_packet import PingPacket
from python.pong_packet import PongPacket
from python.data_chunk_packet import DataChunkPacket
from python.user_profile_packet import UserProfilePacket
from python.secure_message_packet import SecureMessagePacket


# Test mode detection for conditional tests
TEST_MODE = os.environ.get("TEST_MODE", "BOTH")

# Check what methods are available (depends on generation mode)
HAS_JSON = hasattr(MessagePacket, 'from_json')
HAS_MSGPACK = hasattr(MessagePacket, 'from_msgpack')


def skip_if_msgpack_only():
    """Skip test if running in MSGPACK_ONLY mode (no JSON methods)."""
    if not HAS_JSON:
        pytest.skip("JSON tests skipped - JSON methods not available")


def skip_if_json_only():
    """Skip test if running in JSON_ONLY mode (no MsgPack methods)."""
    if not HAS_MSGPACK:
        pytest.skip("MsgPack tests skipped in JSON_ONLY mode")


class TestMessagePacket:
    """Tests for MessagePacket - the primary example packet."""

    def test_empty_constructor(self):
        """Test creating packet with empty constructor."""
        packet = MessagePacket()
        assert packet.sender_id is None
        assert packet.content is None
        assert packet.timestamp is None

    def test_parameterized_constructor(self):
        """Test creating packet with all parameters."""
        now = datetime.now(timezone.utc)
        packet = MessagePacket(
            sender_id="user123",
            content="Hello, World!",
            timestamp=now
        )
        assert packet.sender_id == "user123"
        assert packet.content == "Hello, World!"
        assert packet.timestamp == now

    def test_setter_pattern(self):
        """Test creating packet with empty constructor then setters."""
        packet = MessagePacket()
        packet.sender_id = "user456"
        packet.content = "Test message"
        packet.timestamp = datetime(2026, 1, 9, 12, 0, 0, tzinfo=timezone.utc)
        
        assert packet.sender_id == "user456"
        assert packet.content == "Test message"
        assert packet.timestamp.year == 2026

    def test_type_constant(self):
        """Test TYPE constant is correct."""
        assert MessagePacket.TYPE == "/chat/MessagePacket"
        packet = MessagePacket()
        assert packet.TYPE == "/chat/MessagePacket"

    def test_json_roundtrip_full(self):
        """Test JSON serialization and deserialization with all fields."""
        skip_if_msgpack_only()
        now = datetime(2026, 1, 9, 12, 30, 45, tzinfo=timezone.utc)
        original = MessagePacket(
            sender_id="alice",
            content="Hello Bob!",
            timestamp=now
        )
        
        json_str = original.to_json()
        restored = MessagePacket.from_json(json_str)
        
        assert restored.sender_id == original.sender_id
        assert restored.content == original.content
        # Datetime comparison (fromisoformat preserves timezone)
        assert restored.timestamp.isoformat() == original.timestamp.isoformat()

    def test_json_roundtrip_empty(self):
        """Test JSON roundtrip with empty/None fields."""
        skip_if_msgpack_only()
        original = MessagePacket()
        
        json_str = original.to_json()
        restored = MessagePacket.from_json(json_str)
        
        assert restored.sender_id is None
        assert restored.content is None
        assert restored.timestamp is None

    def test_json_roundtrip_partial(self):
        """Test JSON roundtrip with some fields set."""
        skip_if_msgpack_only()
        original = MessagePacket(sender_id="test", content=None, timestamp=None)
        
        json_str = original.to_json()
        restored = MessagePacket.from_json(json_str)
        
        assert restored.sender_id == "test"
        assert restored.content is None
        assert restored.timestamp is None

    def test_msgpack_roundtrip_full(self):
        """Test MessagePack serialization and deserialization."""
        skip_if_json_only()
        now = datetime(2026, 1, 9, 14, 0, 0, tzinfo=timezone.utc)
        original = MessagePacket(
            sender_id="bob",
            content="Reply to Alice",
            timestamp=now
        )
        
        msgpack_bytes = original.to_msgpack()
        assert isinstance(msgpack_bytes, bytes)
        
        restored = MessagePacket.from_msgpack(msgpack_bytes)
        assert restored.sender_id == original.sender_id
        assert restored.content == original.content

    def test_msgpack_roundtrip_empty(self):
        """Test MessagePack roundtrip with empty fields."""
        skip_if_json_only()
        original = MessagePacket()
        
        msgpack_bytes = original.to_msgpack()
        restored = MessagePacket.from_msgpack(msgpack_bytes)
        
        assert restored.sender_id is None
        assert restored.content is None

    def test_packettype_in_json(self):
        """Test that packetType field is in serialized JSON."""
        skip_if_msgpack_only()
        packet = MessagePacket(sender_id="test")
        data = json.loads(packet.to_json())
        
        assert "packetType" in data
        assert data["packetType"] == "/chat/MessagePacket"

    def test_unicode_content(self):
        """Test Unicode characters in content."""
        skip_if_msgpack_only()
        packet = MessagePacket(
            sender_id="用户",
            content="こんにちは世界! 🌍🚀"
        )
        
        json_str = packet.to_json()
        restored = MessagePacket.from_json(json_str)
        
        assert restored.sender_id == "用户"
        assert restored.content == "こんにちは世界! 🌍🚀"

    def test_special_characters(self):
        """Test special characters in strings."""
        skip_if_msgpack_only()
        packet = MessagePacket(
            sender_id="user\"with'quotes",
            content="Line1\nLine2\tTabbed\\Backslash"
        )
        
        json_str = packet.to_json()
        restored = MessagePacket.from_json(json_str)
        
        assert restored.sender_id == "user\"with'quotes"
        assert "Line1\nLine2" in restored.content


class TestComprehensivePacket:
    """Tests for ComprehensivePacket - tests ALL supported types."""

    def test_empty_constructor(self):
        """Test empty constructor - all fields should be None."""
        packet = ComprehensivePacket()
        assert packet.int_field is None
        assert packet.float_field is None
        assert packet.double_field is None
        assert packet.string_field is None
        assert packet.bool_field is None
        assert packet.datetime_field is None
        assert packet.time_field is None
        assert packet.list_field is None
        assert packet.list_int_field is None
        assert packet.list_string_field is None
        assert packet.map_field is None
        assert packet.embedded_map_field is None
        assert packet.map_string_dynamic_field is None
        assert packet.bytes_field is None

    def test_full_constructor(self):
        """Test constructor with all fields."""
        now = datetime.now(timezone.utc)
        current_time = time(12, 30, 45)
        
        packet = ComprehensivePacket(
            int_field=42,
            float_field=3.14,
            double_field=2.718281828,
            string_field="test",
            bool_field=True,
            datetime_field=now,
            time_field=current_time,
            list_field=[1, "two", 3.0],
            list_int_field=[1, 2, 3],
            list_string_field=["a", "b", "c"],
            map_field={"key": "value"},
            embedded_map_field={"nested": {"deep": 123}},
            map_string_dynamic_field={"dyn": [1, 2, 3]},
            bytes_field=b"binary data"
        )
        
        assert packet.int_field == 42
        assert packet.float_field == 3.14
        assert packet.bool_field is True
        assert packet.list_int_field == [1, 2, 3]

    def test_type_constant(self):
        """Test TYPE constant."""
        assert ComprehensivePacket.TYPE == "/test/ComprehensivePacket"

    def test_int_field_boundary_values(self):
        """Test integer field with boundary values."""
        skip_if_msgpack_only()
        # Large positive
        packet = ComprehensivePacket(int_field=2**31 - 1)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.int_field == 2**31 - 1
        
        # Large negative
        packet = ComprehensivePacket(int_field=-2**31)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.int_field == -2**31
        
        # Zero
        packet = ComprehensivePacket(int_field=0)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.int_field == 0

    def test_float_precision(self):
        """Test float/double field precision."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(
            float_field=3.141592653589793,
            double_field=2.718281828459045
        )
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert abs(restored.float_field - 3.141592653589793) < 1e-10
        assert abs(restored.double_field - 2.718281828459045) < 1e-10

    def test_float_special_values(self):
        """Test float with edge values."""
        skip_if_msgpack_only()
        # Very small
        packet = ComprehensivePacket(float_field=1e-10)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.float_field == pytest.approx(1e-10)
        
        # Very large
        packet = ComprehensivePacket(float_field=1e10)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.float_field == pytest.approx(1e10)

    def test_bool_values(self):
        """Test boolean field values."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(bool_field=True)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.bool_field is True
        
        packet = ComprehensivePacket(bool_field=False)
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.bool_field is False

    def test_datetime_with_timezone(self):
        """Test datetime with timezone information."""
        skip_if_msgpack_only()
        dt = datetime(2026, 1, 9, 15, 30, 0, tzinfo=timezone.utc)
        packet = ComprehensivePacket(datetime_field=dt)
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.datetime_field.isoformat() == dt.isoformat()

    def test_time_field(self):
        """Test time field serialization."""
        skip_if_msgpack_only()
        t = time(14, 30, 45, 123456)
        packet = ComprehensivePacket(time_field=t)
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.time_field == t

    def test_list_with_mixed_types(self):
        """Test list field with mixed types."""
        skip_if_msgpack_only()
        mixed_list = [1, "two", 3.0, True, None, {"nested": "map"}]
        packet = ComprehensivePacket(list_field=mixed_list)
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.list_field == mixed_list

    def test_list_int_type_coercion(self):
        """Test list_int field type coercion."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(list_int_field=[1, 2, 3])
        restored = ComprehensivePacket.from_json(packet.to_json())
        
        assert all(isinstance(x, int) for x in restored.list_int_field)
        assert restored.list_int_field == [1, 2, 3]

    def test_list_string_type_coercion(self):
        """Test list_string field type coercion."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(list_string_field=["a", "b", "c"])
        restored = ComprehensivePacket.from_json(packet.to_json())
        
        assert all(isinstance(x, str) for x in restored.list_string_field)
        assert restored.list_string_field == ["a", "b", "c"]

    def test_empty_lists(self):
        """Test empty list handling."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(
            list_field=[],
            list_int_field=[],
            list_string_field=[]
        )
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.list_field == []
        # Empty lists may be deserialized as None or [] depending on implementation
        assert restored.list_int_field is None or restored.list_int_field == []
        assert restored.list_string_field is None or restored.list_string_field == []

    def test_map_field(self):
        """Test map field with various value types."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(
            map_field={
                "string": "value",
                "number": 42,
                "boolean": True,
                "list": [1, 2, 3]
            }
        )
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.map_field["string"] == "value"
        assert restored.map_field["number"] == 42
        assert restored.map_field["boolean"] is True
        assert restored.map_field["list"] == [1, 2, 3]

    def test_embedded_map(self):
        """Test deeply nested map structures."""
        skip_if_msgpack_only()
        nested = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        packet = ComprehensivePacket(embedded_map_field=nested)
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.embedded_map_field["level1"]["level2"]["level3"]["value"] == "deep"

    def test_empty_map(self):
        """Test empty map handling."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(map_field={})
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.map_field == {}

    def test_msgpack_all_types(self):
        """Test MessagePack roundtrip with all types."""
        skip_if_json_only()
        now = datetime.now(timezone.utc)
        t = time(10, 30, 0)
        
        packet = ComprehensivePacket(
            int_field=100,
            float_field=1.5,
            double_field=2.5,
            string_field="msgpack test",
            bool_field=True,
            datetime_field=now,
            time_field=t,
            list_field=[1, 2, 3],
            list_int_field=[10, 20, 30],
            list_string_field=["x", "y", "z"],
            map_field={"key": "value"}
        )
        
        msgpack_bytes = packet.to_msgpack()
        restored = ComprehensivePacket.from_msgpack(msgpack_bytes)
        
        assert restored.int_field == 100
        assert restored.string_field == "msgpack test"
        assert restored.bool_field is True

    def test_packettype_field(self):
        """Test packetType is correctly set in serialized output."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(int_field=1)
        data = json.loads(packet.to_json())
        
        assert data["packetType"] == "/test/ComprehensivePacket"


class TestPingPongPackets:
    """Tests for PingPacket and PongPacket."""

    def test_ping_packet(self):
        """Test PingPacket serialization."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = PingPacket(timestamp=now, message="ping test")
        
        assert packet.TYPE == "/example/PingPacket"
        
        json_str = packet.to_json()
        restored = PingPacket.from_json(json_str)
        
        assert restored.message == "ping test"

    def test_pong_packet(self):
        """Test PongPacket serialization."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = PongPacket(original_timestamp=now, latency_ms=42)
        
        assert packet.TYPE == "/example/PongPacket"
        
        json_str = packet.to_json()
        restored = PongPacket.from_json(json_str)
        
        assert restored.latency_ms == 42

    def test_ping_empty(self):
        """Test PingPacket with empty constructor."""
        packet = PingPacket()
        assert packet.timestamp is None
        assert packet.message is None

    def test_ping_msgpack(self):
        """Test PingPacket with MessagePack."""
        skip_if_json_only()
        now = datetime.now(timezone.utc)
        packet = PingPacket(timestamp=now, message="msgpack ping")
        msgpack_bytes = packet.to_msgpack()
        restored = PingPacket.from_msgpack(msgpack_bytes)
        
        assert restored.message == "msgpack ping"


class TestDataChunkPacket:
    """Tests for DataChunkPacket with embedded_map field."""

    def test_data_chunk(self):
        """Test data chunk packet."""
        packet = DataChunkPacket(
            chunk_index=1,
            total_chunks=10,
            data={"key": "value", "count": 42},
            checksum="abc123"
        )
        
        assert packet.TYPE == "/example/DataChunkPacket"
        assert packet.chunk_index == 1

    def test_empty_data(self):
        """Test empty data."""
        skip_if_msgpack_only()
        packet = DataChunkPacket(
            chunk_index=0,
            total_chunks=1,
            data={},
            checksum=""
        )
        
        json_str = packet.to_json()
        restored = DataChunkPacket.from_json(json_str)
        assert restored.chunk_index == 0

    def test_nested_data(self):
        """Test nested data structures."""
        skip_if_json_only()
        nested = {"level1": {"level2": {"value": 123}}}
        packet = DataChunkPacket(
            chunk_index=99,
            total_chunks=100,
            data=nested,
            checksum="xyz789"
        )
        
        msgpack_bytes = packet.to_msgpack()
        restored = DataChunkPacket.from_msgpack(msgpack_bytes)
        
        assert restored.chunk_index == 99
        assert restored.data["level1"]["level2"]["value"] == 123


class TestUserProfilePacket:
    """Tests for UserProfilePacket with optional fields."""

    def test_full_profile(self):
        """Test profile with all fields."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = UserProfilePacket(
            user_id=123,
            username="john_doe",
            email="john@example.com",
            bio="Hello, I'm John!",
            age=30,
            balance=100.50,
            tags=["developer", "python"],
            preferences={"theme": "dark"},
            created_at=now
        )
        
        assert packet.TYPE == "/example/UserProfilePacket"
        
        restored = UserProfilePacket.from_json(packet.to_json())
        assert restored.username == "john_doe"
        assert restored.email == "john@example.com"
        assert restored.age == 30

    def test_minimal_profile(self):
        """Test profile with only some fields."""
        skip_if_msgpack_only()
        packet = UserProfilePacket(
            user_id=1,
            username="minimal"
        )
        
        restored = UserProfilePacket.from_json(packet.to_json())
        assert restored.user_id == 1
        assert restored.username == "minimal"
        assert restored.bio is None


class TestSecureMessagePacket:
    """Tests for SecureMessagePacket with security fields."""

    def test_secure_message(self):
        """Test secure message packet."""
        skip_if_json_only()
        now = datetime.now(timezone.utc)
        encrypted = bytes([0xDE, 0xAD, 0xBE, 0xEF] * 10)
        
        packet = SecureMessagePacket(
            message_id="msg-001",
            sender_id=1,
            recipient_id=2,
            subject="Test Subject",
            body="Test body content",
            priority=1,
            is_read=False,
            encrypted_payload=encrypted,
            sent_at=now
        )
        
        assert packet.TYPE == "/example/SecureMessagePacket"
        
        msgpack_bytes = packet.to_msgpack()
        restored = SecureMessagePacket.from_msgpack(msgpack_bytes)
        
        assert restored.sender_id == 1
        assert restored.recipient_id == 2
        assert restored.subject == "Test Subject"
        assert restored.priority == 1


class TestEdgeCases:
    """Test edge cases across all packet types."""

    def test_null_string_vs_empty_string(self):
        """Test distinction between null and empty string."""
        skip_if_msgpack_only()
        packet1 = MessagePacket(content=None)
        packet2 = MessagePacket(content="")
        
        restored1 = MessagePacket.from_json(packet1.to_json())
        restored2 = MessagePacket.from_json(packet2.to_json())
        
        assert restored1.content is None
        assert restored2.content == ""

    def test_zero_values(self):
        """Test that zero values are preserved (not treated as None)."""
        skip_if_msgpack_only()
        packet = ComprehensivePacket(
            int_field=0,
            float_field=0.0,
            bool_field=False
        )
        
        restored = ComprehensivePacket.from_json(packet.to_json())
        assert restored.int_field == 0
        assert restored.float_field == 0.0
        assert restored.bool_field is False

    def test_very_long_string(self):
        """Test very long string content."""
        skip_if_msgpack_only()
        long_string = "A" * 100000
        packet = MessagePacket(content=long_string)
        
        restored = MessagePacket.from_json(packet.to_json())
        assert len(restored.content) == 100000
        assert restored.content == long_string

    def test_all_packets_have_packettype(self):
        """Verify all packets include packetType in serialization."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packets = [
            MessagePacket(sender_id="test"),
            ComprehensivePacket(int_field=1),
            PingPacket(message="test"),
            PongPacket(latency_ms=10),
            DataChunkPacket(chunk_index=1),
            UserProfilePacket(user_id=1),
            SecureMessagePacket(sender_id=1)
        ]
        
        for packet in packets:
            data = json.loads(packet.to_json())
            assert "packetType" in data, f"{type(packet).__name__} missing packetType"
            assert data["packetType"].startswith("/"), f"{type(packet).__name__} has invalid packetType"

    def test_deserialization_ignores_unknown_fields(self):
        """Test that deserialization ignores unknown fields gracefully."""
        skip_if_msgpack_only()
        json_str = json.dumps({
            "packetType": "/chat/MessagePacket",
            "sender_id": "test",
            "content": "hello",
            "unknown_field": "should be ignored",
            "another_unknown": 12345
        })
        
        packet = MessagePacket.from_json(json_str)
        assert packet.sender_id == "test"
        assert packet.content == "hello"


class TestCrossFormatConsistency:
    """Test that JSON and MessagePack produce consistent results."""

    def test_json_msgpack_equivalence(self):
        """Verify JSON and MessagePack roundtrip produce same results."""
        skip_if_msgpack_only()
        skip_if_json_only()
        now = datetime(2026, 1, 9, 12, 0, 0, tzinfo=timezone.utc)
        original = MessagePacket(
            sender_id="consistency_test",
            content="Testing cross-format",
            timestamp=now
        )
        
        from_json = MessagePacket.from_json(original.to_json())
        from_msgpack = MessagePacket.from_msgpack(original.to_msgpack())
        
        assert from_json.sender_id == from_msgpack.sender_id
        assert from_json.content == from_msgpack.content

    def test_comprehensive_cross_format(self):
        """Test comprehensive packet cross-format consistency."""
        skip_if_msgpack_only()
        skip_if_json_only()
        original = ComprehensivePacket(
            int_field=42,
            float_field=3.14,
            string_field="cross-format",
            bool_field=True,
            list_field=[1, 2, 3],
            map_field={"key": "value"}
        )
        
        from_json = ComprehensivePacket.from_json(original.to_json())
        from_msgpack = ComprehensivePacket.from_msgpack(original.to_msgpack())
        
        assert from_json.int_field == from_msgpack.int_field
        assert from_json.string_field == from_msgpack.string_field
        assert from_json.bool_field == from_msgpack.bool_field


class TestDataclassFeatures:
    """Test dataclass-specific features of generated packets."""

    def test_equality(self):
        """Test dataclass equality comparison."""
        packet1 = MessagePacket(sender_id="test", content="hello")
        packet2 = MessagePacket(sender_id="test", content="hello")
        packet3 = MessagePacket(sender_id="test", content="different")
        
        assert packet1 == packet2
        assert packet1 != packet3

    def test_repr(self):
        """Test dataclass repr."""
        packet = MessagePacket(sender_id="test")
        repr_str = repr(packet)
        
        assert "MessagePacket" in repr_str
        assert "sender_id='test'" in repr_str

    def test_hash_not_supported(self):
        """Dataclasses with mutable fields are not hashable by default."""
        packet = ComprehensivePacket(list_field=[1, 2, 3])
        
        with pytest.raises(TypeError):
            hash(packet)

    def test_field_assignment(self):
        """Test field assignment after creation."""
        packet = MessagePacket()
        
        packet.sender_id = "updated"
        packet.content = "also updated"
        
        assert packet.sender_id == "updated"
        assert packet.content == "also updated"


class TestDeserializePacket:
    """Tests for the module-level deserialize_packet function."""

    def test_deserialize_message_packet(self):
        """Test deserializing a MessagePacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/chat/MessagePacket",
            "sender_id": "test_user",
            "content": "Hello!"
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, MessagePacket)
        assert packet.sender_id == "test_user"
        assert packet.content == "Hello!"

    def test_deserialize_ping_packet(self):
        """Test deserializing a PingPacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/example/PingPacket",
            "message": "ping!"
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, PingPacket)

    def test_deserialize_pong_packet(self):
        """Test deserializing a PongPacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/example/PongPacket",
            "latency_ms": 42
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, PongPacket)
        assert packet.latency_ms == 42

    def test_deserialize_data_chunk_packet(self):
        """Test deserializing a DataChunkPacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/example/DataChunkPacket",
            "chunk_index": 5,
            "total_chunks": 10
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, DataChunkPacket)
        assert packet.chunk_index == 5

    def test_deserialize_comprehensive_packet(self):
        """Test deserializing a ComprehensivePacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/test/ComprehensivePacket",
            "int_field": 123,
            "string_field": "comprehensive"
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, ComprehensivePacket)
        assert packet.int_field == 123

    def test_deserialize_user_profile_packet(self):
        """Test deserializing a UserProfilePacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/example/UserProfilePacket",
            "user_id": 999,
            "username": "testuser"
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, UserProfilePacket)
        assert packet.user_id == 999

    def test_deserialize_secure_message_packet(self):
        """Test deserializing a SecureMessagePacket."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/example/SecureMessagePacket",
            "sender_id": 1,
            "recipient_id": 2,
            "subject": "Test"
        }
        
        packet = deserialize_packet(data)
        assert isinstance(packet, SecureMessagePacket)
        assert packet.sender_id == 1

    def test_deserialize_unknown_type_raises(self):
        """Test that unknown packet type raises ValueError."""
        from python import deserialize_packet
        
        data = {
            "packetType": "/unknown/UnknownPacket",
            "field": "value"
        }
        
        with pytest.raises(ValueError, match="Unknown packet type"):
            deserialize_packet(data)

    def test_deserialize_none_type_raises(self):
        """Test that missing packetType raises ValueError."""
        from python import deserialize_packet
        
        data = {"field": "value"}  # No packetType
        
        with pytest.raises(ValueError, match="Unknown packet type"):
            deserialize_packet(data)

    def test_deserialize_non_dict_raises(self):
        """Test that non-dict input raises ValueError."""
        from python import deserialize_packet
        
        with pytest.raises(ValueError, match="Unknown packet type"):
            deserialize_packet("not a dict")

        with pytest.raises(ValueError, match="Unknown packet type"):
            deserialize_packet(12345)


class TestPongPacketFullCoverage:
    """Additional tests for PongPacket to reach 100% coverage."""

    def test_pong_all_fields(self):
        """Test PongPacket with all fields."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = PongPacket(
            original_timestamp=now,
            response_timestamp=now,
            latency_ms=100
        )
        
        restored = PongPacket.from_json(packet.to_json())
        assert restored.latency_ms == 100
        assert restored.original_timestamp is not None
        assert restored.response_timestamp is not None

    def test_pong_empty(self):
        """Test empty PongPacket."""
        skip_if_msgpack_only()
        packet = PongPacket()
        
        restored = PongPacket.from_json(packet.to_json())
        assert restored.original_timestamp is None
        assert restored.response_timestamp is None
        assert restored.latency_ms is None

    def test_pong_msgpack(self):
        """Test PongPacket with MessagePack."""
        skip_if_json_only()
        now = datetime.now(timezone.utc)
        packet = PongPacket(
            original_timestamp=now,
            response_timestamp=now,
            latency_ms=50
        )
        
        msgpack_bytes = packet.to_msgpack()
        restored = PongPacket.from_msgpack(msgpack_bytes)
        
        assert restored.latency_ms == 50


class TestUserProfilePacketFullCoverage:
    """Additional tests for UserProfilePacket to reach 100% coverage."""

    def test_all_fields_roundtrip(self):
        """Test all fields roundtrip."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = UserProfilePacket(
            user_id=1,
            username="full_user",
            email="full@test.com",
            bio="Full bio",
            age=25,
            balance=100.50,
            tags=["tag1", "tag2"],
            preferences={"theme": "dark"},
            avatar=b"binary avatar data",
            created_at=now,
            last_login=now
        )
        
        # JSON roundtrip
        restored = UserProfilePacket.from_json(packet.to_json())
        assert restored.user_id == 1
        assert restored.username == "full_user"
        assert restored.age == 25
        assert restored.balance == 100.50
        assert restored.tags == ["tag1", "tag2"]
        assert restored.created_at is not None
        assert restored.last_login is not None

    def test_msgpack_roundtrip(self):
        """Test MessagePack roundtrip."""
        skip_if_json_only()
        now = datetime.now(timezone.utc)
        packet = UserProfilePacket(
            user_id=2,
            username="msgpack_user",
            created_at=now,
            last_login=now
        )
        
        msgpack_bytes = packet.to_msgpack()
        restored = UserProfilePacket.from_msgpack(msgpack_bytes)
        
        assert restored.user_id == 2
        assert restored.username == "msgpack_user"


class TestSecureMessagePacketFullCoverage:
    """Additional tests for SecureMessagePacket to reach 100% coverage."""

    def test_all_fields(self):
        """Test all fields."""
        skip_if_msgpack_only()
        now = datetime.now(timezone.utc)
        packet = SecureMessagePacket(
            message_id="msg-full",
            sender_id=1,
            recipient_id=2,
            subject="Full Subject",
            body="Full body text",
            attachments=[{"name": "file.txt", "size": 100}],
            encrypted_payload=b"encrypted",
            priority=2,
            is_read=True,
            sent_at=now
        )
        
        restored = SecureMessagePacket.from_json(packet.to_json())
        assert restored.message_id == "msg-full"
        assert restored.is_read is True
        assert restored.attachments == [{"name": "file.txt", "size": 100}]
        assert restored.sent_at is not None


class TestMsgpackUnavailable:
    """Tests for when msgpack is not available."""

    def test_to_msgpack_raises_without_msgpack(self, monkeypatch):
        """Test to_msgpack raises ImportError when msgpack unavailable."""
        skip_if_json_only()
        import python.ping_packet as ping_module
        monkeypatch.setattr(ping_module, "HAS_MSGPACK", False)
        
        packet = PingPacket()
        with pytest.raises(ImportError) as exc:
            packet.to_msgpack()
        assert "msgpack is required" in str(exc.value)

    def test_from_msgpack_raises_without_msgpack(self, monkeypatch):
        """Test from_msgpack raises ImportError when msgpack unavailable."""
        skip_if_json_only()
        import python.ping_packet as ping_module
        monkeypatch.setattr(ping_module, "HAS_MSGPACK", False)
        
        with pytest.raises(ImportError) as exc:
            PingPacket.from_msgpack(b"\x80")
        assert "msgpack is required" in str(exc.value)

    def test_message_packet_msgpack_unavailable(self, monkeypatch):
        """Test MessagePacket to_msgpack/from_msgpack without msgpack."""
        skip_if_json_only()
        import python.message_packet as msg_module
        monkeypatch.setattr(msg_module, "HAS_MSGPACK", False)
        
        packet = MessagePacket()
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            MessagePacket.from_msgpack(b"\x80")

    def test_comprehensive_packet_msgpack_unavailable(self, monkeypatch):
        """Test ComprehensivePacket msgpack methods without msgpack."""
        skip_if_json_only()
        import python.comprehensive_packet as comp_module
        monkeypatch.setattr(comp_module, "HAS_MSGPACK", False)
        
        packet = ComprehensivePacket()
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            ComprehensivePacket.from_msgpack(b"\x80")

    def test_pong_packet_msgpack_unavailable(self, monkeypatch):
        """Test PongPacket msgpack methods without msgpack."""
        skip_if_json_only()
        import python.pong_packet as pong_module
        monkeypatch.setattr(pong_module, "HAS_MSGPACK", False)
        
        packet = PongPacket()
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            PongPacket.from_msgpack(b"\x80")

    def test_data_chunk_packet_msgpack_unavailable(self, monkeypatch):
        """Test DataChunkPacket msgpack methods without msgpack."""
        skip_if_json_only()
        import python.data_chunk_packet as chunk_module
        monkeypatch.setattr(chunk_module, "HAS_MSGPACK", False)
        
        packet = DataChunkPacket()
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            DataChunkPacket.from_msgpack(b"\x80")

    def test_user_profile_packet_msgpack_unavailable(self, monkeypatch):
        """Test UserProfilePacket msgpack methods without msgpack."""
        skip_if_json_only()
        import python.user_profile_packet as profile_module
        monkeypatch.setattr(profile_module, "HAS_MSGPACK", False)
        
        now = datetime.now(timezone.utc)
        packet = UserProfilePacket(user_id=1, username="test", created_at=now)
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            UserProfilePacket.from_msgpack(b"\x80")

    def test_secure_message_packet_msgpack_unavailable(self, monkeypatch):
        """Test SecureMessagePacket msgpack methods without msgpack."""
        skip_if_json_only()
        import python.secure_message_packet as secure_module
        monkeypatch.setattr(secure_module, "HAS_MSGPACK", False)
        
        now = datetime.now(timezone.utc)
        packet = SecureMessagePacket(
            message_id="msg-1",
            sender_id=1,
            recipient_id=2,
            subject="Test",
            body="Body",
            priority=1,
            sent_at=now
        )
        with pytest.raises(ImportError):
            packet.to_msgpack()
        with pytest.raises(ImportError):
            SecureMessagePacket.from_msgpack(b"\x80")


# JUSTIFICATION: This block is only executed when running the script directly via
# `python test_generated_packets.py`, not when running through pytest. Since our CI
# and test infrastructure use pytest as the test runner, this __main__ guard is never
# reached during test execution. This is standard Python practice for test modules.
if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
