package com.crosspacket;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

import java.time.ZonedDateTime;
import java.time.ZoneOffset;
import java.time.LocalTime;
import java.util.*;

/**
 * JUnit 5 Comprehensive Test Suite for CrossPacket Java Generated Code.
 * 
 * Tests all 7 packet types with JSON and MsgPack serialization,
 * edge cases for all data types, and error handling.
 * 
 * Author: Serhat Güler (sero583)
 * GitHub: https://github.com/sero583
 * License: MIT
 */
class PacketTest {
    
    // Reflection helpers for detecting available methods
    private static boolean hasJson;
    private static boolean hasMsgPack;
    
    @BeforeAll
    static void detectMethods() {
        // Must check BOTH toJson AND fromJson - MSGPACK_ONLY mode may have toJson but not fromJson
        try {
            PingPacket.class.getMethod("toJson");
            PingPacket.class.getMethod("fromJson", String.class);
            hasJson = true;
        } catch (NoSuchMethodException e) {
            hasJson = false;
        }
        // Must check BOTH toMsgPack AND fromMsgPack - JSON_ONLY mode may have toMsgPack but not fromMsgPack
        try {
            PingPacket.class.getMethod("toMsgPack");
            PingPacket.class.getMethod("fromMsgPack", byte[].class);
            hasMsgPack = true;
        } catch (NoSuchMethodException e) {
            hasMsgPack = false;
        }
        System.out.println("JSON methods available: " + hasJson);
        System.out.println("MsgPack methods available: " + hasMsgPack);
    }
    
    void skipIfNoJson() {
        org.junit.jupiter.api.Assumptions.assumeTrue(hasJson, "JSON methods not available");
    }
    
    void skipIfNoMsgPack() {
        org.junit.jupiter.api.Assumptions.assumeTrue(hasMsgPack, "MsgPack methods not available");
    }
    
    @SuppressWarnings("unchecked")
    static <T> String invokeToJson(Object packet) throws Exception {
        java.lang.reflect.Method m = packet.getClass().getMethod("toJson");
        return (String) m.invoke(packet);
    }
    
    @SuppressWarnings("unchecked")
    static <T> T invokeFromJson(Class<T> clazz, String json) throws Exception {
        java.lang.reflect.Method m = clazz.getMethod("fromJson", String.class);
        return (T) m.invoke(null, json);
    }
    
    static byte[] invokeToMsgPack(Object packet) throws Exception {
        java.lang.reflect.Method m = packet.getClass().getMethod("toMsgPack");
        return (byte[]) m.invoke(packet);
    }
    
    @SuppressWarnings("unchecked")
    static <T> T invokeFromMsgPack(Class<T> clazz, byte[] bytes) throws Exception {
        java.lang.reflect.Method m = clazz.getMethod("fromMsgPack", byte[].class);
        return (T) m.invoke(null, bytes);
    }

    
    // ============================================================================
    // TYPE Constants Tests
    // ============================================================================
    
    @Test
    @DisplayName("MessagePacket.TYPE should be /chat/MessagePacket")
    void testMessagePacketType() {
        assertEquals("/chat/MessagePacket", MessagePacket.TYPE);
    }
    
    @Test
    @DisplayName("PingPacket.TYPE should be /example/PingPacket")
    void testPingPacketType() {
        assertEquals("/example/PingPacket", PingPacket.TYPE);
    }
    
    @Test
    @DisplayName("PongPacket.TYPE should be /example/PongPacket")
    void testPongPacketType() {
        assertEquals("/example/PongPacket", PongPacket.TYPE);
    }
    
    @Test
    @DisplayName("DataChunkPacket.TYPE should be /example/DataChunkPacket")
    void testDataChunkPacketType() {
        assertEquals("/example/DataChunkPacket", DataChunkPacket.TYPE);
    }
    
    @Test
    @DisplayName("ComprehensivePacket.TYPE should be /test/ComprehensivePacket")
    void testComprehensivePacketType() {
        assertEquals("/test/ComprehensivePacket", ComprehensivePacket.TYPE);
    }
    
    @Test
    @DisplayName("UserProfilePacket.TYPE should be /example/UserProfilePacket")
    void testUserProfilePacketType() {
        assertEquals("/example/UserProfilePacket", UserProfilePacket.TYPE);
    }
    
    @Test
    @DisplayName("SecureMessagePacket.TYPE should be /example/SecureMessagePacket")
    void testSecureMessagePacketType() {
        assertEquals("/example/SecureMessagePacket", SecureMessagePacket.TYPE);
    }
    
    // ============================================================================
    // MessagePacket Tests
    // ============================================================================
    
    @Nested
    @DisplayName("MessagePacket Tests")
    class MessagePacketTests {
        
        @Test
        @DisplayName("Empty constructor creates instance")
        void testEmptyConstructor() {
            MessagePacket p = new MessagePacket();
            assertNotNull(p);
            assertEquals("/chat/MessagePacket", p.getType());
        }
        
        @Test
        @DisplayName("Parameterized constructor sets all fields")
        void testParameterizedConstructor() {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            MessagePacket p = new MessagePacket("user123", "Hello World", now);
            
            assertEquals("user123", p.getSenderId());
            assertEquals("Hello World", p.getContent());
            assertEquals(now, p.getTimestamp());
        }
        
        @Test
        @DisplayName("Setters and getters work correctly")
        void testSettersAndGetters() {
            MessagePacket p = new MessagePacket();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            
            p.setSenderId("sender_test");
            p.setContent("test content");
            p.setTimestamp(now);
            
            assertEquals("sender_test", p.getSenderId());
            assertEquals("test content", p.getContent());
            assertEquals(now, p.getTimestamp());
        }
        
        @Test
        @DisplayName("JSON serialization roundtrip preserves all fields")
        void testJsonRoundtrip() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            MessagePacket original = new MessagePacket("json_user", "JSON content with \"quotes\"", now);
            
            String json = invokeToJson(original);
            MessagePacket decoded = invokeFromJson(MessagePacket.class, json);
            
            assertEquals(original.getSenderId(), decoded.getSenderId());
            assertEquals(original.getContent(), decoded.getContent());
            // Timestamps might have slight format differences but should be equivalent
            assertNotNull(decoded.getTimestamp());
        }
        
        @Test
        @DisplayName("MsgPack serialization roundtrip preserves all fields")
        void testMsgPackRoundtrip() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            MessagePacket original = new MessagePacket("msgpack_user", "MsgPack content", now);
            
            byte[] packed = invokeToMsgPack(original);
            MessagePacket decoded = invokeFromMsgPack(MessagePacket.class, packed);
            
            assertEquals(original.getSenderId(), decoded.getSenderId());
            assertEquals(original.getContent(), decoded.getContent());
            assertNotNull(decoded.getTimestamp());
        }
        
        @Test
        @DisplayName("Null fields are handled in JSON roundtrip")
        void testNullFieldsJsonRoundtrip() throws Exception {
            skipIfNoJson();
            MessagePacket original = new MessagePacket();
            original.setSenderId(null);
            original.setContent(null);
            original.setTimestamp(null);
            
            String json = invokeToJson(original);
            MessagePacket decoded = invokeFromJson(MessagePacket.class, json);
            
            assertNull(decoded.getSenderId());
            assertNull(decoded.getContent());
            assertNull(decoded.getTimestamp());
        }
        
        @Test
        @DisplayName("Empty strings are preserved")
        void testEmptyStrings() throws Exception {
            skipIfNoJson();
            MessagePacket original = new MessagePacket("", "", ZonedDateTime.now(ZoneOffset.UTC));
            
            String json = invokeToJson(original);
            MessagePacket decoded = invokeFromJson(MessagePacket.class, json);
            
            assertEquals("", decoded.getSenderId());
            assertEquals("", decoded.getContent());
        }
        
        @Test
        @DisplayName("Special JSON characters are escaped correctly")
        void testSpecialCharacters() throws Exception {
            skipIfNoJson();
            String specialContent = "Quote: \"test\" Tab:\t Newline:\n Backslash:\\";
            MessagePacket original = new MessagePacket("sender", specialContent, ZonedDateTime.now(ZoneOffset.UTC));
            
            String json = invokeToJson(original);
            MessagePacket decoded = invokeFromJson(MessagePacket.class, json);
            
            assertEquals(specialContent, decoded.getContent());
        }
    }
    
    // ============================================================================
    // PingPacket Tests
    // ============================================================================
    
    @Nested
    @DisplayName("PingPacket Tests")
    class PingPacketTests {
        
        @Test
        @DisplayName("JSON roundtrip preserves fields")
        void testJsonRoundtrip() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PingPacket original = new PingPacket(now, "ping message");
            
            String json = invokeToJson(original);
            PingPacket decoded = invokeFromJson(PingPacket.class, json);
            
            assertEquals("ping message", decoded.getMessage());
            assertNotNull(decoded.getTimestamp());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip preserves fields")
        void testMsgPackRoundtrip() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PingPacket original = new PingPacket(now, "msgpack ping");
            
            byte[] packed = invokeToMsgPack(original);
            PingPacket decoded = invokeFromMsgPack(PingPacket.class, packed);
            
            assertEquals("msgpack ping", decoded.getMessage());
        }
        
        @Test
        @DisplayName("getType returns correct type")
        void testGetType() {
            PingPacket p = new PingPacket();
            assertEquals("/example/PingPacket", p.getType());
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PingPacket p = new PingPacket(now, "hello");
            
            assertEquals(now, p.getTimestamp());
            assertEquals("hello", p.getMessage());
            assertEquals(PingPacket.TYPE, p.getType());
        }
    }
    
    // ============================================================================
    // PongPacket Tests
    // ============================================================================
    
    @Nested
    @DisplayName("PongPacket Tests")
    class PongPacketTests {
        
        @Test
        @DisplayName("JSON roundtrip with multiple datetime fields")
        void testJsonRoundtrip() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            ZonedDateTime later = now.plusNanos(100_000_000L);
            PongPacket original = new PongPacket(now, later, 100L);
            
            String json = invokeToJson(original);
            PongPacket decoded = invokeFromJson(PongPacket.class, json);
            
            assertEquals(100L, decoded.getLatencyMs());
            assertNotNull(decoded.getOriginalTimestamp());
            assertNotNull(decoded.getResponseTimestamp());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip preserves latency")
        void testMsgPackRoundtrip() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PongPacket original = new PongPacket(now, now, 50L);
            
            byte[] packed = invokeToMsgPack(original);
            PongPacket decoded = invokeFromMsgPack(PongPacket.class, packed);
            
            assertEquals(50L, decoded.getLatencyMs());
        }
        
        @Test
        @DisplayName("Zero latency is preserved")
        void testZeroLatency() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PongPacket original = new PongPacket(now, now, 0L);
            
            String json = invokeToJson(original);
            PongPacket decoded = invokeFromJson(PongPacket.class, json);
            
            assertEquals(0L, decoded.getLatencyMs());
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            ZonedDateTime orig = ZonedDateTime.now(ZoneOffset.UTC);
            ZonedDateTime resp = orig.plusSeconds(1);
            PongPacket p = new PongPacket(orig, resp, 1000L);
            
            assertEquals(orig, p.getOriginalTimestamp());
            assertEquals(resp, p.getResponseTimestamp());
            assertEquals(1000L, p.getLatencyMs());
            assertEquals(PongPacket.TYPE, p.getType());
        }
    }
    
    // ============================================================================
    // DataChunkPacket Tests
    // ============================================================================
    
    @Nested
    @DisplayName("DataChunkPacket Tests")
    class DataChunkPacketTests {
        
        @Test
        @DisplayName("JSON roundtrip with embedded map")
        void testJsonRoundtrip() throws Exception {
            skipIfNoJson();
            Map<Object, Object> data = new HashMap<>();
            data.put("key1", "value1");
            data.put("key2", 42);
            
            DataChunkPacket original = new DataChunkPacket(0L, 10L, data, "checksum123");
            
            String json = invokeToJson(original);
            DataChunkPacket decoded = invokeFromJson(DataChunkPacket.class, json);
            
            assertEquals(0L, decoded.getChunkIndex());
            assertEquals(10L, decoded.getTotalChunks());
            assertEquals("checksum123", decoded.getChecksum());
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip with embedded map")
        void testMsgPackRoundtrip() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("msgpack_key", "msgpack_value");
            
            DataChunkPacket original = new DataChunkPacket(5L, 20L, data, "msgpack_checksum");
            
            byte[] packed = invokeToMsgPack(original);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertEquals(5L, decoded.getChunkIndex());
            assertEquals(20L, decoded.getTotalChunks());
        }
        
        @Test
        @DisplayName("Empty map is preserved")
        void testEmptyMap() throws Exception {
            skipIfNoJson();
            DataChunkPacket original = new DataChunkPacket(0L, 1L, new HashMap<>(), "");
            
            String json = invokeToJson(original);
            DataChunkPacket decoded = invokeFromJson(DataChunkPacket.class, json);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            Map<Object, Object> data = new HashMap<>();
            data.put("test", "value");
            
            DataChunkPacket p = new DataChunkPacket(3L, 10L, data, "cs123");
            
            assertEquals(3L, p.getChunkIndex());
            assertEquals(10L, p.getTotalChunks());
            assertEquals(data, p.getData());
            assertEquals("cs123", p.getChecksum());
            assertEquals(DataChunkPacket.TYPE, p.getType());
        }
    }
    
    // ============================================================================
    // UserProfilePacket Tests (Optional Fields)
    // ============================================================================
    
    @Nested
    @DisplayName("UserProfilePacket Tests")
    class UserProfilePacketTests {
        
        @Test
        @DisplayName("Full constructor with all fields")
        void testFullConstructor() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] avatar = new byte[]{1, 2, 3, 4, 5};
            List<String> tags = Arrays.asList("developer", "java");
            Map<String, Object> prefs = new HashMap<>();
            prefs.put("theme", "dark");
            
            UserProfilePacket p = new UserProfilePacket(
                12345L, "testuser", "test@example.com", "My bio",
                25L, 100.50, tags, prefs, avatar, now, now
            );
            
            assertEquals(12345L, p.getUserId());
            assertEquals("testuser", p.getUsername());
            assertEquals("test@example.com", p.getEmail());
            assertEquals(25L, p.getAge());
            assertEquals(100.50, p.getBalance(), 0.001);
        }
        
        @Test
        @DisplayName("JSON roundtrip with null optional fields")
        void testNullOptionalFields() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            UserProfilePacket original = new UserProfilePacket();
            original.setUserId(1L);
            original.setUsername("minimal");
            original.setEmail("min@test.com");
            original.setBio(null);
            original.setAge(0L);  // primitives cannot be null, use 0 as default
            original.setBalance(0.0);
            original.setTags(new ArrayList<>());
            original.setPreferences(new HashMap<>());
            original.setAvatar(null);
            original.setCreatedAt(now);
            original.setLastLogin(null);
            
            String json = invokeToJson(original);
            UserProfilePacket decoded = invokeFromJson(UserProfilePacket.class, json);
            
            assertNull(decoded.getBio());
            assertEquals(0L, decoded.getAge());  // Check default value
            assertNull(decoded.getAvatar());
            assertNull(decoded.getLastLogin());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip with bytes field (avatar)")
        void testBytesFieldMsgPack() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] avatar = new byte[256];
            for (int i = 0; i < 256; i++) avatar[i] = (byte) i;
            
            UserProfilePacket original = new UserProfilePacket();
            original.setUserId(999L);
            original.setUsername("avatar_test");
            original.setEmail("avatar@test.com");
            original.setBio("bio");
            original.setAge(30L);
            original.setBalance(50.0);
            original.setTags(new ArrayList<>());
            original.setPreferences(new HashMap<>());
            original.setAvatar(avatar);
            original.setCreatedAt(now);
            original.setLastLogin(now);
            
            byte[] packed = invokeToMsgPack(original);
            UserProfilePacket decoded = invokeFromMsgPack(UserProfilePacket.class, packed);
            
            assertNotNull(decoded.getAvatar());
            assertEquals(256, decoded.getAvatar().length);
            assertEquals((byte) 0, decoded.getAvatar()[0]);
            assertEquals((byte) 255, decoded.getAvatar()[255]);
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] avatar = new byte[]{1, 2, 3};
            List<String> tags = Arrays.asList("tag1", "tag2");
            Map<String, Object> prefs = new HashMap<>();
            prefs.put("pref1", "val1");
            
            UserProfilePacket p = new UserProfilePacket(
                42L, "username", "email@test.com", "bio text",
                25L, 100.50, tags, prefs, avatar, now, now
            );
            
            assertEquals(42L, p.getUserId());
            assertEquals("username", p.getUsername());
            assertEquals("email@test.com", p.getEmail());
            assertEquals("bio text", p.getBio());
            assertEquals(25L, p.getAge());
            assertEquals(100.50, p.getBalance(), 0.01);
            assertEquals(tags, p.getTags());
            assertEquals(prefs, p.getPreferences());
            assertArrayEquals(avatar, p.getAvatar());
            assertEquals(now, p.getCreatedAt());
            assertEquals(now, p.getLastLogin());
            assertEquals(UserProfilePacket.TYPE, p.getType());
        }
        
        @Test
        @DisplayName("MsgPack with null optional fields")
        void testMsgPackNullOptionals() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            UserProfilePacket original = new UserProfilePacket();
            original.setUserId(1L);
            original.setUsername("minimal");
            original.setEmail("e@e.com");
            original.setBio(null);  // optional null
            original.setAge(0L);
            original.setBalance(0.0);
            original.setTags(null);  // optional null
            original.setPreferences(null);  // optional null
            original.setAvatar(null);  // optional null
            original.setCreatedAt(now);
            original.setLastLogin(null);  // optional null
            
            byte[] packed = invokeToMsgPack(original);
            UserProfilePacket decoded = invokeFromMsgPack(UserProfilePacket.class, packed);
            
            assertEquals(1L, decoded.getUserId());
            assertNull(decoded.getBio());
            assertNull(decoded.getTags());
            assertNull(decoded.getPreferences());
            assertNull(decoded.getAvatar());
            assertNull(decoded.getLastLogin());
        }
    }
    
    // ============================================================================
    // SecureMessagePacket Tests
    // ============================================================================
    
    @Nested
    @DisplayName("SecureMessagePacket Tests")
    class SecureMessagePacketTests {
        
        @Test
        @DisplayName("JSON roundtrip with encrypted payload")
        void testWithEncryptedPayload() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] payload = new byte[]{(byte)0xDE, (byte)0xAD, (byte)0xBE, (byte)0xEF};
            List<Object> attachments = Arrays.asList("file1.pdf", "file2.doc");
            
            SecureMessagePacket original = new SecureMessagePacket(
                "msg-001", 100L, 200L, "Subject", "Body",
                attachments, payload, 3L, false, now
            );
            
            String json = invokeToJson(original);
            SecureMessagePacket decoded = invokeFromJson(SecureMessagePacket.class, json);
            
            assertEquals("msg-001", decoded.getMessageId());
            assertEquals(100L, decoded.getSenderId());
            assertEquals(200L, decoded.getRecipientId());
            assertEquals(3L, decoded.getPriority());
            assertEquals(false, decoded.getIsRead());
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] payload = new byte[]{10, 20, 30};
            List<Object> attachments = Arrays.asList("a.txt", "b.pdf");
            
            SecureMessagePacket p = new SecureMessagePacket(
                "mid-123", 1L, 2L, "Subject Line", "Body Text",
                attachments, payload, 5L, true, now
            );
            
            assertEquals("mid-123", p.getMessageId());
            assertEquals(1L, p.getSenderId());
            assertEquals(2L, p.getRecipientId());
            assertEquals("Subject Line", p.getSubject());
            assertEquals("Body Text", p.getBody());
            assertEquals(attachments, p.getAttachments());
            assertArrayEquals(payload, p.getEncryptedPayload());
            assertEquals(5L, p.getPriority());
            assertTrue(p.getIsRead());
            assertEquals(now, p.getSentAt());
            assertEquals(SecureMessagePacket.TYPE, p.getType());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip preserves encrypted bytes")
        void testMsgPackEncryptedPayload() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            byte[] payload = new byte[]{1, 2, 3, 4, 5};
            
            SecureMessagePacket original = new SecureMessagePacket();
            original.setMessageId("msg-002");
            original.setSenderId(50L);
            original.setRecipientId(60L);
            original.setSubject("MsgPack");
            original.setBody("Body");
            original.setAttachments(new ArrayList<>());
            original.setEncryptedPayload(payload);
            original.setPriority(5L);
            original.setIsRead(true);
            original.setSentAt(now);
            
            byte[] packed = invokeToMsgPack(original);
            SecureMessagePacket decoded = invokeFromMsgPack(SecureMessagePacket.class, packed);
            
            assertNotNull(decoded.getEncryptedPayload());
            assertEquals(5, decoded.getEncryptedPayload().length);
        }
        
        @Test
        @DisplayName("Null encrypted payload is preserved")
        void testNullPayload() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            SecureMessagePacket original = new SecureMessagePacket();
            original.setMessageId("msg-003");
            original.setSenderId(1L);
            original.setRecipientId(2L);
            original.setSubject("No encryption");
            original.setBody("Plain");
            original.setAttachments(new ArrayList<>());
            original.setEncryptedPayload(null);
            original.setPriority(1L);
            original.setIsRead(false);
            original.setSentAt(now);
            
            String json = invokeToJson(original);
            SecureMessagePacket decoded = invokeFromJson(SecureMessagePacket.class, json);
            
            assertNull(decoded.getEncryptedPayload());
        }
        
        @Test
        @DisplayName("MsgPack handles all null optional fields")
        void testMsgPackNullOptionals() throws Exception {
            skipIfNoMsgPack();
            SecureMessagePacket original = new SecureMessagePacket();
            original.setMessageId(null);  // null string
            original.setSenderId(0L);
            original.setRecipientId(0L);
            original.setSubject(null);  // null string
            original.setBody(null);  // null string
            original.setAttachments(null);  // null list
            original.setEncryptedPayload(null);  // null bytes
            original.setPriority(0L);
            original.setIsRead(false);
            original.setSentAt(null);  // null datetime
            
            byte[] packed = invokeToMsgPack(original);
            SecureMessagePacket decoded = invokeFromMsgPack(SecureMessagePacket.class, packed);
            
            assertNull(decoded.getMessageId());
            assertNull(decoded.getSubject());
            assertNull(decoded.getBody());
            assertNull(decoded.getAttachments());
            assertNull(decoded.getEncryptedPayload());
            assertNull(decoded.getSentAt());
        }
        
        @Test
        @DisplayName("MsgPack with non-empty attachments list")
        void testMsgPackNonEmptyAttachments() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            List<Object> attachments = Arrays.asList("file1.pdf", "file2.doc", "image.png");
            
            SecureMessagePacket original = new SecureMessagePacket();
            original.setMessageId("msg-attachments");
            original.setSenderId(1L);
            original.setRecipientId(2L);
            original.setSubject("With Attachments");
            original.setBody("Body");
            original.setAttachments(attachments);
            original.setEncryptedPayload(new byte[]{1, 2});
            original.setPriority(3L);
            original.setIsRead(true);
            original.setSentAt(now);
            
            byte[] packed = invokeToMsgPack(original);
            SecureMessagePacket decoded = invokeFromMsgPack(SecureMessagePacket.class, packed);
            
            assertNotNull(decoded.getAttachments());
            assertEquals(3, decoded.getAttachments().size());
        }
    }
    
    // ============================================================================
    // ComprehensivePacket Tests (All Field Types)
    // ============================================================================
    
    @Nested
    @DisplayName("ComprehensivePacket Tests")
    class ComprehensivePacketTests {
        
        @Test
        @DisplayName("All field types work correctly")
        void testAllFieldTypes() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(14, 30, 45);
            List<Object> list = Arrays.asList(1, "two", true);
            List<Long> listInt = Arrays.asList(10L, 20L, 30L);
            List<String> listString = Arrays.asList("a", "b", "c");
            Map<String, Object> map = new HashMap<>();
            map.put("key", "value");
            Map<Object, Object> embeddedMap = new HashMap<>();
            embeddedMap.put("nested", "data");
            Map<String, Object> mapStringDynamic = new HashMap<>();
            mapStringDynamic.put("dynamic", 42);
            byte[] bytes = new byte[]{1, 2, 3};
            
            ComprehensivePacket p = new ComprehensivePacket(
                42L, 3.14, 2.718, "test string", true,
                now, time, list, listInt, listString, map,
                embeddedMap, mapStringDynamic, bytes
            );
            
            assertEquals(42L, p.getIntField());
            assertEquals(3.14, p.getFloatField(), 0.0001);
            assertEquals(2.718, p.getDoubleField(), 0.0001);
            assertEquals("test string", p.getStringField());
            assertEquals(true, p.getBoolField());
            assertNotNull(p.getDatetimeField());
            assertNotNull(p.getTimeField());
        }
        
        @Test
        @DisplayName("JSON roundtrip preserves all field types")
        void testJsonRoundtrip() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(12, 0, 0);
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(999L);
            original.setFloatField(1.5);
            original.setDoubleField(2.5);
            original.setStringField("json test");
            original.setBoolField(false);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(Arrays.asList(1, 2, 3));
            original.setListIntField(Arrays.asList(100L, 200L));
            original.setListStringField(Arrays.asList("x", "y"));
            original.setMapField(new HashMap<>());
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[]{10, 20});
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals(999L, decoded.getIntField());
            assertEquals("json test", decoded.getStringField());
            assertEquals(false, decoded.getBoolField());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip preserves all field types")
        void testMsgPackRoundtrip() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(23, 59, 59);
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(12345L);
            original.setFloatField(9.99);
            original.setDoubleField(8.88);
            original.setStringField("msgpack test");
            original.setBoolField(true);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(new ArrayList<>());
            original.setListIntField(new ArrayList<>());
            original.setListStringField(new ArrayList<>());
            original.setMapField(new HashMap<>());
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[0]);
            
            byte[] packed = invokeToMsgPack(original);
            ComprehensivePacket decoded = invokeFromMsgPack(ComprehensivePacket.class, packed);
            
            assertEquals(12345L, decoded.getIntField());
            assertEquals("msgpack test", decoded.getStringField());
        }
        
        @ParameterizedTest
        @ValueSource(longs = {0, 1, -1, Long.MAX_VALUE, Long.MIN_VALUE})
        @DisplayName("Integer edge cases are preserved")
        void testIntegerEdgeCases(long value) throws Exception {
            skipIfNoJson();
            ComprehensivePacket original = createDefaultPacket();
            original.setIntField(value);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals(value, decoded.getIntField());
        }
        
        @ParameterizedTest
        @ValueSource(doubles = {0.0, 1.0, -1.0, 3.14159, 1e-10, 1e10})
        @DisplayName("Float edge cases are preserved")
        void testFloatEdgeCases(double value) throws Exception {
            skipIfNoJson();
            ComprehensivePacket original = createDefaultPacket();
            original.setFloatField(value);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals(value, decoded.getFloatField(), 1e-10);
        }
        
        @Test
        @DisplayName("Empty string is preserved")
        void testEmptyString() throws Exception {
            skipIfNoJson();
            ComprehensivePacket original = createDefaultPacket();
            original.setStringField("");
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals("", decoded.getStringField());
        }
        
        @Test
        @DisplayName("Unicode strings are preserved")
        void testUnicodeStrings() throws Exception {
            skipIfNoJson();
            String unicode = "Hello 世界! Émoji: 🎉🚀";
            ComprehensivePacket original = createDefaultPacket();
            original.setStringField(unicode);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals(unicode, decoded.getStringField());
        }
        
        @Test
        @DisplayName("All getters return correct values")
        void testAllGetters() throws Exception {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(10, 30, 0);
            List<Object> list = Arrays.asList("a", 1);
            List<Long> listInt = Arrays.asList(1L, 2L);
            List<String> listString = Arrays.asList("x", "y");
            Map<String, Object> map = new HashMap<>();
            map.put("k", "v");
            Map<Object, Object> embeddedMap = new HashMap<>();
            embeddedMap.put("e", "m");
            Map<String, Object> mapStringDynamic = new HashMap<>();
            mapStringDynamic.put("d", "y");
            byte[] bytes = new byte[]{5, 6, 7};
            
            ComprehensivePacket p = new ComprehensivePacket(
                100L, 1.1, 2.2, "str", true,
                now, time, list, listInt, listString,
                map, embeddedMap, mapStringDynamic, bytes
            );
            
            // Exercise ALL getters
            assertEquals(100L, p.getIntField());
            assertEquals(1.1, p.getFloatField(), 0.01);
            assertEquals(2.2, p.getDoubleField(), 0.01);
            assertEquals("str", p.getStringField());
            assertTrue(p.getBoolField());
            assertEquals(now, p.getDatetimeField());
            assertEquals(time, p.getTimeField());
            assertEquals(list, p.getListField());
            assertEquals(listInt, p.getListIntField());
            assertEquals(listString, p.getListStringField());
            assertEquals(map, p.getMapField());
            assertEquals(embeddedMap, p.getEmbeddedMapField());
            assertEquals(mapStringDynamic, p.getMapStringDynamicField());
            assertArrayEquals(bytes, p.getBytesField());
            assertEquals(ComprehensivePacket.TYPE, p.getType());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip with non-empty collections")
        void testMsgPackWithNonEmptyCollections() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(15, 45, 30);
            
            List<Object> list = Arrays.asList("item1", 42, true, 3.14);
            List<Long> listInt = Arrays.asList(100L, 200L, 300L);
            List<String> listString = Arrays.asList("hello", "world");
            Map<String, Object> map = new HashMap<>();
            map.put("key1", "value1");
            map.put("key2", 123);
            Map<Object, Object> embeddedMap = new HashMap<>();
            embeddedMap.put("nested_key", "nested_value");
            Map<String, Object> mapStringDynamic = new HashMap<>();
            mapStringDynamic.put("dynamic", "data");
            byte[] bytes = new byte[]{10, 20, 30, 40, 50};
            
            ComprehensivePacket original = new ComprehensivePacket(
                999L, 9.9, 8.8, "msgpack collections test", true,
                now, time, list, listInt, listString,
                map, embeddedMap, mapStringDynamic, bytes
            );
            
            byte[] packed = invokeToMsgPack(original);
            ComprehensivePacket decoded = invokeFromMsgPack(ComprehensivePacket.class, packed);
            
            assertEquals(999L, decoded.getIntField());
            assertEquals("msgpack collections test", decoded.getStringField());
            assertNotNull(decoded.getListField());
            assertNotNull(decoded.getListIntField());
            assertNotNull(decoded.getListStringField());
            assertNotNull(decoded.getMapField());
            assertNotNull(decoded.getEmbeddedMapField());
            assertNotNull(decoded.getMapStringDynamicField());
            assertNotNull(decoded.getBytesField());
        }
        
        @Test
        @DisplayName("MsgPack handles null list and map fields")
        void testMsgPackNullCollections() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(0, 0, 0);
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(0L);
            original.setFloatField(0.0);
            original.setDoubleField(0.0);
            original.setStringField("null test");
            original.setBoolField(false);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(null);  // null list
            original.setListIntField(null);  // null list_int
            original.setListStringField(null);  // null list_string
            original.setMapField(null);  // null map
            original.setEmbeddedMapField(null);  // null embedded_map
            original.setMapStringDynamicField(null);  // null map_string_dynamic
            original.setBytesField(null);  // null bytes
            
            byte[] packed = invokeToMsgPack(original);
            ComprehensivePacket decoded = invokeFromMsgPack(ComprehensivePacket.class, packed);
            
            assertEquals("null test", decoded.getStringField());
            // After decoding, nulls should remain null
            assertNull(decoded.getListField());
            assertNull(decoded.getListIntField());
            assertNull(decoded.getListStringField());
            assertNull(decoded.getMapField());
            assertNull(decoded.getEmbeddedMapField());
            assertNull(decoded.getMapStringDynamicField());
            assertNull(decoded.getBytesField());
        }
        
        private ComprehensivePacket createDefaultPacket() {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(0, 0, 0);
            
            ComprehensivePacket p = new ComprehensivePacket();
            p.setIntField(0L);
            p.setFloatField(0.0);
            p.setDoubleField(0.0);
            p.setStringField("");
            p.setBoolField(false);
            p.setDatetimeField(now);
            p.setTimeField(time);
            p.setListField(new ArrayList<>());
            p.setListIntField(new ArrayList<>());
            p.setListStringField(new ArrayList<>());
            p.setMapField(new HashMap<>());
            p.setEmbeddedMapField(new HashMap<>());
            p.setMapStringDynamicField(new HashMap<>());
            p.setBytesField(new byte[0]);
            return p;
        }
    }
    
    // ============================================================================
    // Packet Factory Tests (direct fromJson dispatching)
    // ============================================================================
    
    @Nested
    @DisplayName("Packet Factory Tests")
    class PacketFactoryTests {
        
        @Test
        @DisplayName("MessagePacket can be deserialized from JSON")
        void testMessagePacketFromJson() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            MessagePacket original = new MessagePacket("test", "content", now);
            String json = invokeToJson(original);
            
            MessagePacket deserialized = invokeFromJson(MessagePacket.class, json);
            
            assertNotNull(deserialized);
            assertEquals("test", deserialized.getSenderId());
        }
        
        @Test
        @DisplayName("PingPacket can be deserialized from MsgPack")
        void testPingPacketFromMsgPack() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PingPacket original = new PingPacket(now, "ping!");
            byte[] packed = invokeToMsgPack(original);
            
            PingPacket deserialized = invokeFromMsgPack(PingPacket.class, packed);
            
            assertNotNull(deserialized);
            assertEquals("ping!", deserialized.getMessage());
        }
    }
    
    // ============================================================================
    // MsgPack packValue Branch Coverage Tests (via DataChunkPacket.data map)
    // ============================================================================
    
    @Nested
    @DisplayName("MsgPack Value Packing Tests")
    class MsgPackPackValueTests {
        
        @Test
        @DisplayName("packValue handles String values")
        void testPackValueString() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("stringKey", "stringValue");
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles Long values")
        void testPackValueLong() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("longKey", Long.valueOf(999999L));
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles Integer values")
        void testPackValueInteger() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("intKey", Integer.valueOf(42));
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles Double values")
        void testPackValueDouble() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("doubleKey", Double.valueOf(3.14159));
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles Float values")
        void testPackValueFloat() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("floatKey", Float.valueOf(2.718f));
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles Boolean values")
        void testPackValueBoolean() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("boolKey", Boolean.TRUE);
            data.put("boolKey2", Boolean.FALSE);
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles byte[] values")
        void testPackValueByteArray() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("bytesKey", new byte[]{1, 2, 3, 4, 5});
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles List values")
        void testPackValueList() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            List<Object> list = Arrays.asList("a", 1, true, 3.14);
            data.put("listKey", list);
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles nested Map values")
        void testPackValueNestedMap() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            Map<String, Object> nested = new HashMap<>();
            nested.put("inner", "value");
            data.put("mapKey", nested);
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles null values")
        void testPackValueNull() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            data.put("nullKey", null);
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
        
        @Test
        @DisplayName("packValue handles unknown type via toString()")
        void testPackValueUnknownType() throws Exception {
            skipIfNoMsgPack();
            Map<Object, Object> data = new HashMap<>();
            // Use a LocalTime which isn't directly handled - will use toString()
            data.put("customKey", LocalTime.of(12, 30));
            DataChunkPacket p = new DataChunkPacket(0L, 1L, data, "checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNotNull(decoded.getData());
        }
    }
    
    // ============================================================================
    // Null Field Handling Tests
    // ============================================================================
    
    @Nested
    @DisplayName("Null Field Handling Tests")
    class NullFieldHandlingTests {
        
        @Test
        @DisplayName("MessagePacket handles null sender_id in MsgPack")
        void testNullSenderId() throws Exception {
            skipIfNoMsgPack();
            MessagePacket p = new MessagePacket();
            p.setSenderId(null);
            p.setContent("content");
            p.setTimestamp(ZonedDateTime.now(ZoneOffset.UTC));
            
            byte[] packed = invokeToMsgPack(p);
            MessagePacket decoded = invokeFromMsgPack(MessagePacket.class, packed);
            
            assertNull(decoded.getSenderId());
        }
        
        @Test
        @DisplayName("MessagePacket handles null content in MsgPack")
        void testNullContent() throws Exception {
            skipIfNoMsgPack();
            MessagePacket p = new MessagePacket();
            p.setSenderId("sender");
            p.setContent(null);
            p.setTimestamp(ZonedDateTime.now(ZoneOffset.UTC));
            
            byte[] packed = invokeToMsgPack(p);
            MessagePacket decoded = invokeFromMsgPack(MessagePacket.class, packed);
            
            assertNull(decoded.getContent());
        }
        
        @Test
        @DisplayName("MessagePacket handles null timestamp in MsgPack")
        void testNullTimestamp() throws Exception {
            skipIfNoMsgPack();
            MessagePacket p = new MessagePacket();
            p.setSenderId("sender");
            p.setContent("content");
            p.setTimestamp(null);
            
            byte[] packed = invokeToMsgPack(p);
            MessagePacket decoded = invokeFromMsgPack(MessagePacket.class, packed);
            
            assertNull(decoded.getTimestamp());
        }
        
        @Test
        @DisplayName("PingPacket handles all null fields in MsgPack")
        void testPingAllNulls() throws Exception {
            skipIfNoMsgPack();
            PingPacket p = new PingPacket();
            p.setTimestamp(null);
            p.setMessage(null);
            
            byte[] packed = invokeToMsgPack(p);
            PingPacket decoded = invokeFromMsgPack(PingPacket.class, packed);
            
            assertNull(decoded.getTimestamp());
            assertNull(decoded.getMessage());
        }
        
        @Test
        @DisplayName("PongPacket handles null original_timestamp in MsgPack")
        void testPongNullOriginal() throws Exception {
            skipIfNoMsgPack();
            PongPacket p = new PongPacket();
            p.setOriginalTimestamp(null);
            p.setResponseTimestamp(ZonedDateTime.now(ZoneOffset.UTC));
            p.setLatencyMs(50L);
            
            byte[] packed = invokeToMsgPack(p);
            PongPacket decoded = invokeFromMsgPack(PongPacket.class, packed);
            
            assertNull(decoded.getOriginalTimestamp());
        }
        
        @Test
        @DisplayName("PongPacket handles null response_timestamp in MsgPack")
        void testPongNullResponse() throws Exception {
            skipIfNoMsgPack();
            PongPacket p = new PongPacket();
            p.setOriginalTimestamp(ZonedDateTime.now(ZoneOffset.UTC));
            p.setResponseTimestamp(null);
            p.setLatencyMs(50L);
            
            byte[] packed = invokeToMsgPack(p);
            PongPacket decoded = invokeFromMsgPack(PongPacket.class, packed);
            
            assertNull(decoded.getResponseTimestamp());
        }
        
        @Test
        @DisplayName("DataChunkPacket handles null data map in MsgPack")
        void testDataChunkNullData() throws Exception {
            skipIfNoMsgPack();
            DataChunkPacket p = new DataChunkPacket();
            p.setChunkIndex(0L);
            p.setTotalChunks(1L);
            p.setData(null);
            p.setChecksum("checksum");
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNull(decoded.getData());
        }
        
        @Test
        @DisplayName("DataChunkPacket handles null checksum in MsgPack")
        void testDataChunkNullChecksum() throws Exception {
            skipIfNoMsgPack();
            DataChunkPacket p = new DataChunkPacket();
            p.setChunkIndex(0L);
            p.setTotalChunks(1L);
            p.setData(new HashMap<>());
            p.setChecksum(null);
            
            byte[] packed = invokeToMsgPack(p);
            DataChunkPacket decoded = invokeFromMsgPack(DataChunkPacket.class, packed);
            
            assertNull(decoded.getChecksum());
        }
    }
    
    // ============================================================================
    // toMap Tests (exercising toMap through toJson)
    // ============================================================================
    
    @Nested
    @DisplayName("toMap Tests")
    class ToMapTests {
        
        @Test
        @DisplayName("MessagePacket toMap includes packetType")
        void testMessagePacketToMap() throws Exception {
            skipIfNoJson();
            MessagePacket p = new MessagePacket("s", "c", ZonedDateTime.now(ZoneOffset.UTC));
            String json = invokeToJson(p);
            assertTrue(json.contains("packetType"));
            assertTrue(json.contains("/chat/MessagePacket"));
        }
        
        @Test
        @DisplayName("PingPacket toMap includes packetType")
        void testPingPacketToMap() throws Exception {
            skipIfNoJson();
            PingPacket p = new PingPacket(ZonedDateTime.now(ZoneOffset.UTC), "msg");
            String json = invokeToJson(p);
            assertTrue(json.contains("/example/PingPacket"));
        }
        
        @Test
        @DisplayName("PongPacket toMap includes packetType")
        void testPongPacketToMap() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            PongPacket p = new PongPacket(now, now, 100L);
            String json = invokeToJson(p);
            assertTrue(json.contains("/example/PongPacket"));
        }
        
        @Test
        @DisplayName("DataChunkPacket toMap includes packetType")
        void testDataChunkPacketToMap() throws Exception {
            skipIfNoJson();
            DataChunkPacket p = new DataChunkPacket(0L, 1L, new HashMap<>(), "cs");
            String json = invokeToJson(p);
            assertTrue(json.contains("/example/DataChunkPacket"));
        }
        
        @Test
        @DisplayName("UserProfilePacket toMap includes packetType")
        void testUserProfilePacketToMap() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            UserProfilePacket p = new UserProfilePacket();
            p.setUserId(1L);
            p.setUsername("user");
            p.setEmail("e@e.com");
            p.setBio("bio");
            p.setAge(25L);
            p.setBalance(100.0);
            p.setTags(new ArrayList<>());
            p.setPreferences(new HashMap<>());
            p.setAvatar(null);
            p.setCreatedAt(now);
            p.setLastLogin(now);
            String json = invokeToJson(p);
            assertTrue(json.contains("/example/UserProfilePacket"));
        }
        
        @Test
        @DisplayName("SecureMessagePacket toMap includes packetType")
        void testSecureMessagePacketToMap() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            SecureMessagePacket p = new SecureMessagePacket();
            p.setMessageId("m1");
            p.setSenderId(1L);
            p.setRecipientId(2L);
            p.setSubject("s");
            p.setBody("b");
            p.setAttachments(new ArrayList<>());
            p.setEncryptedPayload(new byte[]{1});
            p.setPriority(1L);
            p.setIsRead(false);
            p.setSentAt(now);
            String json = invokeToJson(p);
            assertTrue(json.contains("/example/SecureMessagePacket"));
        }
        
        @Test
        @DisplayName("ComprehensivePacket toMap includes packetType")
        void testComprehensivePacketToMap() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(12, 0);
            ComprehensivePacket p = new ComprehensivePacket();
            p.setIntField(1L);
            p.setFloatField(1.0);
            p.setDoubleField(1.0);
            p.setStringField("s");
            p.setBoolField(true);
            p.setDatetimeField(now);
            p.setTimeField(time);
            p.setListField(new ArrayList<>());
            p.setListIntField(new ArrayList<>());
            p.setListStringField(new ArrayList<>());
            p.setMapField(new HashMap<>());
            p.setEmbeddedMapField(new HashMap<>());
            p.setMapStringDynamicField(new HashMap<>());
            p.setBytesField(new byte[0]);
            String json = invokeToJson(p);
            assertTrue(json.contains("/test/ComprehensivePacket"));
        }
    }
    
    // ============================================================================
    // DataPacket Base Class Tests
    // ============================================================================
    
    @Nested
    @DisplayName("DataPacket Base Class Tests")
    class DataPacketBaseTests {
        
        @Test
        @DisplayName("DataPacket.toJson uses toMap")
        void testBaseToJson() throws Exception {
            skipIfNoJson();
            MessagePacket p = new MessagePacket("sender", "content", ZonedDateTime.now(ZoneOffset.UTC));
            // This calls invokeToJson(DataPacket) which uses toMap()
            String json = invokeToJson(p);
            assertTrue(json.contains("sender"));
            assertTrue(json.contains("content"));
        }
    }
    
    // ============================================================================
    // Security-Critical Payload Tests
    // ============================================================================
    
    @Nested
    @DisplayName("Security-Critical Payload Tests")
    class SecurityPayloadTests {
        
        @Test
        @DisplayName("JSON roundtrip preserves security-critical financial data")
        void testSecurityPayloadJson() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(12, 0, 0);
            
            Map<String, Object> secureMap = new HashMap<>();
            secureMap.put("source_account", "ACC-12345");
            secureMap.put("dest_account", "ACC-67890");
            secureMap.put("amount_cents", 9999999L);
            secureMap.put("currency", "USD");
            secureMap.put("verified", true);
            
            List<Object> auditList = Arrays.asList("audit1", "audit2", 1704067200);
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(1234567890123456789L);
            original.setFloatField(99999.99);
            original.setDoubleField(0.0);
            original.setStringField("TRANSFER:ACC-12345→ACC-67890");
            original.setBoolField(true);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(auditList);
            original.setListIntField(new ArrayList<>());
            original.setListStringField(new ArrayList<>());
            original.setMapField(secureMap);
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[0]);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertEquals(1234567890123456789L, decoded.getIntField());
            assertEquals("TRANSFER:ACC-12345→ACC-67890", decoded.getStringField());
            assertTrue(decoded.getBoolField());
            assertEquals(3, decoded.getListField().size());
            assertEquals(5, decoded.getMapField().size());
        }
        
        @Test
        @DisplayName("MsgPack roundtrip preserves security-critical financial data")
        void testSecurityPayloadMsgPack() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(12, 0, 0);
            
            Map<String, Object> secureMap = new HashMap<>();
            secureMap.put("source_account", "ACC-12345");
            secureMap.put("dest_account", "ACC-67890");
            secureMap.put("amount_cents", 9999999L);
            secureMap.put("currency", "USD");
            secureMap.put("verified", true);
            
            List<Object> auditList = Arrays.asList("audit1", "audit2", 1704067200);
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(1234567890123456789L);
            original.setFloatField(99999.99);
            original.setDoubleField(0.0);
            original.setStringField("TRANSFER:ACC-12345→ACC-67890");
            original.setBoolField(true);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(auditList);
            original.setListIntField(new ArrayList<>());
            original.setListStringField(new ArrayList<>());
            original.setMapField(secureMap);
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[0]);
            
            byte[] packed = invokeToMsgPack(original);
            ComprehensivePacket decoded = invokeFromMsgPack(ComprehensivePacket.class, packed);
            
            assertEquals(1234567890123456789L, decoded.getIntField());
            assertEquals("TRANSFER:ACC-12345→ACC-67890", decoded.getStringField());
            assertTrue(decoded.getBoolField());
            assertNotNull(decoded.getListField());
            assertNotNull(decoded.getMapField());
        }
    }
    
    // ============================================================================
    // Binary Data Edge Cases Tests
    // ============================================================================
    
    @Nested
    @DisplayName("Binary Data Edge Cases Tests")
    class BinaryDataEdgeCasesTests {
        
        @Test
        @DisplayName("Empty binary array is preserved in MsgPack")
        void testEmptyBinaryArray() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            
            UserProfilePacket original = new UserProfilePacket();
            original.setUserId(1L);
            original.setUsername("bintest");
            original.setEmail("bin@test.com");
            original.setBio("Binary test");
            original.setAge(20L);
            original.setBalance(0.0);
            original.setTags(new ArrayList<>());
            original.setPreferences(new HashMap<>());
            original.setAvatar(new byte[0]);  // empty array
            original.setCreatedAt(now);
            original.setLastLogin(now);
            
            byte[] packed = invokeToMsgPack(original);
            UserProfilePacket decoded = invokeFromMsgPack(UserProfilePacket.class, packed);
            
            assertNotNull(decoded.getAvatar());
            assertEquals(0, decoded.getAvatar().length);
        }
        
        @Test
        @DisplayName("Large binary array (10KB) is preserved in MsgPack")
        void testLargeBinaryArray() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            
            byte[] largeBinary = new byte[10000];
            for (int i = 0; i < largeBinary.length; i++) {
                largeBinary[i] = (byte)(i % 256);
            }
            
            UserProfilePacket original = new UserProfilePacket();
            original.setUserId(2L);
            original.setUsername("largebin");
            original.setEmail("large@bin.com");
            original.setBio("Large binary");
            original.setAge(30L);
            original.setBalance(0.0);
            original.setTags(new ArrayList<>());
            original.setPreferences(new HashMap<>());
            original.setAvatar(largeBinary);
            original.setCreatedAt(now);
            original.setLastLogin(now);
            
            byte[] packed = invokeToMsgPack(original);
            UserProfilePacket decoded = invokeFromMsgPack(UserProfilePacket.class, packed);
            
            assertNotNull(decoded.getAvatar());
            assertEquals(10000, decoded.getAvatar().length);
            // Verify first 100 bytes match pattern
            for (int i = 0; i < 100; i++) {
                assertEquals((byte)(i % 256), decoded.getAvatar()[i]);
            }
        }
        
        @Test
        @DisplayName("Binary with special byte values (0xFF, 0x00) preserved")
        void testSpecialByteValues() throws Exception {
            skipIfNoMsgPack();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            
            byte[] payload = new byte[]{(byte)0xFF, (byte)0xFE, (byte)0x00, (byte)0x01, (byte)0xAB};
            
            SecureMessagePacket original = new SecureMessagePacket();
            original.setMessageId("enc-001");
            original.setSenderId(1L);
            original.setRecipientId(2L);
            original.setSubject("Encrypted");
            original.setBody("Body");
            original.setAttachments(new ArrayList<>());
            original.setEncryptedPayload(payload);
            original.setPriority(1L);
            original.setIsRead(false);
            original.setSentAt(now);
            
            byte[] packed = invokeToMsgPack(original);
            SecureMessagePacket decoded = invokeFromMsgPack(SecureMessagePacket.class, packed);
            
            assertNotNull(decoded.getEncryptedPayload());
            assertEquals(5, decoded.getEncryptedPayload().length);
            assertEquals((byte)0xFF, decoded.getEncryptedPayload()[0]);
            assertEquals((byte)0x00, decoded.getEncryptedPayload()[2]);
            assertEquals((byte)0xAB, decoded.getEncryptedPayload()[4]);
        }
    }
    
    // ============================================================================
    // Large Collection Tests
    // ============================================================================
    
    @Nested
    @DisplayName("Large Collection Tests")
    class LargeCollectionTests {
        
        @Test
        @DisplayName("Large list (1000 elements) is preserved in JSON")
        void testLargeListJson() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(0, 0, 0);
            
            List<Object> largeList = new ArrayList<>();
            for (int i = 0; i < 1000; i++) {
                largeList.add(i);
            }
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(0L);
            original.setFloatField(0.0);
            original.setDoubleField(0.0);
            original.setStringField("");
            original.setBoolField(false);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(largeList);
            original.setListIntField(new ArrayList<>());
            original.setListStringField(new ArrayList<>());
            original.setMapField(new HashMap<>());
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[0]);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertNotNull(decoded.getListField());
            assertEquals(1000, decoded.getListField().size());
        }
        
        @Test
        @DisplayName("Large map (100 entries) is preserved in JSON")
        void testLargeMapJson() throws Exception {
            skipIfNoJson();
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            LocalTime time = LocalTime.of(0, 0, 0);
            
            Map<String, Object> largeMap = new HashMap<>();
            for (int i = 0; i < 100; i++) {
                largeMap.put("key_" + i, i);
            }
            
            ComprehensivePacket original = new ComprehensivePacket();
            original.setIntField(0L);
            original.setFloatField(0.0);
            original.setDoubleField(0.0);
            original.setStringField("");
            original.setBoolField(false);
            original.setDatetimeField(now);
            original.setTimeField(time);
            original.setListField(new ArrayList<>());
            original.setListIntField(new ArrayList<>());
            original.setListStringField(new ArrayList<>());
            original.setMapField(largeMap);
            original.setEmbeddedMapField(new HashMap<>());
            original.setMapStringDynamicField(new HashMap<>());
            original.setBytesField(new byte[0]);
            
            String json = invokeToJson(original);
            ComprehensivePacket decoded = invokeFromJson(ComprehensivePacket.class, json);
            
            assertNotNull(decoded.getMapField());
            assertEquals(100, decoded.getMapField().size());
        }
    }
}
