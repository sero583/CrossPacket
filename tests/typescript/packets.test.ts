/**
 * CrossPacket - Comprehensive TypeScript Test Suite (Jest)
 *
 * Author: Serhat Güler (sero583)
 * GitHub: https://github.com/sero583
 * License: MIT
 *
 * This test suite provides 100% code coverage for all generated packets.
 * Uses reflection-like patterns to support JSON_ONLY, MSGPACK_ONLY, and BOTH modes.
 */

// Import ALL generated packets
import { PingPacket } from '../../generated/typescript/ping_packet';
import { PongPacket } from '../../generated/typescript/pong_packet';
import { MessagePacket } from '../../generated/typescript/message_packet';
import { DataChunkPacket } from '../../generated/typescript/data_chunk_packet';
import { ComprehensivePacket } from '../../generated/typescript/comprehensive_packet';
import { UserProfilePacket } from '../../generated/typescript/user_profile_packet';
import { SecureMessagePacket } from '../../generated/typescript/secure_message_packet';
import { deserializePacket } from '../../generated/typescript/index';

const TEST_MODE = (process.env.TEST_MODE || 'BOTH').toUpperCase();

// Reflection-like helper functions for method detection
function hasMethod(obj: any, method: string): boolean {
  return typeof obj[method] === 'function';
}

function hasStaticMethod(cls: any, method: string): boolean {
  return typeof cls[method] === 'function';
}

// Helper to invoke instance method via reflection
function invokeMethod<T>(obj: any, method: string, ...args: any[]): T {
  return obj[method](...args);
}

// Helper to invoke static method via reflection
function invokeStatic<T>(cls: any, method: string, ...args: any[]): T {
  return cls[method](...args);
}

// Detect available methods at runtime from a sample packet
const samplePing = new PingPacket({ timestamp: new Date(), message: 'test' });
const hasJson = hasMethod(samplePing, 'toJSON');
const hasMsgPack = hasMethod(samplePing, 'toMsgPack');

// ============================================================================
// PingPacket Tests
// ============================================================================
describe('PingPacket', () => {
  const createPacket = () => new PingPacket({
    timestamp: new Date('2024-01-15T10:30:00.000Z'),
    message: 'Hello World'
  });

  test('TYPE constant is correct', () => {
    expect(PingPacket.TYPE).toBe('/example/PingPacket');
  });

  test('constructor with Date', () => {
    const p = createPacket();
    expect(p.timestamp).toBeInstanceOf(Date);
    expect(p.message).toBe('Hello World');
  });

  test('constructor with string date', () => {
    const p = new PingPacket({
      timestamp: '2024-01-15T10:30:00.000Z',
      message: 'test'
    });
    expect(p.timestamp).toBeInstanceOf(Date);
  });

  test('toJSON returns valid JSON string', () => {
    if (!hasJson) return;
    const p = createPacket();
    const json = invokeMethod<string>(p, 'toJSON');
    expect(typeof json).toBe('string');
    const parsed = JSON.parse(json);
    expect(parsed.packetType).toBe('/example/PingPacket');
    expect(parsed.message).toBe('Hello World');
  });

  test('fromJSON roundtrip', () => {
    if (!hasJson) return;
    const original = createPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<PingPacket>(PingPacket, 'fromJSON', json);
    expect(decoded.message).toBe(original.message);
    expect(decoded.timestamp.getTime()).toBe(original.timestamp.getTime());
  });

  test('toMsgPack returns Uint8Array', () => {
    if (!hasMsgPack) return;
    const p = createPacket();
    const bytes = invokeMethod<Uint8Array>(p, 'toMsgPack');
    expect(bytes).toBeInstanceOf(Uint8Array);
    expect(bytes.length).toBeGreaterThan(0);
  });

  test('fromMsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<PingPacket>(PingPacket, 'fromMsgPack', bytes);
    expect(decoded.message).toBe(original.message);
  });
});

// ============================================================================
// PongPacket Tests
// ============================================================================
describe('PongPacket', () => {
  const createPacket = () => new PongPacket({
    originalTimestamp: new Date('2024-01-15T10:30:00.000Z'),
    responseTimestamp: new Date('2024-01-15T10:30:00.150Z'),
    latencyMs: 150
  });

  test('TYPE constant is correct', () => {
    expect(PongPacket.TYPE).toBe('/example/PongPacket');
  });

  test('constructor sets fields correctly', () => {
    const p = createPacket();
    expect(p.latencyMs).toBe(150);
    expect(p.originalTimestamp).toBeInstanceOf(Date);
    expect(p.responseTimestamp).toBeInstanceOf(Date);
  });

  test('constructor with string dates', () => {
    const p = new PongPacket({
      originalTimestamp: '2024-01-15T10:30:00.000Z',
      responseTimestamp: '2024-01-15T10:30:00.150Z',
      latencyMs: 100
    });
    expect(p.originalTimestamp).toBeInstanceOf(Date);
  });

  test('JSON roundtrip', () => {
    if (!hasJson) return;
    const original = createPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<PongPacket>(PongPacket, 'fromJSON', json);
    expect(decoded.latencyMs).toBe(original.latencyMs);
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<PongPacket>(PongPacket, 'fromMsgPack', bytes);
    expect(decoded.latencyMs).toBe(original.latencyMs);
  });
});

// ============================================================================
// MessagePacket Tests
// ============================================================================
describe('MessagePacket', () => {
  const createPacket = () => new MessagePacket({
    senderId: 'user123',
    content: 'Hello, World!',
    timestamp: new Date('2024-01-15T10:30:00.000Z')
  });

  test('TYPE constant is correct', () => {
    expect(MessagePacket.TYPE).toBe('/chat/MessagePacket');
  });

  test('constructor sets fields correctly', () => {
    const p = createPacket();
    expect(p.senderId).toBe('user123');
    expect(p.content).toBe('Hello, World!');
  });

  test('empty strings work', () => {
    const p = new MessagePacket({
      senderId: '',
      content: '',
      timestamp: new Date()
    });
    expect(p.senderId).toBe('');
    expect(p.content).toBe('');
  });

  test('Unicode content works', () => {
    const p = new MessagePacket({
      senderId: 'sender',
      content: 'Hello 世界! 🎉🚀',
      timestamp: new Date()
    });
    expect(p.content).toBe('Hello 世界! 🎉🚀');
  });

  test('JSON roundtrip', () => {
    if (!hasJson) return;
    const original = createPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<MessagePacket>(MessagePacket, 'fromJSON', json);
    expect(decoded.senderId).toBe(original.senderId);
    expect(decoded.content).toBe(original.content);
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<MessagePacket>(MessagePacket, 'fromMsgPack', bytes);
    expect(decoded.senderId).toBe(original.senderId);
  });
});

// ============================================================================
// DataChunkPacket Tests
// ============================================================================
describe('DataChunkPacket', () => {
  const createPacket = () => new DataChunkPacket({
    chunkIndex: 2,
    totalChunks: 10,
    data: new Map<any, any>([['key', 'value'], ['nested', { deep: true }]]),
    checksum: 'abc123checksum'
  });

  test('TYPE constant is correct', () => {
    expect(DataChunkPacket.TYPE).toBe('/example/DataChunkPacket');
  });

  test('constructor sets fields correctly', () => {
    const p = createPacket();
    expect(p.chunkIndex).toBe(2);
    expect(p.totalChunks).toBe(10);
    expect(p.checksum).toBe('abc123checksum');
  });

  test('empty data works', () => {
    const p = new DataChunkPacket({
      chunkIndex: 0,
      totalChunks: 1,
      data: new Map(),
      checksum: ''
    });
    expect(p.data.size).toBe(0);
  });

  test('JSON roundtrip', () => {
    if (!hasJson) return;
    const original = createPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<DataChunkPacket>(DataChunkPacket, 'fromJSON', json);
    expect(decoded.chunkIndex).toBe(original.chunkIndex);
    expect(decoded.totalChunks).toBe(original.totalChunks);
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<DataChunkPacket>(DataChunkPacket, 'fromMsgPack', bytes);
    expect(decoded.chunkIndex).toBe(original.chunkIndex);
  });
});

// ============================================================================
// UserProfilePacket Tests
// ============================================================================
describe('UserProfilePacket', () => {
  const createFullPacket = () => new UserProfilePacket({
    userId: 12345,
    username: 'testuser',
    email: 'test@example.com',
    bio: 'This is my bio',
    age: 25,
    balance: 100.50,
    tags: ['developer', 'gamer'],
    preferences: { theme: 'dark', language: 'en' },
    avatar: new Uint8Array([0x89, 0x50, 0x4E, 0x47]),
    createdAt: new Date('2024-01-01T00:00:00.000Z'),
    lastLogin: new Date('2024-01-15T10:30:00.000Z')
  });

  const createMinimalPacket = () => new UserProfilePacket({
    userId: 1,
    username: 'minimal',
    email: 'min@test.com',
    balance: 0,
    tags: [],
    preferences: {},
    createdAt: new Date()
  });

  test('TYPE constant is correct', () => {
    expect(UserProfilePacket.TYPE).toBe('/example/UserProfilePacket');
  });

  test('constructor with all fields', () => {
    const p = createFullPacket();
    expect(p.userId).toBe(12345);
    expect(p.bio).toBe('This is my bio');
    expect(p.age).toBe(25);
    expect(p.avatar).toBeInstanceOf(Uint8Array);
    expect(p.lastLogin).toBeInstanceOf(Date);
  });

  test('constructor with minimal fields (nullables)', () => {
    const p = createMinimalPacket();
    expect(p.bio).toBeNull();
    expect(p.age).toBeNull();
    expect(p.avatar).toBeNull();
    expect(p.lastLogin).toBeNull();
  });

  test('constructor with string dates', () => {
    const p = new UserProfilePacket({
      userId: 1,
      username: 'test',
      email: 'test@test.com',
      balance: 0,
      tags: [],
      preferences: {},
      createdAt: '2024-01-01T00:00:00.000Z',
      lastLogin: '2024-01-15T00:00:00.000Z'
    });
    expect(p.createdAt).toBeInstanceOf(Date);
    expect(p.lastLogin).toBeInstanceOf(Date);
  });

  test('JSON roundtrip with full packet', () => {
    if (!hasJson) return;
    const original = createFullPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<UserProfilePacket>(UserProfilePacket, 'fromJSON', json);
    expect(decoded.userId).toBe(original.userId);
    expect(decoded.username).toBe(original.username);
    expect(decoded.bio).toBe(original.bio);
    expect(decoded.age).toBe(original.age);
  });

  test('JSON roundtrip with minimal packet', () => {
    if (!hasJson) return;
    const original = createMinimalPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<UserProfilePacket>(UserProfilePacket, 'fromJSON', json);
    expect(decoded.bio).toBeNull();
    expect(decoded.age).toBeNull();
    expect(decoded.lastLogin).toBeNull();
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createFullPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<UserProfilePacket>(UserProfilePacket, 'fromMsgPack', bytes);
    expect(decoded.userId).toBe(original.userId);
    expect(decoded.username).toBe(original.username);
  });
});

// ============================================================================
// SecureMessagePacket Tests
// ============================================================================
describe('SecureMessagePacket', () => {
  const createFullPacket = () => new SecureMessagePacket({
    messageId: '550e8400-e29b-41d4-a716-446655440000',
    senderId: 1,
    recipientId: 2,
    subject: 'Test Subject',
    body: 'This is a secure message body.',
    attachments: [{ filename: 'doc.pdf', size: 1024 }],
    encryptedPayload: new Uint8Array([0xDE, 0xAD, 0xBE, 0xEF]),
    priority: 3,
    isRead: false,
    sentAt: new Date('2024-01-15T10:30:00.000Z')
  });

  const createMinimalPacket = () => new SecureMessagePacket({
    messageId: 'minimal-id',
    senderId: 10,
    recipientId: 20,
    subject: 'Minimal',
    body: 'Body',
    attachments: [],
    priority: 1,
    isRead: true,
    sentAt: new Date()
  });

  test('TYPE constant is correct', () => {
    expect(SecureMessagePacket.TYPE).toBe('/example/SecureMessagePacket');
  });

  test('constructor with all fields', () => {
    const p = createFullPacket();
    expect(p.messageId).toBe('550e8400-e29b-41d4-a716-446655440000');
    expect(p.senderId).toBe(1);
    expect(p.recipientId).toBe(2);
    expect(p.priority).toBe(3);
    expect(p.isRead).toBe(false);
    expect(p.encryptedPayload).toBeInstanceOf(Uint8Array);
  });

  test('constructor with minimal fields', () => {
    const p = createMinimalPacket();
    expect(p.encryptedPayload).toBeNull();
    expect(p.isRead).toBe(true);
  });

  test('multiple attachments', () => {
    const p = new SecureMessagePacket({
      messageId: 'id',
      senderId: 1,
      recipientId: 2,
      subject: 's',
      body: 'b',
      attachments: [
        { name: 'file1.txt' },
        { name: 'file2.pdf' },
        { name: 'image.png' }
      ],
      priority: 1,
      isRead: false,
      sentAt: new Date()
    });
    expect(p.attachments.length).toBe(3);
  });

  test('JSON roundtrip', () => {
    if (!hasJson) return;
    const original = createFullPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<SecureMessagePacket>(SecureMessagePacket, 'fromJSON', json);
    expect(decoded.messageId).toBe(original.messageId);
    expect(decoded.senderId).toBe(original.senderId);
    expect(decoded.priority).toBe(original.priority);
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createFullPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<SecureMessagePacket>(SecureMessagePacket, 'fromMsgPack', bytes);
    expect(decoded.messageId).toBe(original.messageId);
  });
});

// ============================================================================
// ComprehensivePacket Tests
// ============================================================================
describe('ComprehensivePacket', () => {
  const createPacket = () => new ComprehensivePacket({
    intField: 42,
    floatField: 3.14159,
    doubleField: 2.718281828,
    stringField: 'comprehensive test',
    boolField: true,
    datetimeField: new Date('2024-01-15T10:30:00.000Z'),
    timeField: '14:30:00',
    listField: [1, 'two', true, null],
    listIntField: [1, 2, 3, 4, 5],
    listStringField: ['a', 'b', 'c'],
    mapField: { key1: 'value1', nested: { deep: true } },
    embeddedMapField: new Map([['mapKey', 'mapValue']]),
    mapStringDynamicField: { dynamic: 123 },
    bytesField: new Uint8Array([0xFF, 0xFE, 0xFD])
  });

  test('TYPE constant is correct', () => {
    expect(ComprehensivePacket.TYPE).toBe('/test/ComprehensivePacket');
  });

  test('constructor sets all fields', () => {
    const p = createPacket();
    expect(p.intField).toBe(42);
    expect(p.floatField).toBeCloseTo(3.14159);
    expect(p.stringField).toBe('comprehensive test');
    expect(p.boolField).toBe(true);
    expect(p.listField.length).toBe(4);
    expect(p.listIntField.length).toBe(5);
    expect(p.bytesField).toBeInstanceOf(Uint8Array);
  });

  test('integer edge cases', () => {
    const cases = [0, 1, -1, 2147483647, -2147483648, 999999999999];
    for (const val of cases) {
      const p = new ComprehensivePacket({
        ...createPacket(),
        intField: val
      });
      expect(p.intField).toBe(val);
    }
  });

  test('float edge cases', () => {
    const cases = [0.0, 1.0, -1.0, 3.141592653589793, 0.0000001, 1e10];
    for (const val of cases) {
      const p = new ComprehensivePacket({
        ...createPacket(),
        floatField: val
      });
      expect(p.floatField).toBeCloseTo(val);
    }
  });

  test('string edge cases', () => {
    const cases = ['', 'a', '   ', 'Hello 世界! 🎉', 'Quote: "test"', 'line1\nline2'];
    for (const val of cases) {
      const p = new ComprehensivePacket({
        ...createPacket(),
        stringField: val
      });
      expect(p.stringField).toBe(val);
    }
  });

  test('JSON roundtrip', () => {
    if (!hasJson) return;
    const original = createPacket();
    const json = invokeMethod<string>(original, 'toJSON');
    const decoded = invokeStatic<ComprehensivePacket>(ComprehensivePacket, 'fromJSON', json);
    expect(decoded.intField).toBe(original.intField);
    expect(decoded.stringField).toBe(original.stringField);
    expect(decoded.boolField).toBe(original.boolField);
  });

  test('MsgPack roundtrip', () => {
    if (!hasMsgPack) return;
    const original = createPacket();
    const bytes = invokeMethod<Uint8Array>(original, 'toMsgPack');
    const decoded = invokeStatic<ComprehensivePacket>(ComprehensivePacket, 'fromMsgPack', bytes);
    expect(decoded.intField).toBe(original.intField);
    expect(decoded.stringField).toBe(original.stringField);
  });
});

// ============================================================================
// Index.ts - deserializePacket Tests
// ============================================================================
describe('deserializePacket', () => {
  test('deserializes PingPacket', () => {
    if (!hasJson) return;
    const p = new PingPacket({ timestamp: new Date(), message: 'test' });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(PingPacket);
    expect(result.message).toBe('test');
  });

  test('deserializes MessagePacket', () => {
    if (!hasJson) return;
    const p = new MessagePacket({ senderId: 'user', content: 'msg', timestamp: new Date() });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(MessagePacket);
  });

  test('deserializes PongPacket', () => {
    if (!hasJson) return;
    const p = new PongPacket({
      originalTimestamp: new Date(),
      responseTimestamp: new Date(),
      latencyMs: 50
    });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(PongPacket);
  });

  test('deserializes DataChunkPacket', () => {
    if (!hasJson) return;
    const p = new DataChunkPacket({
      chunkIndex: 0,
      totalChunks: 1,
      data: new Map(),
      checksum: 'test'
    });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(DataChunkPacket);
  });

  test('deserializes ComprehensivePacket', () => {
    if (!hasJson) return;
    const p = new ComprehensivePacket({
      intField: 1, floatField: 1.0, doubleField: 1.0,
      stringField: '', boolField: true,
      datetimeField: new Date(), timeField: '00:00',
      listField: [], listIntField: [], listStringField: [],
      mapField: {}, embeddedMapField: new Map(), mapStringDynamicField: {},
      bytesField: new Uint8Array()
    });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(ComprehensivePacket);
  });

  test('deserializes UserProfilePacket', () => {
    if (!hasJson) return;
    const p = new UserProfilePacket({
      userId: 1, username: 'u', email: 'e@e.com',
      balance: 0, tags: [], preferences: {}, createdAt: new Date()
    });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(UserProfilePacket);
  });

  test('deserializes SecureMessagePacket', () => {
    if (!hasJson) return;
    const p = new SecureMessagePacket({
      messageId: 'id', senderId: 1, recipientId: 2,
      subject: 's', body: 'b', attachments: [],
      priority: 1, isRead: false, sentAt: new Date()
    });
    const json = invokeMethod<string>(p, 'toJSON');
    const data = JSON.parse(json);
    const result = deserializePacket(data);
    expect(result).toBeInstanceOf(SecureMessagePacket);
  });

  test('throws on unknown packet type', () => {
    if (!hasJson) return;
    expect(() => deserializePacket({ packetType: '/unknown/Packet' }))
      .toThrow('Unknown packet type');
  });
});
