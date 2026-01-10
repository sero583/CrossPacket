<?php
/**
 * CrossPacket - PHP Unit Tests using PHPUnit
 *
 * Author: Serhat Gueler (sero583)
 * GitHub: https://github.com/sero583
 * License: MIT
 */

declare(strict_types=1);

namespace CrossPacket\Tests;

use PHPUnit\Framework\TestCase;
use App\DataPackets\PingPacket;
use App\DataPackets\PongPacket;
use App\DataPackets\MessagePacket;
use App\DataPackets\DataChunkPacket;
use App\DataPackets\UserProfilePacket;
use App\DataPackets\SecureMessagePacket;
use App\DataPackets\ComprehensivePacket;
use DateTimeImmutable;

class PacketTest extends TestCase
{
    private static bool $hasJson;
    private static bool $hasMsgPack;

    public static function setUpBeforeClass(): void
    {
        // Use reflection to detect available methods at runtime
        // This allows tests to pass in JSON_ONLY, MSGPACK_ONLY, and BOTH modes
        self::$hasJson = method_exists(PingPacket::class, 'toJson');
        self::$hasMsgPack = method_exists(PingPacket::class, 'toMsgPack');
        echo "JSON methods available: " . (self::$hasJson ? 'yes' : 'no') . "\n";
        echo "MsgPack methods available: " . (self::$hasMsgPack ? 'yes' : 'no') . "\n";
    }

    private function skipIfNoJson(): void
    {
        if (!self::$hasJson) {
            $this->markTestSkipped('JSON methods not available (MSGPACK_ONLY mode)');
        }
    }

    private function skipIfNoMsgPack(): void
    {
        if (!self::$hasMsgPack) {
            $this->markTestSkipped('MsgPack methods not available (JSON_ONLY mode)');
        }
    }

    // ============================================================================
    // PingPacket Tests
    // ============================================================================
    public function testPingPacketTypeConstant(): void
    {
        $this->assertSame('/example/PingPacket', PingPacket::TYPE);
    }

    public function testPingPacketConstructor(): void
    {
        $ts = new DateTimeImmutable();
        $p = new PingPacket($ts, 'hello');
        $this->assertSame('hello', $p->getMessage());
        $this->assertNotNull($p->getTimestamp());
    }

    public function testPingPacketSetters(): void
    {
        $p = new PingPacket();
        $p->setMessage('setter test');
        $p->setTimestamp(new DateTimeImmutable());
        $this->assertSame('setter test', $p->getMessage());
    }

    public function testPingPacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new PingPacket(new DateTimeImmutable('2024-01-15T10:30:00+00:00'), 'json test');
        $json = $original->toJson();
        $decoded = PingPacket::fromJson($json);
        $this->assertSame($original->getMessage(), $decoded->getMessage());
    }

    public function testPingPacketJsonSerialize(): void
    {
        $this->skipIfNoJson();
        $p = new PingPacket(new DateTimeImmutable(), 'test');
        $arr = $p->jsonSerialize();
        $this->assertArrayHasKey('packetType', $arr);
        $this->assertSame('/example/PingPacket', $arr['packetType']);
    }

    public function testPingPacketNullFields(): void
    {
        $p = new PingPacket();
        $this->assertNull($p->getTimestamp());
        $this->assertNull($p->getMessage());
    }

    public function testPingPacketFluentSetters(): void
    {
        $p = (new PingPacket())
            ->setTimestamp(new DateTimeImmutable())
            ->setMessage('fluent');
        $this->assertSame('fluent', $p->getMessage());
    }

    // ============================================================================
    // PongPacket Tests
    // ============================================================================
    public function testPongPacketTypeConstant(): void
    {
        $this->assertSame('/example/PongPacket', PongPacket::TYPE);
    }

    public function testPongPacketConstructor(): void
    {
        $ts = new DateTimeImmutable();
        $p = new PongPacket($ts, $ts, 150);
        $this->assertSame(150, $p->getLatencyMs());
    }

    public function testPongPacketZeroLatency(): void
    {
        $ts = new DateTimeImmutable();
        $p = new PongPacket($ts, $ts, 0);
        $this->assertSame(0, $p->getLatencyMs());
    }

    public function testPongPacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new PongPacket(
            new DateTimeImmutable('2024-04-01T10:00:00+00:00'),
            new DateTimeImmutable('2024-04-01T10:00:00.025+00:00'),
            25
        );
        $json = $original->toJson();
        $decoded = PongPacket::fromJson($json);
        $this->assertSame($original->getLatencyMs(), $decoded->getLatencyMs());
    }

    public function testPongPacketSetters(): void
    {
        $p = new PongPacket();
        $p->setOriginalTimestamp(new DateTimeImmutable());
        $p->setResponseTimestamp(new DateTimeImmutable());
        $p->setLatencyMs(100);
        $this->assertSame(100, $p->getLatencyMs());
    }

    // ============================================================================
    // MessagePacket Tests
    // ============================================================================
    public function testMessagePacketTypeConstant(): void
    {
        $this->assertSame('/chat/MessagePacket', MessagePacket::TYPE);
    }

    public function testMessagePacketConstructor(): void
    {
        $m = new MessagePacket('user123', 'Hello, World!', new DateTimeImmutable());
        $this->assertSame('user123', $m->getSenderId());
        $this->assertSame('Hello, World!', $m->getContent());
    }

    public function testMessagePacketEmptyStrings(): void
    {
        $m = new MessagePacket('', '', new DateTimeImmutable());
        $this->assertSame('', $m->getSenderId());
        $this->assertSame('', $m->getContent());
    }

    public function testMessagePacketUnicode(): void
    {
        $unicodeContent = 'Hello 世界! Émoji: 🎉🚀💻';
        $m = new MessagePacket('unicode_sender', $unicodeContent, new DateTimeImmutable());
        $this->assertSame($unicodeContent, $m->getContent());
    }

    public function testMessagePacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new MessagePacket('sender_abc', 'JSON test content', new DateTimeImmutable('2024-01-15T10:30:00+00:00'));
        $json = $original->toJson();
        $decoded = MessagePacket::fromJson($json);
        $this->assertSame($original->getSenderId(), $decoded->getSenderId());
        $this->assertSame($original->getContent(), $decoded->getContent());
    }

    public function testMessagePacketSetters(): void
    {
        $m = new MessagePacket();
        $m->setSenderId('setter_test');
        $m->setContent('test content');
        $m->setTimestamp(new DateTimeImmutable());
        $this->assertSame('setter_test', $m->getSenderId());
        $this->assertSame('test content', $m->getContent());
    }

    // ============================================================================
    // DataChunkPacket Tests
    // ============================================================================
    public function testDataChunkPacketTypeConstant(): void
    {
        $this->assertSame('/example/DataChunkPacket', DataChunkPacket::TYPE);
    }

    public function testDataChunkPacketConstructor(): void
    {
        $p = new DataChunkPacket(0, 10, ['key' => 'value'], 'abc123');
        $this->assertSame(0, $p->getChunkIndex());
        $this->assertSame(10, $p->getTotalChunks());
        $this->assertSame('abc123', $p->getChecksum());
    }

    public function testDataChunkPacketEmptyMap(): void
    {
        $p = new DataChunkPacket(5, 5, [], '');
        $this->assertIsArray($p->getData());
        $this->assertEmpty($p->getData());
    }

    public function testDataChunkPacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new DataChunkPacket(2, 5, ['test' => 'value'], 'json_checksum');
        $json = $original->toJson();
        $decoded = DataChunkPacket::fromJson($json);
        $this->assertSame($original->getChunkIndex(), $decoded->getChunkIndex());
        $this->assertSame($original->getTotalChunks(), $decoded->getTotalChunks());
        $this->assertSame($original->getChecksum(), $decoded->getChecksum());
    }

    public function testDataChunkPacketSetters(): void
    {
        $p = new DataChunkPacket();
        $p->setChunkIndex(3);
        $p->setTotalChunks(10);
        $p->setData(['key' => 'value']);
        $p->setChecksum('test_checksum');
        $this->assertSame(3, $p->getChunkIndex());
        $this->assertSame(10, $p->getTotalChunks());
        $this->assertSame('test_checksum', $p->getChecksum());
    }

    public function testDataChunkPacketComplexData(): void
    {
        $data = ['nested' => ['array' => [1, 2, 3]], 'key' => 'value'];
        $p = new DataChunkPacket(0, 1, $data, 'hash');
        $this->assertEquals($data, $p->getData());
    }

    // ============================================================================
    // UserProfilePacket Tests (using positional args - snake_case params)
    // ============================================================================
    public function testUserProfilePacketTypeConstant(): void
    {
        $this->assertSame('/example/UserProfilePacket', UserProfilePacket::TYPE);
    }

    public function testUserProfilePacketFullConstructor(): void
    {
        // Using positional arguments in correct order
        $p = new UserProfilePacket(
            12345,             // user_id
            'testuser',        // username
            'test@example.com',// email
            'This is my bio',  // bio
            25,                // age
            100.50,            // balance
            ['developer', 'gamer'],  // tags
            ['theme' => 'dark'],     // preferences
            null,              // avatar
            new DateTimeImmutable(), // created_at
            new DateTimeImmutable()  // last_login
        );
        $this->assertSame(12345, $p->getUserId());
        $this->assertSame('testuser', $p->getUsername());
        $this->assertSame('This is my bio', $p->getBio());
        $this->assertSame(25, $p->getAge());
        $this->assertEqualsWithDelta(100.50, $p->getBalance(), 0.01);
    }

    public function testUserProfilePacketNullOptionalFields(): void
    {
        // Testing with null optional fields
        $p = new UserProfilePacket(
            1,
            'minimaluser',
            'minimal@test.com',
            null,  // bio
            null,  // age
            0.0,   // balance
            [],    // tags
            [],    // preferences
            null,  // avatar
            new DateTimeImmutable(),
            null   // last_login
        );
        $this->assertNull($p->getBio());
        $this->assertNull($p->getAge());
        $this->assertNull($p->getLastLogin());
    }

    public function testUserProfilePacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new UserProfilePacket(
            999,
            'jsonuser',
            'json@example.com',
            'JSON bio',
            30,
            250.75,
            ['json', 'test'],
            ['key' => 'value'],
            null,
            new DateTimeImmutable('2024-05-01T12:00:00+00:00'),
            new DateTimeImmutable('2024-05-15T18:30:00+00:00')
        );
        $json = $original->toJson();
        $decoded = UserProfilePacket::fromJson($json);
        $this->assertSame($original->getUserId(), $decoded->getUserId());
        $this->assertSame($original->getUsername(), $decoded->getUsername());
        $this->assertSame($original->getBio(), $decoded->getBio());
        $this->assertSame($original->getAge(), $decoded->getAge());
    }

    public function testUserProfilePacketSetters(): void
    {
        $p = new UserProfilePacket();
        $p->setUserId(42);
        $p->setUsername('setteruser');
        $p->setEmail('setter@test.com');
        $p->setBio('Bio via setter');
        $p->setAge(20);
        $p->setBalance(50.0);
        $p->setTags(['tag1']);
        $p->setPreferences(['pref' => 'val']);
        $p->setCreatedAt(new DateTimeImmutable());

        $this->assertSame(42, $p->getUserId());
        $this->assertSame('setteruser', $p->getUsername());
        $this->assertSame('Bio via setter', $p->getBio());
        $this->assertSame(20, $p->getAge());
    }

    // ============================================================================
    // SecureMessagePacket Tests
    // ============================================================================
    public function testSecureMessagePacketTypeConstant(): void
    {
        $this->assertSame('/example/SecureMessagePacket', SecureMessagePacket::TYPE);
    }

    public function testSecureMessagePacketFullConstructor(): void
    {
        $p = new SecureMessagePacket(
            '550e8400-e29b-41d4-a716-446655440000', // message_id
            1,                       // sender_id
            2,                       // recipient_id
            'Test Subject',          // subject
            'Secure message body',   // body
            [['filename' => 'doc.pdf', 'size' => 1024]], // attachments
            'DEADBEEF',              // encrypted_payload
            3,                       // priority
            false,                   // is_read
            new DateTimeImmutable()  // sent_at
        );
        $this->assertSame('550e8400-e29b-41d4-a716-446655440000', $p->getMessageId());
        $this->assertSame(1, $p->getSenderId());
        $this->assertSame(2, $p->getRecipientId());
        $this->assertSame(3, $p->getPriority());
        $this->assertFalse($p->getIsRead());
    }

    public function testSecureMessagePacketNullPayload(): void
    {
        $p = new SecureMessagePacket(
            'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            10,
            20,
            'Unencrypted',
            'No encryption here',
            [],
            null,  // encrypted_payload
            1,
            true,
            new DateTimeImmutable()
        );
        $this->assertNull($p->getEncryptedPayload());
        $this->assertTrue($p->getIsRead());
    }

    public function testSecureMessagePacketPriorityBoundaries(): void
    {
        $ts = new DateTimeImmutable();
        $p1 = new SecureMessagePacket('id1', 1, 1, 's', 'b', [], null, 1, false, $ts);
        $p5 = new SecureMessagePacket('id5', 1, 1, 's', 'b', [], null, 5, false, $ts);
        $this->assertSame(1, $p1->getPriority());
        $this->assertSame(5, $p5->getPriority());
    }

    public function testSecureMessagePacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new SecureMessagePacket(
            'aaaabbbb-cccc-dddd-eeee-ffffffffffff',
            100,
            200,
            'JSON Test',
            'Testing JSON serialization',
            [['test' => 'data']],
            null,
            5,
            true,
            new DateTimeImmutable('2024-09-01T09:00:00+00:00')
        );
        $json = $original->toJson();
        $decoded = SecureMessagePacket::fromJson($json);
        $this->assertSame($original->getMessageId(), $decoded->getMessageId());
        $this->assertSame($original->getSenderId(), $decoded->getSenderId());
        $this->assertSame($original->getSubject(), $decoded->getSubject());
        $this->assertSame($original->getPriority(), $decoded->getPriority());
    }

    public function testSecureMessagePacketSetters(): void
    {
        $p = new SecureMessagePacket();
        $p->setMessageId('test-uuid');
        $p->setSenderId(5);
        $p->setRecipientId(10);
        $p->setSubject('Subject');
        $p->setBody('Body');
        $p->setAttachments([]);
        $p->setPriority(2);
        $p->setIsRead(true);
        $p->setSentAt(new DateTimeImmutable());

        $this->assertSame('test-uuid', $p->getMessageId());
        $this->assertSame(5, $p->getSenderId());
        $this->assertSame('Subject', $p->getSubject());
        $this->assertTrue($p->getIsRead());
    }

    // ============================================================================
    // ComprehensivePacket Tests
    // ============================================================================
    public function testComprehensivePacketTypeConstant(): void
    {
        $this->assertSame('/test/ComprehensivePacket', ComprehensivePacket::TYPE);
    }

    public function testComprehensivePacketFullConstructor(): void
    {
        $p = new ComprehensivePacket(
            42,                      // int_field
            3.14159,                 // float_field
            2.718281828,             // double_field
            'comprehensive test',    // string_field
            true,                    // bool_field
            new DateTimeImmutable(), // datetime_field
            '14:30',                 // time_field
            [1, 'two', true],        // list_field
            [1, 2, 3, 4, 5],         // list_int_field
            ['a', 'b', 'c'],         // list_string_field
            ['key1' => 'value1'],    // map_field
            ['mapKey' => 'mapValue'],// embedded_map_field
            ['dynamic' => 123],      // map_string_dynamic_field
            'FFFE'                   // bytes_field
        );
        $this->assertSame(42, $p->getIntField());
        $this->assertSame('comprehensive test', $p->getStringField());
        $this->assertTrue($p->getBoolField());
    }

    // Integer edge cases
    /**
     * @dataProvider integerEdgeCasesProvider
     */
    public function testComprehensivePacketIntegerEdgeCases(int $value): void
    {
        $p = new ComprehensivePacket($value);
        $this->assertSame($value, $p->getIntField());
    }

    public static function integerEdgeCasesProvider(): array
    {
        return [
            'zero' => [0],
            'one' => [1],
            'negative' => [-1],
            'max_32' => [2147483647],
            'min_32' => [-2147483648],
        ];
    }

    // Float edge cases
    /**
     * @dataProvider floatEdgeCasesProvider
     */
    public function testComprehensivePacketFloatEdgeCases(float $value): void
    {
        $p = new ComprehensivePacket(null, $value);
        $this->assertEqualsWithDelta($value, $p->getFloatField(), 1e-10);
    }

    public static function floatEdgeCasesProvider(): array
    {
        return [
            'zero' => [0.0],
            'pi' => [3.141592653589793],
            'small' => [0.0000001],
            'large' => [1e10],
        ];
    }

    // String edge cases
    /**
     * @dataProvider stringEdgeCasesProvider
     */
    public function testComprehensivePacketStringEdgeCases(string $value): void
    {
        $p = new ComprehensivePacket(null, null, null, $value);
        $this->assertSame($value, $p->getStringField());
    }

    public static function stringEdgeCasesProvider(): array
    {
        return [
            'empty' => [''],
            'unicode' => ['Hello 世界! 🎉'],
            'special' => ['Quote: "test" Backslash: \\'],
        ];
    }

    // Boolean edge cases
    /**
     * @dataProvider booleanEdgeCasesProvider
     */
    public function testComprehensivePacketBooleanEdgeCases(bool $value): void
    {
        $p = new ComprehensivePacket(null, null, null, null, $value);
        $this->assertSame($value, $p->getBoolField());
    }

    public static function booleanEdgeCasesProvider(): array
    {
        return [
            'true' => [true],
            'false' => [false],
        ];
    }

    public function testComprehensivePacketListFields(): void
    {
        $p = new ComprehensivePacket(
            null, null, null, null, null, null, null,
            [1, 'two', true, null],   // list_field
            [-100, 0, 100],           // list_int_field
            ['', 'a', '日本語']        // list_string_field
        );
        $this->assertCount(4, $p->getListField());
        $this->assertCount(3, $p->getListIntField());
        $this->assertCount(3, $p->getListStringField());
    }

    public function testComprehensivePacketMapFields(): void
    {
        $p = new ComprehensivePacket(
            null, null, null, null, null, null, null, null, null, null,
            ['a' => 1, 'b' => 'two', 'c' => true],  // map_field
            ['key' => 'value'],                     // embedded_map_field
            ['str' => 'text', 'int' => 42, 'bool' => true]  // map_string_dynamic_field
        );
        $this->assertCount(3, $p->getMapField());
        $this->assertCount(1, $p->getEmbeddedMapField());
        $this->assertCount(3, $p->getMapStringDynamicField());
    }

    public function testComprehensivePacketBytesField(): void
    {
        $bytesHex = 'DEADBEEF';
        $p = new ComprehensivePacket(
            null, null, null, null, null, null, null, null, null, null, null, null, null,
            $bytesHex
        );
        $this->assertSame($bytesHex, $p->getBytesField());
    }

    public function testComprehensivePacketJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $original = new ComprehensivePacket(
            123456,
            1.5,
            2.5,
            'json roundtrip test',
            true,
            new DateTimeImmutable('2024-12-25T00:00:00+00:00'),
            '12:30',
            [1, 'two', true],
            [10, 20, 30],
            ['x', 'y', 'z'],
            ['a' => 1, 'b' => 2],
            ['key' => 'val'],
            ['dynamic' => true],
            '0B161F'
        );
        $json = $original->toJson();
        $decoded = ComprehensivePacket::fromJson($json);
        $this->assertSame($original->getIntField(), $decoded->getIntField());
        $this->assertSame($original->getStringField(), $decoded->getStringField());
        $this->assertSame($original->getBoolField(), $decoded->getBoolField());
    }

    public function testComprehensivePacketSetters(): void
    {
        $p = new ComprehensivePacket();
        $p->setIntField(100);
        $p->setFloatField(1.5);
        $p->setDoubleField(2.5);
        $p->setStringField('test');
        $p->setBoolField(true);
        $p->setDatetimeField(new DateTimeImmutable());
        $p->setTimeField('10:00');
        $p->setListField([1, 2]);
        $p->setListIntField([1, 2, 3]);
        $p->setListStringField(['a', 'b']);
        $p->setMapField(['k' => 'v']);
        $p->setEmbeddedMapField(['e' => 'v']);
        $p->setMapStringDynamicField(['d' => 1]);
        $p->setBytesField('FF');

        $this->assertSame(100, $p->getIntField());
        $this->assertSame('test', $p->getStringField());
        $this->assertTrue($p->getBoolField());
        $this->assertSame('FF', $p->getBytesField());
    }

    // ============================================================================
    // Edge Case Tests
    // ============================================================================
    public function testVeryLongString(): void
    {
        $longString = str_repeat('x', 10000);
        $m = new MessagePacket('long_sender', $longString, new DateTimeImmutable());
        $this->assertSame(10000, strlen($m->getContent()));
    }

    public function testEpochDate(): void
    {
        $epoch = new DateTimeImmutable('1970-01-01T00:00:00+00:00');
        $p = new PingPacket($epoch, 'epoch test');
        $this->assertSame(0, $p->getTimestamp()->getTimestamp());
    }

    public function testFarFutureDate(): void
    {
        $future = new DateTimeImmutable('2099-12-31T23:59:59+00:00');
        $p = new PingPacket($future, 'future test');
        $this->assertSame(2099, (int)$p->getTimestamp()->format('Y'));
    }

    public function testLargeInteger(): void
    {
        $largeInt = 9007199254740991; // MAX_SAFE_INTEGER equivalent
        $p = new UserProfilePacket($largeInt, 'large', 'large@test.com');
        $this->assertSame($largeInt, $p->getUserId());
    }

    public function testCjkUnicodeJsonRoundtrip(): void
    {
        $this->skipIfNoJson();
        $unicodeContent = '日本語テスト 中文测试 한국어 테스트';
        $original = new MessagePacket('cjk_sender', $unicodeContent, new DateTimeImmutable());
        $json = $original->toJson();
        $decoded = MessagePacket::fromJson($json);
        $this->assertSame($unicodeContent, $decoded->getContent());
    }

    public function testEmptyObjectConstruction(): void
    {
        // All packets should be constructable with no args
        $ping = new PingPacket();
        $pong = new PongPacket();
        $msg = new MessagePacket();
        $chunk = new DataChunkPacket();
        $user = new UserProfilePacket();
        $secure = new SecureMessagePacket();
        $comp = new ComprehensivePacket();

        $this->assertInstanceOf(PingPacket::class, $ping);
        $this->assertInstanceOf(PongPacket::class, $pong);
        $this->assertInstanceOf(MessagePacket::class, $msg);
        $this->assertInstanceOf(DataChunkPacket::class, $chunk);
        $this->assertInstanceOf(UserProfilePacket::class, $user);
        $this->assertInstanceOf(SecureMessagePacket::class, $secure);
        $this->assertInstanceOf(ComprehensivePacket::class, $comp);
    }

    public function testNullTimestampInJsonSerialize(): void
    {
        $this->skipIfNoJson();
        $p = new PingPacket(null, 'no timestamp');
        $arr = $p->jsonSerialize();
        $this->assertNull($arr['timestamp']);
    }

    public function testSpecialCharactersInMessage(): void
    {
        $this->skipIfNoJson();
        $special = '<script>alert("xss")</script>';
        $m = new MessagePacket('xss_test', $special, new DateTimeImmutable());
        $json = $m->toJson();
        $decoded = MessagePacket::fromJson($json);
        $this->assertSame($special, $decoded->getContent());
    }

    public function testNestedArrayInDataChunk(): void
    {
        $this->skipIfNoJson();
        $nested = [
            'level1' => [
                'level2' => [
                    'level3' => ['value']
                ]
            ]
        ];
        $p = new DataChunkPacket(0, 1, $nested, 'nested');
        $json = $p->toJson();
        $decoded = DataChunkPacket::fromJson($json);
        $this->assertEquals($nested, $decoded->getData());
    }

    public function testAllPacketTypesHaveTypeConstant(): void
    {
        $this->assertNotEmpty(PingPacket::TYPE);
        $this->assertNotEmpty(PongPacket::TYPE);
        $this->assertNotEmpty(MessagePacket::TYPE);
        $this->assertNotEmpty(DataChunkPacket::TYPE);
        $this->assertNotEmpty(UserProfilePacket::TYPE);
        $this->assertNotEmpty(SecureMessagePacket::TYPE);
        $this->assertNotEmpty(ComprehensivePacket::TYPE);
    }

    // ============================================================================
    // MessagePack Tests (msgpack extension not installed, but test methods exist)
    // ============================================================================
    public function testPingPacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new PingPacket(new DateTimeImmutable(), 'test');
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testPongPacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new PongPacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testMessagePacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new MessagePacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testDataChunkPacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new DataChunkPacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testUserProfilePacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new UserProfilePacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testSecureMessagePacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new SecureMessagePacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    public function testComprehensivePacketMsgPackMethodsExist(): void
    {
        $this->skipIfNoMsgPack();
        $p = new ComprehensivePacket();
        $this->assertTrue(method_exists($p, 'toMsgPack'));
        $this->assertTrue(method_exists($p, 'fromMsgPack'));
    }

    // ============================================================================
    // MsgPack Roundtrip Tests (only run when msgpack extension is available)
    // ============================================================================
    public function testPingPacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new PingPacket(new DateTimeImmutable('2024-06-15T10:30:00+00:00'), 'msgpack test');
        $packed = $original->toMsgPack();
        $this->assertIsString($packed);
        $decoded = PingPacket::fromMsgPack($packed);
        $this->assertSame($original->getMessage(), $decoded->getMessage());
    }

    public function testPongPacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new PongPacket(
            new DateTimeImmutable('2024-01-01T00:00:00+00:00'),
            new DateTimeImmutable('2024-01-01T00:00:00.150+00:00'),
            150
        );
        $packed = $original->toMsgPack();
        $decoded = PongPacket::fromMsgPack($packed);
        $this->assertSame($original->getLatencyMs(), $decoded->getLatencyMs());
    }

    public function testMessagePacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new MessagePacket('sender123', 'Hello MsgPack! 🚀', new DateTimeImmutable());
        $packed = $original->toMsgPack();
        $decoded = MessagePacket::fromMsgPack($packed);
        $this->assertSame($original->getSenderId(), $decoded->getSenderId());
        $this->assertSame($original->getContent(), $decoded->getContent());
    }

    public function testDataChunkPacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new DataChunkPacket(3, 10, ['nested' => ['key' => 'value']], 'checksum123');
        $packed = $original->toMsgPack();
        $decoded = DataChunkPacket::fromMsgPack($packed);
        $this->assertSame($original->getChunkIndex(), $decoded->getChunkIndex());
        $this->assertSame($original->getTotalChunks(), $decoded->getTotalChunks());
        $this->assertSame($original->getChecksum(), $decoded->getChecksum());
    }

    public function testUserProfilePacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new UserProfilePacket(
            12345,
            'msgpackuser',
            'msgpack@example.com',
            'MsgPack bio',
            30,
            250.50,
            ['tag1', 'tag2'],
            ['theme' => 'dark'],
            'avatar_data',
            new DateTimeImmutable()
        );
        $packed = $original->toMsgPack();
        $decoded = UserProfilePacket::fromMsgPack($packed);
        $this->assertSame($original->getUserId(), $decoded->getUserId());
        $this->assertSame($original->getUsername(), $decoded->getUsername());
        $this->assertSame($original->getEmail(), $decoded->getEmail());
    }

    public function testSecureMessagePacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new SecureMessagePacket(
            'uuid-msgpack-001',
            1,
            2,
            'MsgPack Subject',
            'MsgPack body text',
            [['filename' => 'file.pdf']],
            'encrypted_data',
            5,
            false,
            new DateTimeImmutable()
        );
        $packed = $original->toMsgPack();
        $decoded = SecureMessagePacket::fromMsgPack($packed);
        $this->assertSame($original->getMessageId(), $decoded->getMessageId());
        $this->assertSame($original->getSubject(), $decoded->getSubject());
    }

    public function testComprehensivePacketMsgPackRoundtrip(): void
    {
        $this->skipIfNoMsgPack();
        if (!function_exists('msgpack_pack')) {
            $this->markTestSkipped('msgpack extension not available');
        }
        $original = new ComprehensivePacket(
            42,
            3.14,
            2.718,
            'msgpack comprehensive',
            true,
            new DateTimeImmutable('2024-12-25T12:00:00+00:00'),
            '14:30',
            [1, 'two', true],
            [10, 20, 30],
            ['a', 'b', 'c'],
            ['key' => 'value'],
            ['embedded' => ['deep' => true]],
            ['dynamic' => 123],
            'binary_data'
        );
        $packed = $original->toMsgPack();
        $decoded = ComprehensivePacket::fromMsgPack($packed);
        $this->assertSame($original->getIntField(), $decoded->getIntField());
        $this->assertSame($original->getStringField(), $decoded->getStringField());
        $this->assertSame($original->getBoolField(), $decoded->getBoolField());
    }

    // ============================================================================
    // Additional coverage for fromJson with isset branches
    // ============================================================================
    public function testPingPacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Only timestamp
        $json = json_encode(['packetType' => PingPacket::TYPE, 'timestamp' => '2024-01-01T00:00:00+00:00']);
        $p = PingPacket::fromJson($json);
        $this->assertNotNull($p->getTimestamp());
        $this->assertNull($p->getMessage());

        // Only message
        $json2 = json_encode(['packetType' => PingPacket::TYPE, 'message' => 'hello']);
        $p2 = PingPacket::fromJson($json2);
        $this->assertNull($p2->getTimestamp());
        $this->assertSame('hello', $p2->getMessage());
    }

    public function testPongPacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Only original_timestamp
        $json = json_encode([
            'packetType' => PongPacket::TYPE,
            'original_timestamp' => '2024-01-01T00:00:00+00:00'
        ]);
        $p = PongPacket::fromJson($json);
        $this->assertNotNull($p->getOriginalTimestamp());

        // Only response_timestamp
        $json2 = json_encode([
            'packetType' => PongPacket::TYPE,
            'response_timestamp' => '2024-01-01T00:00:00+00:00'
        ]);
        $p2 = PongPacket::fromJson($json2);
        $this->assertNotNull($p2->getResponseTimestamp());

        // Only latency_ms
        $json3 = json_encode(['packetType' => PongPacket::TYPE, 'latency_ms' => 100]);
        $p3 = PongPacket::fromJson($json3);
        $this->assertSame(100, $p3->getLatencyMs());
    }

    public function testMessagePacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Individual fields
        $json = json_encode(['packetType' => MessagePacket::TYPE, 'sender_id' => 'test']);
        $p = MessagePacket::fromJson($json);
        $this->assertSame('test', $p->getSenderId());

        $json2 = json_encode(['packetType' => MessagePacket::TYPE, 'content' => 'hello']);
        $p2 = MessagePacket::fromJson($json2);
        $this->assertSame('hello', $p2->getContent());
    }

    public function testDataChunkPacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        $json = json_encode(['packetType' => DataChunkPacket::TYPE, 'chunk_index' => 5]);
        $p = DataChunkPacket::fromJson($json);
        $this->assertSame(5, $p->getChunkIndex());

        $json2 = json_encode(['packetType' => DataChunkPacket::TYPE, 'total_chunks' => 10]);
        $p2 = DataChunkPacket::fromJson($json2);
        $this->assertSame(10, $p2->getTotalChunks());

        $json3 = json_encode(['packetType' => DataChunkPacket::TYPE, 'checksum' => 'hash']);
        $p3 = DataChunkPacket::fromJson($json3);
        $this->assertSame('hash', $p3->getChecksum());
    }

    public function testUserProfilePacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Test each field individually to cover all isset branches
        $fields = [
            'user_id' => 1,
            'username' => 'user',
            'email' => 'test@test.com',
            'bio' => 'bio',
            'age' => 25,
            'balance' => 100.0,
            'tags' => ['a', 'b'],
            'preferences' => ['k' => 'v'],
            'avatar' => 'data',
            'created_at' => '2024-01-01T00:00:00+00:00',
            'last_login' => '2024-01-01T00:00:00+00:00'
        ];

        foreach ($fields as $field => $value) {
            $json = json_encode(['packetType' => UserProfilePacket::TYPE, $field => $value]);
            $p = UserProfilePacket::fromJson($json);
            $this->assertInstanceOf(UserProfilePacket::class, $p);
        }
    }

    public function testSecureMessagePacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Test each field individually
        $fields = [
            'message_id' => 'uuid',
            'sender_id' => 1,
            'recipient_id' => 2,
            'subject' => 'sub',
            'body' => 'text',
            'attachments' => [['file' => 'f.txt']],
            'encrypted_payload' => 'enc',
            'priority' => 3,
            'is_read' => true,
            'sent_at' => '2024-01-01T00:00:00+00:00'
        ];

        foreach ($fields as $field => $value) {
            $json = json_encode(['packetType' => SecureMessagePacket::TYPE, $field => $value]);
            $p = SecureMessagePacket::fromJson($json);
            $this->assertInstanceOf(SecureMessagePacket::class, $p);
        }
    }

    public function testComprehensivePacketFromJsonPartial(): void
    {
        $this->skipIfNoJson();
        // Test each field individually
        $fields = [
            'int_field' => 42,
            'float_field' => 3.14,
            'double_field' => 2.71,
            'string_field' => 'test',
            'bool_field' => true,
            'datetime_field' => '2024-01-01T00:00:00+00:00',
            'time_field' => '12:30',
            'list_field' => [1, 2, 3],
            'list_int_field' => [1, 2],
            'list_string_field' => ['a', 'b'],
            'map_field' => ['k' => 'v'],
            'embedded_map_field' => ['e' => 'v'],
            'map_string_dynamic_field' => ['d' => 1],
            'bytes_field' => 'FF'
        ];

        foreach ($fields as $field => $value) {
            $json = json_encode(['packetType' => ComprehensivePacket::TYPE, $field => $value]);
            $p = ComprehensivePacket::fromJson($json);
            $this->assertInstanceOf(ComprehensivePacket::class, $p);
        }
    }

    // Test nullable setters with null values
    public function testUserProfilePacketSettersWithNull(): void
    {
        $p = new UserProfilePacket();
        $p->setBio(null);
        $p->setAge(null);
        $p->setAvatar(null);
        $p->setLastLogin(null);
        
        $this->assertNull($p->getBio());
        $this->assertNull($p->getAge());
        $this->assertNull($p->getAvatar());
        $this->assertNull($p->getLastLogin());
    }

    public function testSecureMessagePacketSettersWithNull(): void
    {
        $p = new SecureMessagePacket();
        $p->setEncryptedPayload(null);
        $this->assertNull($p->getEncryptedPayload());
    }
}
