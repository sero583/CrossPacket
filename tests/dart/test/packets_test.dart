// CrossPacket - Comprehensive Dart Test Suite (Pure Dart)
//
// Author: Serhat Güler (sero583)
// GitHub: https://github.com/sero583
// License: MIT
//
// This test validates all generated packets with comprehensive edge cases.
// Uses pure Dart test package (no Flutter dependency).
// Uses dynamic dispatch to support JSON_ONLY, MSGPACK_ONLY, and BOTH modes.
//
// NOTE: Dart does not support dynamic static method invocation. Static methods
// like fromJson/fromMsgPack must exist at compile time. Therefore, we only test:
// - Packet creation and field access
// - Instance method serialization (toJson/toMsgPack via dynamic dispatch)
// Deserialization roundtrip is tested in BOTH mode in CI where all methods exist.

import 'dart:typed_data';
import 'package:test/test.dart';

// Import generated packets from lib (using package import for coverage)
// TimeOfDay is exported from data_packet.dart (pure Dart implementation)
import 'package:crosspacket_tests/generated/ping_packet.dart';
import 'package:crosspacket_tests/generated/pong_packet.dart';
import 'package:crosspacket_tests/generated/message_packet.dart';
import 'package:crosspacket_tests/generated/data_chunk_packet.dart';
import 'package:crosspacket_tests/generated/user_profile_packet.dart';
import 'package:crosspacket_tests/generated/secure_message_packet.dart';
import 'package:crosspacket_tests/generated/comprehensive_packet.dart';
import 'package:crosspacket_tests/data_packet.dart';

// Runtime flags for method availability (detected at startup)
bool _hasJsonMethods = false;
bool _hasMsgPackMethods = false;

void _detectMethods() {
  // Detect available methods by trying to call them
  final testPacket = PingPacket.create(timestamp: DateTime.now(), message: 'test');
  
  try {
    // Try to access toJson - if it exists, JSON is enabled
    (testPacket as dynamic).toJson();
    _hasJsonMethods = true;
  } catch (e) {
    _hasJsonMethods = false;
  }
  
  try {
    // Try to access toMsgPack - if it exists, MsgPack is enabled
    (testPacket as dynamic).toMsgPack();
    _hasMsgPackMethods = true;
  } catch (e) {
    _hasMsgPackMethods = false;
  }
}

// Dynamic method invocation for instance methods (works at runtime)
String _toJson(dynamic obj) => (obj as dynamic).toJson() as String;
Uint8List _toMsgPack(dynamic obj) => (obj as dynamic).toMsgPack() as Uint8List;

void main() {
  // Detect available methods before running tests
  setUpAll(() {
    _detectMethods();
    print('JSON methods available: $_hasJsonMethods');
    print('MsgPack methods available: $_hasMsgPackMethods');
  });

  // ============================================================================
  // PingPacket Tests
  // ============================================================================
  group('PingPacket', () {
    test('TYPE constant is correct', () {
      final p = PingPacket.create(timestamp: DateTime.now(), message: 'test');
      expect(p.type, equals('/example/PingPacket'));
    });

    test('constructor sets fields correctly', () {
      final ts = DateTime.now();
      final p = PingPacket.create(timestamp: ts, message: 'hello');
      expect(p.message, equals('hello'));
      expect(p.timestamp, isNotNull);
    });

    test('default constructor and setters work', () {
      final p = PingPacket();
      p.message = 'setter test';
      p.timestamp = DateTime.now();
      expect(p.message, equals('setter test'));
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = PingPacket.create(
        timestamp: DateTime.parse('2024-01-15T10:30:00.000Z'),
        message: 'json test',
      );
      final json = _toJson(p);
      expect(json, contains('"packetType":"/example/PingPacket"'));
      expect(json, contains('"message":"json test"'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = PingPacket.create(
        timestamp: DateTime.now(),
        message: 'msgpack test',
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
      expect(bytes, isA<Uint8List>());
    });
  });

  // ============================================================================
  // PongPacket Tests
  // ============================================================================
  group('PongPacket', () {
    test('TYPE constant is correct', () {
      final p = PongPacket.create(
        original_timestamp: DateTime.now(),
        response_timestamp: DateTime.now(),
        latency_ms: 10,
      );
      expect(p.type, equals('/example/PongPacket'));
    });

    test('empty constructor and setters work', () {
      final p = PongPacket();
      p.original_timestamp = DateTime.now();
      p.latency_ms = 5;
      expect(p.latency_ms, equals(5));
    });

    test('constructor sets fields correctly', () {
      final p = PongPacket.create(
        original_timestamp: DateTime.parse('2024-01-01T00:00:00.000Z'),
        response_timestamp: DateTime.parse('2024-01-01T00:00:00.150Z'),
        latency_ms: 150,
      );
      expect(p.latency_ms, equals(150));
      expect(p.original_timestamp, isNotNull);
      expect(p.response_timestamp, isNotNull);
    });

    test('zero latency works', () {
      final now = DateTime.now();
      final p = PongPacket.create(
        original_timestamp: now,
        response_timestamp: now,
        latency_ms: 0,
      );
      expect(p.latency_ms, equals(0));
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = PongPacket.create(
        original_timestamp: DateTime.parse('2024-04-01T10:00:00.000Z'),
        response_timestamp: DateTime.parse('2024-04-01T10:00:00.025Z'),
        latency_ms: 25,
      );
      final json = _toJson(p);
      expect(json, contains('"latency_ms":25'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = PongPacket.create(
        original_timestamp: DateTime.now(),
        response_timestamp: DateTime.now(),
        latency_ms: 100,
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // MessagePacket Tests
  // ============================================================================
  group('MessagePacket', () {
    test('TYPE constant is correct', () {
      final m = MessagePacket.create(
        sender_id: 'user1',
        content: 'hello',
        timestamp: DateTime.now(),
      );
      expect(m.type, equals('/chat/MessagePacket'));
    });

    test('empty constructor and setters work', () {
      final m = MessagePacket();
      m.sender_id = 'setter_sender';
      m.content = 'setter_content';
      expect(m.sender_id, equals('setter_sender'));
    });

    test('constructor sets fields correctly', () {
      final m = MessagePacket.create(
        sender_id: 'user123',
        content: 'Hello, World!',
        timestamp: DateTime.now(),
      );
      expect(m.sender_id, equals('user123'));
      expect(m.content, equals('Hello, World!'));
    });

    test('empty strings work', () {
      final m = MessagePacket.create(
        sender_id: '',
        content: '',
        timestamp: DateTime.now(),
      );
      expect(m.sender_id, equals(''));
      expect(m.content, equals(''));
    });

    test('Unicode content works', () {
      final unicodeContent = 'Hello 世界! Émoji: 🎉🚀💻';
      final m = MessagePacket.create(
        sender_id: 'unicode_sender',
        content: unicodeContent,
        timestamp: DateTime.now(),
      );
      expect(m.content, equals(unicodeContent));
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final m = MessagePacket.create(
        sender_id: 'sender_abc',
        content: 'JSON test content',
        timestamp: DateTime.parse('2024-01-15T10:30:00.000Z'),
      );
      final json = _toJson(m);
      expect(json, contains('"sender_id":"sender_abc"'));
      expect(json, contains('"content":"JSON test content"'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final m = MessagePacket.create(
        sender_id: 'msgpack_sender',
        content: 'MsgPack test',
        timestamp: DateTime.now(),
      );
      final bytes = _toMsgPack(m);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // DataChunkPacket Tests
  // ============================================================================
  group('DataChunkPacket', () {
    test('TYPE constant is correct', () {
      final chunk = DataChunkPacket.create(
        chunk_index: 0,
        total_chunks: 1,
        data: {'key': 'value'},
        checksum: 'abc123',
      );
      expect(chunk.type, equals('/example/DataChunkPacket'));
    });

    test('empty constructor and setters work', () {
      final p = DataChunkPacket();
      p.chunk_index = 1;
      p.total_chunks = 5;
      p.data = {'setter': 'test'};
      expect(p.chunk_index, equals(1));
    });

    test('constructor with Map works', () {
      final chunkData = <dynamic, dynamic>{
        'key1': 'value1',
        'key2': 42,
        'nested': {'deep': true},
      };
      final p = DataChunkPacket.create(
        chunk_index: 0,
        total_chunks: 10,
        data: chunkData,
        checksum: 'abc123checksum',
      );
      expect(p.chunk_index, equals(0));
      expect(p.total_chunks, equals(10));
      expect(p.checksum, equals('abc123checksum'));
      expect(p.data, isNotNull);
    });

    test('empty Map works', () {
      final p = DataChunkPacket.create(
        chunk_index: 5,
        total_chunks: 5,
        data: {},
        checksum: '',
      );
      expect(p.data, isNotNull);
      expect(p.data!.isEmpty, isTrue);
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = DataChunkPacket.create(
        chunk_index: 2,
        total_chunks: 5,
        data: {'test': 'value'},
        checksum: 'json_checksum',
      );
      final json = _toJson(p);
      expect(json, contains('"chunk_index":2'));
      expect(json, contains('"checksum":"json_checksum"'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = DataChunkPacket.create(
        chunk_index: 3,
        total_chunks: 8,
        data: {'msgpack': 'test'},
        checksum: 'msgpack_checksum',
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // UserProfilePacket Tests (CORRECT field names from packets.json)
  // Fields: user_id (int), username, email, bio, age, balance, tags, preferences, avatar, created_at, last_login
  // ============================================================================
  group('UserProfilePacket', () {
    test('TYPE constant is correct', () {
      final p = UserProfilePacket.create(
        user_id: 123,
        username: 'testuser',
        email: 'test@example.com',
        created_at: DateTime.now(),
      );
      expect(p.type, equals('/example/UserProfilePacket'));
    });

    test('empty constructor and setters work', () {
      final p = UserProfilePacket();
      p.user_id = 456;
      p.username = 'setter_username';
      p.email = 'setter@example.com';
      expect(p.user_id, equals(456));
      expect(p.username, equals('setter_username'));
    });

    test('constructor sets all fields correctly', () {
      final p = UserProfilePacket.create(
        user_id: 789,
        username: 'johndoe',
        email: 'john@example.com',
        bio: 'Hello, I am John',
        age: 30,
        balance: 100.50,
        tags: ['developer', 'gamer'],
        preferences: {'theme': 'dark'},
        avatar: Uint8List.fromList([1, 2, 3]),
        created_at: DateTime.parse('2024-01-01T00:00:00.000Z'),
        last_login: DateTime.parse('2024-06-15T12:00:00.000Z'),
      );
      expect(p.user_id, equals(789));
      expect(p.username, equals('johndoe'));
      expect(p.email, equals('john@example.com'));
      expect(p.bio, equals('Hello, I am John'));
      expect(p.age, equals(30));
      expect(p.balance, closeTo(100.50, 0.001));
      expect(p.tags, equals(['developer', 'gamer']));
      expect(p.preferences!['theme'], equals('dark'));
      expect(p.avatar!.length, equals(3));
    });

    test('optional fields can be null', () {
      final p = UserProfilePacket.create(
        user_id: 1,
        username: 'user',
        email: 'user@example.com',
        created_at: DateTime.now(),
      );
      expect(p.bio, isNull);
      expect(p.age, isNull);
      expect(p.avatar, isNull);
      expect(p.last_login, isNull);
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = UserProfilePacket.create(
        user_id: 999,
        username: 'json_user',
        email: 'json@example.com',
        created_at: DateTime.parse('2024-06-15T12:00:00.000Z'),
      );
      final json = _toJson(p);
      expect(json, contains('"user_id":999'));
      expect(json, contains('"username":"json_user"'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = UserProfilePacket.create(
        user_id: 888,
        username: 'msgpack_user',
        email: 'msgpack@example.com',
        created_at: DateTime.now(),
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // SecureMessagePacket Tests (CORRECT field names from packets.json)
  // Fields: message_id, sender_id (int), recipient_id (int), subject, body, 
  //         attachments, encrypted_payload, priority, is_read, sent_at
  // ============================================================================
  group('SecureMessagePacket', () {
    test('TYPE constant is correct', () {
      final p = SecureMessagePacket.create(
        message_id: 'msg-001',
        sender_id: 1,
        recipient_id: 2,
        sent_at: DateTime.now(),
      );
      expect(p.type, equals('/example/SecureMessagePacket'));
    });

    test('empty constructor and setters work', () {
      final p = SecureMessagePacket();
      p.message_id = 'setter_msg';
      p.sender_id = 100;
      p.recipient_id = 200;
      expect(p.message_id, equals('setter_msg'));
      expect(p.sender_id, equals(100));
    });

    test('constructor sets all fields correctly', () {
      final payload = Uint8List.fromList([0xDE, 0xAD, 0xBE, 0xEF]);
      final p = SecureMessagePacket.create(
        message_id: 'secure-msg-001',
        sender_id: 10,
        recipient_id: 20,
        subject: 'Test Subject',
        body: 'Test body content',
        attachments: [{'name': 'file.txt', 'size': 1024}],
        encrypted_payload: payload,
        priority: 3,
        is_read: false,
        sent_at: DateTime.now(),
      );
      expect(p.message_id, equals('secure-msg-001'));
      expect(p.sender_id, equals(10));
      expect(p.recipient_id, equals(20));
      expect(p.subject, equals('Test Subject'));
      expect(p.body, equals('Test body content'));
      expect(p.encrypted_payload, equals(payload));
      expect(p.priority, equals(3));
      expect(p.is_read, equals(false));
    });

    test('empty encrypted payload works', () {
      final p = SecureMessagePacket.create(
        message_id: 'empty_payload',
        sender_id: 1,
        recipient_id: 2,
        encrypted_payload: Uint8List(0),
        sent_at: DateTime.now(),
      );
      expect(p.encrypted_payload!.isEmpty, isTrue);
    });

    test('large encrypted payload works', () {
      final largePayload = Uint8List.fromList(List.generate(10000, (i) => i % 256));
      final p = SecureMessagePacket.create(
        message_id: 'large_payload',
        sender_id: 1,
        recipient_id: 2,
        encrypted_payload: largePayload,
        sent_at: DateTime.now(),
      );
      expect(p.encrypted_payload!.length, equals(10000));
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = SecureMessagePacket.create(
        message_id: 'json_msg',
        sender_id: 5,
        recipient_id: 10,
        subject: 'JSON Test',
        sent_at: DateTime.parse('2024-07-01T00:00:00.000Z'),
      );
      final json = _toJson(p);
      expect(json, contains('"message_id":"json_msg"'));
      expect(json, contains('"sender_id":5'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = SecureMessagePacket.create(
        message_id: 'msgpack_msg',
        sender_id: 15,
        recipient_id: 25,
        sent_at: DateTime.now(),
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // ComprehensivePacket Tests (CORRECT field names from packets.json)
  // Fields: int_field, float_field, double_field, string_field, bool_field,
  //         datetime_field, time_field, list_field, list_int_field, list_string_field,
  //         map_field, embedded_map_field, map_string_dynamic_field, bytes_field
  // ============================================================================
  group('ComprehensivePacket', () {
    test('TYPE constant is correct', () {
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'test',
      );
      expect(p.type, equals('/test/ComprehensivePacket'));
    });

    test('empty constructor and setters work', () {
      final p = ComprehensivePacket();
      p.int_field = 42;
      p.string_field = 'setter_string';
      p.bool_field = true;
      expect(p.int_field, equals(42));
      expect(p.string_field, equals('setter_string'));
      expect(p.bool_field, equals(true));
    });

    test('constructor sets all fields correctly', () {
      final p = ComprehensivePacket.create(
        int_field: 999,
        float_field: 3.14,
        double_field: 2.71828,
        string_field: 'comprehensive_test',
        bool_field: true,
        datetime_field: DateTime.now(),
        time_field: TimeOfDay(hour: 14, minute: 30),
        list_field: [1, 'two', 3.0],
        list_int_field: [10, 20, 30],
        list_string_field: ['a', 'b', 'c'],
        map_field: {'key': 'value'},
        embedded_map_field: {'nested': {'deep': true}},
        map_string_dynamic_field: {'dynamic': 42},
        bytes_field: Uint8List.fromList([1, 2, 3]),
      );
      expect(p.int_field, equals(999));
      expect(p.float_field, closeTo(3.14, 0.001));
      expect(p.double_field, closeTo(2.71828, 0.00001));
      expect(p.string_field, equals('comprehensive_test'));
      expect(p.bool_field, equals(true));
      expect(p.list_int_field, equals([10, 20, 30]));
      expect(p.list_string_field, equals(['a', 'b', 'c']));
      expect(p.time_field?.hour, equals(14));
      expect(p.time_field?.minute, equals(30));
    });

    test('empty collections work', () {
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'empty_collections',
        list_field: [],
        list_int_field: [],
        list_string_field: [],
        map_field: {},
        embedded_map_field: {},
      );
      expect(p.list_field, isEmpty);
      expect(p.list_int_field, isEmpty);
      expect(p.map_field, isEmpty);
    });

    test('TimeOfDay serialization works', () {
      final tod = TimeOfDay(hour: 9, minute: 15);
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'time_test',
        time_field: tod,
      );
      expect(p.time_field, isNotNull);
      expect(p.time_field?.hour, equals(9));
      expect(p.time_field?.minute, equals(15));
    });

    test('Unicode in strings works', () {
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: '名前テスト 🌍',
        list_string_field: ['日本語', 'Ελληνικά', '한국어'],
      );
      expect(p.string_field, equals('名前テスト 🌍'));
      expect(p.list_string_field, contains('日本語'));
    });

    test('toJson produces valid output', () {
      if (!_hasJsonMethods) return;
      final p = ComprehensivePacket.create(
        int_field: 12345,
        string_field: 'json_comprehensive',
        bool_field: true,
        float_field: 42.5,
      );
      final json = _toJson(p);
      expect(json, contains('"int_field":12345'));
      expect(json, contains('"string_field":"json_comprehensive"'));
    });

    test('toMsgPack produces valid output', () {
      if (!_hasMsgPackMethods) return;
      final p = ComprehensivePacket.create(
        int_field: 67890,
        string_field: 'msgpack_comprehensive',
        bytes_field: Uint8List.fromList([0xCA, 0xFE, 0xBA, 0xBE]),
      );
      final bytes = _toMsgPack(p);
      expect(bytes, isNotEmpty);
    });
  });

  // ============================================================================
  // Cross-cutting Tests
  // ============================================================================
  group('Cross-cutting', () {
    test('All packets have unique TYPE constants', () {
      final types = <String>{};
      final packets = [
        PingPacket.create(timestamp: DateTime.now(), message: ''),
        PongPacket.create(original_timestamp: DateTime.now(), response_timestamp: DateTime.now(), latency_ms: 0),
        MessagePacket.create(sender_id: '', content: '', timestamp: DateTime.now()),
        DataChunkPacket.create(chunk_index: 0, total_chunks: 0, data: {}, checksum: ''),
        UserProfilePacket.create(user_id: 0, username: '', email: '', created_at: DateTime.now()),
        SecureMessagePacket.create(message_id: '', sender_id: 0, recipient_id: 0, sent_at: DateTime.now()),
        ComprehensivePacket.create(int_field: 0, string_field: ''),
      ];
      for (final p in packets) {
        expect(types.contains(p.type), isFalse, reason: 'Duplicate TYPE: ${p.type}');
        types.add(p.type);
      }
    });

    test('JSON methods existence matches flag', () {
      if (_hasJsonMethods) {
        // Should be able to call toJson
        final p = PingPacket.create(timestamp: DateTime.now(), message: 'test');
        expect(() => _toJson(p), returnsNormally);
      }
    });

    test('MsgPack methods existence matches flag', () {
      if (_hasMsgPackMethods) {
        // Should be able to call toMsgPack
        final p = PingPacket.create(timestamp: DateTime.now(), message: 'test');
        expect(() => _toMsgPack(p), returnsNormally);
      }
    });

    test('At least one serialization method is available', () {
      expect(_hasJsonMethods || _hasMsgPackMethods, isTrue,
          reason: 'At least JSON or MsgPack should be available');
    });
  });

  // ============================================================================
  // Edge Cases and Stress Tests
  // ============================================================================
  group('Edge Cases', () {
    test('Very long strings work', () {
      final longString = 'x' * 100000;
      final p = MessagePacket.create(
        sender_id: longString,
        content: longString,
        timestamp: DateTime.now(),
      );
      expect(p.sender_id?.length, equals(100000));
    });

    test('Very large integer arrays work', () {
      final largeCounts = List.generate(10000, (i) => i);
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'large_array',
        list_int_field: largeCounts,
      );
      expect(p.list_int_field?.length, equals(10000));
    });

    test('Deeply nested metadata works', () {
      Map<dynamic, dynamic> createNested(int depth) {
        if (depth == 0) return {'leaf': true};
        return {'nested': createNested(depth - 1)};
      }
      final deepMetadata = createNested(20);
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'deep_nested',
        embedded_map_field: deepMetadata,
      );
      expect(p.embedded_map_field, isNotNull);
    });

    test('Special characters in strings work', () {
      final special = r'Tab:	Newline:' '\n' r'Quote:"' "'" r'Backslash:\';
      final p = MessagePacket.create(
        sender_id: special,
        content: special,
        timestamp: DateTime.now(),
      );
      expect(p.content, equals(special));
    });

    test('Boundary integer values work', () {
      final p = ComprehensivePacket.create(
        int_field: 2147483647, // Max 32-bit int
        string_field: 'max_int',
        list_int_field: [0, 2147483647, -2147483648],
      );
      expect(p.int_field, equals(2147483647));
    });

    test('Boundary float values work', () {
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'float_test',
        double_field: double.maxFinite,
      );
      expect(p.double_field, equals(double.maxFinite));
    });

    test('Zero values work', () {
      final p = PongPacket.create(
        original_timestamp: DateTime.fromMillisecondsSinceEpoch(0),
        response_timestamp: DateTime.fromMillisecondsSinceEpoch(0),
        latency_ms: 0,
      );
      expect(p.latency_ms, equals(0));
    });

    test('Empty binary arrays work', () {
      final p = SecureMessagePacket.create(
        message_id: 'empty_binary',
        sender_id: 1,
        recipient_id: 2,
        encrypted_payload: Uint8List(0),
        sent_at: DateTime.now(),
      );
      expect(p.encrypted_payload?.isEmpty, isTrue);
    });

    test('All bytes 0-255 work in binary', () {
      final allBytes = Uint8List.fromList(List.generate(256, (i) => i));
      final p = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'all_bytes',
        bytes_field: allBytes,
      );
      for (int i = 0; i < 256; i++) {
        expect(p.bytes_field![i], equals(i));
      }
    });

    test('TimeOfDay boundary values work', () {
      final midnight = TimeOfDay(hour: 0, minute: 0);
      final endOfDay = TimeOfDay(hour: 23, minute: 59);
      
      final p1 = ComprehensivePacket.create(
        int_field: 1,
        string_field: 'midnight',
        time_field: midnight,
      );
      expect(p1.time_field?.hour, equals(0));
      expect(p1.time_field?.minute, equals(0));

      final p2 = ComprehensivePacket.create(
        int_field: 2,
        string_field: 'end_of_day',
        time_field: endOfDay,
      );
      expect(p2.time_field?.hour, equals(23));
      expect(p2.time_field?.minute, equals(59));
    });
  });

  // ============================================================================
  // Static Deserialization Roundtrip Tests (for higher coverage)
  // These tests directly call the static fromJson/fromMsgPack methods
  // ============================================================================
  group('Deserialization Roundtrips', () {
    // --------------------------------------------------------------------------
    // PingPacket Roundtrips
    // --------------------------------------------------------------------------
    test('PingPacket JSON roundtrip', () {
      if (!_hasJsonMethods) return;
      final original = PingPacket.create(
        timestamp: DateTime.parse('2024-06-15T12:30:45.000Z'),
        message: 'roundtrip test',
      );
      final json = original.toJson();
      final restored = PingPacket.fromJson(json);
      expect(restored.message, equals(original.message));
    });

    test('PingPacket MsgPack roundtrip', () {
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasMsgPackMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasJsonMethods) return;
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
      if (!_hasJsonMethods) return;
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
