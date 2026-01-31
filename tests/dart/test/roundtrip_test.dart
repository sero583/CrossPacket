// CrossPacket - Roundtrip Deserialization Tests (BOTH mode only)
//
// Author: Serhat Güler (sero583)
// GitHub: https://github.com/sero583
// License: MIT
//
// This test file contains roundtrip serialization/deserialization tests.
// It ONLY runs in BOTH mode because it requires both JSON and MsgPack methods
// to exist at compile time.
//
// Run: TEST_MODE=BOTH dart test test/roundtrip_test.dart

import 'dart:typed_data';
import 'dart:io' show Platform;
import 'package:test/test.dart';

// Import generated packets from lib (using package import for coverage)
import 'package:crosspacket_tests/generated/ping_packet.dart';
import 'package:crosspacket_tests/generated/pong_packet.dart';
import 'package:crosspacket_tests/generated/message_packet.dart';
import 'package:crosspacket_tests/generated/data_chunk_packet.dart';
import 'package:crosspacket_tests/generated/user_profile_packet.dart';
import 'package:crosspacket_tests/generated/secure_message_packet.dart';
import 'package:crosspacket_tests/generated/comprehensive_packet.dart';
import 'package:crosspacket_tests/data_packet.dart';

void main() {
  // This file requires BOTH mode - all methods must exist at compile time
  final testMode = Platform.environment['TEST_MODE'] ?? 'BOTH';
  
  if (testMode != 'BOTH') {
    // Skip all tests if not in BOTH mode - this file won't even compile
    // in single-mode builds, so CI should not run this file at all.
    test('Roundtrip tests require BOTH mode', () {
      print('Skipping roundtrip tests - TEST_MODE=$testMode requires BOTH mode');
    }, skip: 'Roundtrip tests only run in BOTH mode');
    return;
  }

  // ============================================================================
  // Deserialization Roundtrip Tests (for higher coverage)
  // These tests directly call the static fromJson/fromMsgPack methods
  // ============================================================================
  group('Deserialization Roundtrips', () {
    // --------------------------------------------------------------------------
    // PingPacket Roundtrips
    // --------------------------------------------------------------------------
    test('PingPacket JSON roundtrip', () {
      final original = PingPacket.create(
        timestamp: DateTime.parse('2024-06-15T12:30:45.000Z'),
        message: 'roundtrip test',
      );
      final json = original.toJson();
      final restored = PingPacket.fromJson(json);
      expect(restored.message, equals(original.message));
    });

    test('PingPacket MsgPack roundtrip', () {
      final original = PingPacket.create(
        timestamp: DateTime.now(),
        message: 'msgpack roundtrip',
      );
      final bytes = original.toMsgPack();
      final restored = PingPacket.fromMsgPack(bytes);
      expect(restored.message, equals(original.message));
    });

    // --------------------------------------------------------------------------
    // PongPacket Roundtrips
    // --------------------------------------------------------------------------
    test('PongPacket JSON roundtrip', () {
      final original = PongPacket.create(
        original_timestamp: DateTime.parse('2024-06-15T12:30:45.000Z'),
        response_timestamp: DateTime.parse('2024-06-15T12:30:45.050Z'),
        latency_ms: 50,
      );
      final json = original.toJson();
      final restored = PongPacket.fromJson(json);
      expect(restored.latency_ms, equals(50));
    });

    test('PongPacket MsgPack roundtrip', () {
      final original = PongPacket.create(
        original_timestamp: DateTime.now(),
        response_timestamp: DateTime.now(),
        latency_ms: 100,
      );
      final bytes = original.toMsgPack();
      final restored = PongPacket.fromMsgPack(bytes);
      expect(restored.latency_ms, equals(100));
    });

    // --------------------------------------------------------------------------
    // MessagePacket Roundtrips
    // --------------------------------------------------------------------------
    test('MessagePacket JSON roundtrip', () {
      final original = MessagePacket.create(
        sender_id: 'user123',
        content: 'Hello World!',
        timestamp: DateTime.now(),
      );
      final json = original.toJson();
      final restored = MessagePacket.fromJson(json);
      expect(restored.sender_id, equals('user123'));
      expect(restored.content, equals('Hello World!'));
    });

    test('MessagePacket MsgPack roundtrip', () {
      final original = MessagePacket.create(
        sender_id: 'msgpack_user',
        content: 'MsgPack content',
        timestamp: DateTime.now(),
      );
      final bytes = original.toMsgPack();
      final restored = MessagePacket.fromMsgPack(bytes);
      expect(restored.sender_id, equals('msgpack_user'));
      expect(restored.content, equals('MsgPack content'));
    });

    // --------------------------------------------------------------------------
    // DataChunkPacket Roundtrips
    // --------------------------------------------------------------------------
    test('DataChunkPacket JSON roundtrip', () {
      final original = DataChunkPacket.create(
        chunk_index: 5,
        total_chunks: 10,
        data: {'key': 'value', 'nested': {'deep': true}},
        checksum: 'abc123xyz',
      );
      final json = original.toJson();
      final restored = DataChunkPacket.fromJson(json);
      expect(restored.chunk_index, equals(5));
      expect(restored.total_chunks, equals(10));
      expect(restored.checksum, equals('abc123xyz'));
    });

    test('DataChunkPacket MsgPack roundtrip', () {
      final original = DataChunkPacket.create(
        chunk_index: 3,
        total_chunks: 8,
        data: {'msgpack': 'data'},
        checksum: 'msgpack_checksum',
      );
      final bytes = original.toMsgPack();
      final restored = DataChunkPacket.fromMsgPack(bytes);
      expect(restored.chunk_index, equals(3));
      expect(restored.total_chunks, equals(8));
    });

    // --------------------------------------------------------------------------
    // UserProfilePacket Roundtrips
    // --------------------------------------------------------------------------
    test('UserProfilePacket JSON roundtrip', () {
      final original = UserProfilePacket.create(
        user_id: 12345,
        username: 'testuser',
        email: 'test@example.com',
        bio: 'Hello, I am a test user!',
        age: 30,
        balance: 99.99,
        tags: ['developer', 'gamer', 'reader'],
        preferences: {'theme': 'dark', 'language': 'en'},
        avatar: Uint8List.fromList([1, 2, 3, 4]),
        created_at: DateTime.parse('2024-01-01T00:00:00.000Z'),
        last_login: DateTime.parse('2024-06-15T12:00:00.000Z'),
      );
      final json = original.toJson();
      final restored = UserProfilePacket.fromJson(json);
      expect(restored.user_id, equals(12345));
      expect(restored.username, equals('testuser'));
      expect(restored.email, equals('test@example.com'));
      expect(restored.bio, equals('Hello, I am a test user!'));
      expect(restored.age, equals(30));
      expect(restored.tags, equals(['developer', 'gamer', 'reader']));
    });

    test('UserProfilePacket MsgPack roundtrip', () {
      final original = UserProfilePacket.create(
        user_id: 67890,
        username: 'msgpack_user',
        email: 'msgpack@example.com',
        balance: 50.50,
        created_at: DateTime.now(),
      );
      final bytes = original.toMsgPack();
      final restored = UserProfilePacket.fromMsgPack(bytes);
      expect(restored.user_id, equals(67890));
      expect(restored.username, equals('msgpack_user'));
    });

    // --------------------------------------------------------------------------
    // SecureMessagePacket Roundtrips
    // --------------------------------------------------------------------------
    test('SecureMessagePacket JSON roundtrip', () {
      final original = SecureMessagePacket.create(
        message_id: 'secure-001',
        sender_id: 100,
        recipient_id: 200,
        subject: 'Secure Subject',
        body: 'This is a secure message body.',
        attachments: [{'name': 'file1.pdf', 'size': 1024}],
        encrypted_payload: Uint8List.fromList([0xCA, 0xFE, 0xBA, 0xBE]),
        priority: 5,
        is_read: false,
        sent_at: DateTime.parse('2024-07-01T10:00:00.000Z'),
      );
      final json = original.toJson();
      final restored = SecureMessagePacket.fromJson(json);
      expect(restored.message_id, equals('secure-001'));
      expect(restored.sender_id, equals(100));
      expect(restored.recipient_id, equals(200));
      expect(restored.subject, equals('Secure Subject'));
      expect(restored.priority, equals(5));
      expect(restored.is_read, equals(false));
    });

    test('SecureMessagePacket MsgPack roundtrip', () {
      final original = SecureMessagePacket.create(
        message_id: 'msgpack-secure',
        sender_id: 10,
        recipient_id: 20,
        priority: 3,
        is_read: true,
        sent_at: DateTime.now(),
      );
      final bytes = original.toMsgPack();
      final restored = SecureMessagePacket.fromMsgPack(bytes);
      expect(restored.message_id, equals('msgpack-secure'));
      expect(restored.sender_id, equals(10));
      expect(restored.priority, equals(3));
    });

    // --------------------------------------------------------------------------
    // ComprehensivePacket Roundtrips
    // --------------------------------------------------------------------------
    test('ComprehensivePacket JSON roundtrip with all fields', () {
      final original = ComprehensivePacket.create(
        int_field: 42,
        float_field: 3.14,
        double_field: 2.71828,
        string_field: 'comprehensive test',
        bool_field: true,
        datetime_field: DateTime.parse('2024-06-15T12:00:00.000Z'),
        time_field: TimeOfDay(hour: 14, minute: 30),
        list_field: [1, 'two', 3.0, true],
        list_int_field: [10, 20, 30, 40, 50],
        list_string_field: ['alpha', 'beta', 'gamma'],
        map_field: {'key1': 'value1', 'key2': 42},
        embedded_map_field: {'nested': {'deep': {'deeper': 'value'}}},
        map_string_dynamic_field: {'dynamic': 'content'},
        bytes_field: Uint8List.fromList([0xDE, 0xAD, 0xBE, 0xEF]),
      );
      final json = original.toJson();
      final restored = ComprehensivePacket.fromJson(json);
      expect(restored.int_field, equals(42));
      expect(restored.string_field, equals('comprehensive test'));
      expect(restored.bool_field, equals(true));
      expect(restored.list_int_field, equals([10, 20, 30, 40, 50]));
      expect(restored.list_string_field, equals(['alpha', 'beta', 'gamma']));
    });

    test('ComprehensivePacket MsgPack roundtrip', () {
      final original = ComprehensivePacket.create(
        int_field: 999,
        float_field: 1.5,
        string_field: 'msgpack comprehensive',
        bool_field: false,
        list_int_field: [1, 2, 3],
        bytes_field: Uint8List.fromList([0x01, 0x02, 0x03]),
      );
      final bytes = original.toMsgPack();
      final restored = ComprehensivePacket.fromMsgPack(bytes);
      expect(restored.int_field, equals(999));
      expect(restored.string_field, equals('msgpack comprehensive'));
      expect(restored.bool_field, equals(false));
    });

    // --------------------------------------------------------------------------
    // Edge cases in deserialization
    // --------------------------------------------------------------------------
    test('Deserialization handles null optional fields', () {
      final original = UserProfilePacket.create(
        user_id: 1,
        username: 'minimal',
        email: 'minimal@test.com',
        created_at: DateTime.now(),
      );
      final json = original.toJson();
      final restored = UserProfilePacket.fromJson(json);
      expect(restored.bio, isNull);
      expect(restored.age, isNull);
      expect(restored.avatar, isNull);
      expect(restored.last_login, isNull);
    });

    test('Deserialization handles empty collections', () {
      final original = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'empty',
        list_field: [],
        list_int_field: [],
        list_string_field: [],
        map_field: {},
      );
      final json = original.toJson();
      final restored = ComprehensivePacket.fromJson(json);
      expect(restored.list_int_field, isEmpty);
      expect(restored.list_string_field, isEmpty);
    });

    test('Deserialization preserves Unicode', () {
      final original = MessagePacket.create(
        sender_id: '日本語ユーザー',
        content: 'Hello 世界! 🎉🚀💻',
        timestamp: DateTime.now(),
      );
      final json = original.toJson();
      final restored = MessagePacket.fromJson(json);
      expect(restored.sender_id, equals('日本語ユーザー'));
      expect(restored.content, equals('Hello 世界! 🎉🚀💻'));
    });

    test('Deserialization handles large binary data', () {
      final largePayload = Uint8List.fromList(List.generate(1000, (i) => i % 256));
      final original = SecureMessagePacket.create(
        message_id: 'large_binary',
        sender_id: 1,
        recipient_id: 2,
        encrypted_payload: largePayload,
        sent_at: DateTime.now(),
      );
      final json = original.toJson();
      final restored = SecureMessagePacket.fromJson(json);
      expect(restored.encrypted_payload?.length, equals(1000));
    });
  });
}
