// CrossPacket - C# Unit Tests using xUnit
//
// Author: Serhat Gueler (sero583)
// GitHub: https://github.com/sero583
// License: MIT

using System;
using Xunit;
using CrossPacket;

namespace CrossPacket.Tests;

/// <summary>
/// Reflection-based method detection for conditional tests.
/// Supports JSON_ONLY, MSGPACK_ONLY, and BOTH generation modes.
/// </summary>
public static class TestModeHelper
{
    private static readonly bool _hasJson;
    private static readonly bool _hasMsgPack;
    
    static TestModeHelper()
    {
        // Use reflection to detect available methods at runtime
        _hasJson = typeof(PingPacket).GetMethod("ToJson") != null;
        _hasMsgPack = typeof(PingPacket).GetMethod("ToMsgPack") != null;
        Console.WriteLine($"JSON methods available: {_hasJson}");
        Console.WriteLine($"MsgPack methods available: {_hasMsgPack}");
    }
    
    public static bool HasJson => _hasJson;
    public static bool HasMsgPack => _hasMsgPack;
    
    // Legacy compatibility
    public static bool IsMsgPackOnly => !_hasJson && _hasMsgPack;
    public static bool IsJsonOnly => _hasJson && !_hasMsgPack;
    public static bool IsBoth => _hasJson && _hasMsgPack;
    
    // Reflection invocation helpers
    public static string InvokeToJson<T>(T obj)
    {
        var method = typeof(T).GetMethod("ToJson");
        return (string)method!.Invoke(obj, null)!;
    }
    
    public static T InvokeFromJson<T>(string json)
    {
        var method = typeof(T).GetMethod("FromJson", new[] { typeof(string) });
        return (T)method!.Invoke(null, new object[] { json })!;
    }
    
    public static byte[] InvokeToMsgPack<T>(T obj)
    {
        var method = typeof(T).GetMethod("ToMsgPack");
        return (byte[])method!.Invoke(obj, null)!;
    }
    
    public static T InvokeFromMsgPack<T>(byte[] bytes)
    {
        var method = typeof(T).GetMethod("FromMsgPack", new[] { typeof(byte[]) });
        return (T)method!.Invoke(null, new object[] { bytes })!;
    }
}

/// <summary>
/// Tests for PingPacket
/// </summary>
public class PingPacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new PingPacket(DateTimeOffset.UtcNow, "test");
        Assert.Equal(PingPacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/example/PingPacket", PingPacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return; // Skip in MSGPACK_ONLY mode

        var original = new PingPacket(DateTimeOffset.UtcNow, "hello world");
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<PingPacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.Message, decoded!.Message);
        Assert.Equal(original.Type, decoded.Type);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return; // Skip in JSON_ONLY mode

        var original = new PingPacket(DateTimeOffset.UtcNow, "msgpack test");
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<PingPacket>(bytes);

        Assert.Equal(original.Message, decoded.Message);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new PingPacket();
        Assert.Equal(PingPacket.TYPE, p.Type);
        Assert.Equal("", p.Message);
    }
}

/// <summary>
/// Tests for PongPacket
/// </summary>
public class PongPacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new PongPacket(DateTimeOffset.UtcNow, DateTimeOffset.UtcNow, 42);
        Assert.Equal(PongPacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/example/PongPacket", PongPacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var original = new PongPacket(DateTimeOffset.UtcNow, DateTimeOffset.UtcNow, 100);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<PongPacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.LatencyMs, decoded!.LatencyMs);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new PongPacket(DateTimeOffset.UtcNow, DateTimeOffset.UtcNow, 200);
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<PongPacket>(bytes);

        Assert.Equal(original.LatencyMs, decoded.LatencyMs);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new PongPacket();
        Assert.Equal(PongPacket.TYPE, p.Type);
    }
}

/// <summary>
/// Tests for MessagePacket
/// </summary>
public class MessagePacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new MessagePacket("sender1", "Hello!", DateTimeOffset.UtcNow);
        Assert.Equal(MessagePacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/chat/MessagePacket", MessagePacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var original = new MessagePacket("sender", "Test content", DateTimeOffset.UtcNow);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<MessagePacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.Content, decoded!.Content);
        Assert.Equal(original.SenderId, decoded.SenderId);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new MessagePacket("s", "MsgPack content", DateTimeOffset.UtcNow);
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<MessagePacket>(bytes);

        Assert.Equal(original.Content, decoded.Content);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new MessagePacket();
        Assert.Equal(MessagePacket.TYPE, p.Type);
    }
}

/// <summary>
/// Tests for DataChunkPacket
/// </summary>
public class DataChunkPacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new DataChunkPacket(0, 10, new Dictionary<string, object>(), "checksum");
        Assert.Equal(DataChunkPacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/example/DataChunkPacket", DataChunkPacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var data = new Dictionary<string, object> { { "key", "value" } };
        var original = new DataChunkPacket(5, 20, data, "abc123");
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<DataChunkPacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.ChunkIndex, decoded!.ChunkIndex);
        Assert.Equal(original.TotalChunks, decoded.TotalChunks);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new DataChunkPacket(1, 5, new Dictionary<string, object>(), "cs");
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<DataChunkPacket>(bytes);

        Assert.Equal(original.ChunkIndex, decoded.ChunkIndex);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new DataChunkPacket();
        Assert.Equal(DataChunkPacket.TYPE, p.Type);
    }
}

/// <summary>
/// Tests for ComprehensivePacket
/// </summary>
public class ComprehensivePacketTests
{
    private ComprehensivePacket CreateTestPacket(
        long intField = 0,
        double floatField = 0.0,
        double doubleField = 0.0,
        string stringField = "",
        bool boolField = false)
    {
        return new ComprehensivePacket(
            intField, floatField, doubleField, stringField, boolField,
            DateTimeOffset.UtcNow, TimeSpan.Zero,
            new List<object>(), new List<long>(), new List<string>(),
            new Dictionary<string, object>(), new Dictionary<string, object>(),
            new Dictionary<string, object>(), Array.Empty<byte>()
        );
    }

    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = CreateTestPacket();
        Assert.Equal(ComprehensivePacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/test/ComprehensivePacket", ComprehensivePacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var original = CreateTestPacket(intField: 42, stringField: "test");
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.IntField, decoded!.IntField);
        Assert.Equal(original.StringField, decoded.StringField);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = CreateTestPacket(intField: 999);
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<ComprehensivePacket>(bytes);

        Assert.Equal(original.IntField, decoded.IntField);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new ComprehensivePacket();
        Assert.Equal(ComprehensivePacket.TYPE, p.Type);
    }

    // Integer edge cases
    [Theory]
    [InlineData(0)]
    [InlineData(1)]
    [InlineData(-1)]
    [InlineData(int.MaxValue)]
    [InlineData(int.MinValue)]
    [InlineData(long.MaxValue)]
    [InlineData(long.MinValue)]
    public void IntegerEdgeCases_JsonRoundtrip(long value)
    {
        if (!TestModeHelper.HasJson) return;
        var original = CreateTestPacket(intField: value);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(value, decoded!.IntField);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(1)]
    [InlineData(-1)]
    [InlineData(int.MaxValue)]
    [InlineData(int.MinValue)]
    public void IntegerEdgeCases_MsgPackRoundtrip(long value)
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = CreateTestPacket(intField: value);
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<ComprehensivePacket>(bytes);
        Assert.Equal(value, decoded.IntField);
    }

    // Float edge cases
    [Theory]
    [InlineData(0.0)]
    [InlineData(1.0)]
    [InlineData(-1.0)]
    [InlineData(3.14159265)]
    [InlineData(2.71828182)]
    public void FloatEdgeCases_JsonRoundtrip(double value)
    {
        if (!TestModeHelper.HasJson) return;
        var original = CreateTestPacket(doubleField: value);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(value, decoded!.DoubleField, 5);
    }

    // String edge cases
    [Theory]
    [InlineData("")]
    [InlineData("a")]
    [InlineData("   ")]
    [InlineData("Hello 世界 🌍")]
    [InlineData("Quote: \"test\" Backslash: \\")]
    [InlineData("line1\nline2\r\nline3")]
    public void StringEdgeCases_JsonRoundtrip(string value)
    {
        if (!TestModeHelper.HasJson) return;
        var original = CreateTestPacket(stringField: value);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(value, decoded!.StringField);
    }

    // Boolean edge cases
    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void BooleanEdgeCases_JsonRoundtrip(bool value)
    {
        if (!TestModeHelper.HasJson) return;
        var original = CreateTestPacket(boolField: value);
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(value, decoded!.BoolField);
    }

    [Fact]
    public void ListField_JsonRoundtrip()
    {
        if (!TestModeHelper.HasJson) return;
        var p = new ComprehensivePacket(
            0, 0, 0, "", false, DateTimeOffset.UtcNow, TimeSpan.Zero,
            new List<object> { 1, "two", 3.0 },
            new List<long> { 1, 2, 3, 4, 5 },
            new List<string> { "a", "b", "c" },
            new Dictionary<string, object>(),
            new Dictionary<string, object>(),
            new Dictionary<string, object>(),
            Array.Empty<byte>()
        );
        var json = TestModeHelper.InvokeToJson(p);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(3, decoded!.ListField.Count);
        Assert.Equal(5, decoded.ListIntField.Count);
        Assert.Equal(3, decoded.ListStringField.Count);
    }

    [Fact]
    public void MapField_JsonRoundtrip()
    {
        if (!TestModeHelper.HasJson) return;
        var map = new Dictionary<string, object>
        {
            { "key1", "value1" },
            { "key2", 42 },
            { "key3", true }
        };
        var p = new ComprehensivePacket(
            0, 0, 0, "", false, DateTimeOffset.UtcNow, TimeSpan.Zero,
            new List<object>(), new List<long>(), new List<string>(),
            map, new Dictionary<string, object>(), new Dictionary<string, object>(),
            Array.Empty<byte>()
        );
        var json = TestModeHelper.InvokeToJson(p);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);
        Assert.Equal(3, decoded!.MapField.Count);
    }

    [Fact]
    public void BytesField_MsgPackRoundtrip()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var bytes = new byte[] { 0xDE, 0xAD, 0xBE, 0xEF };
        var p = new ComprehensivePacket(
            0, 0, 0, "", false, DateTimeOffset.UtcNow, TimeSpan.Zero,
            new List<object>(), new List<long>(), new List<string>(),
            new Dictionary<string, object>(), new Dictionary<string, object>(),
            new Dictionary<string, object>(), bytes
        );
        var msgpack = TestModeHelper.InvokeToMsgPack(p);
        var decoded = TestModeHelper.InvokeFromMsgPack<ComprehensivePacket>(msgpack);
        Assert.Equal(bytes, decoded.BytesField);
    }
}

/// <summary>
/// Tests for UserProfilePacket
/// </summary>
public class UserProfilePacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new UserProfilePacket(
            1, "john", "john@example.com", "Bio", 30, 100.0,
            new List<string> { "admin" }, new Dictionary<string, object>(),
            null, DateTimeOffset.UtcNow, null
        );
        Assert.Equal(UserProfilePacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/example/UserProfilePacket", UserProfilePacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var original = new UserProfilePacket(
            123, "alice", "alice@test.com", null, 25, 50.0,
            new List<string> { "user" }, new Dictionary<string, object>(),
            null, DateTimeOffset.UtcNow, null
        );
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<UserProfilePacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.Username, decoded!.Username);
        Assert.Equal(original.Age, decoded.Age);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new UserProfilePacket(
            456, "bob", "bob@test.com", "Hi", 35, 999.99,
            new List<string>(), new Dictionary<string, object>(),
            null, DateTimeOffset.UtcNow, DateTimeOffset.UtcNow
        );
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<UserProfilePacket>(bytes);

        Assert.Equal(original.Username, decoded.Username);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new UserProfilePacket();
        Assert.Equal(UserProfilePacket.TYPE, p.Type);
    }
}

/// <summary>
/// Tests for SecureMessagePacket
/// </summary>
public class SecureMessagePacketTests
{
    [Fact]
    public void Constructor_SetsTypeCorrectly()
    {
        var p = new SecureMessagePacket(
            "msg-001", 1, 2, "Subject", "Body",
            new List<object>(), null, 1, false, DateTimeOffset.UtcNow
        );
        Assert.Equal(SecureMessagePacket.TYPE, p.Type);
    }

    [Fact]
    public void TypeConstant_IsCorrect()
    {
        Assert.Equal("/example/SecureMessagePacket", SecureMessagePacket.TYPE);
    }

    [Fact]
    public void JsonRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasJson) return;
        var original = new SecureMessagePacket(
            "sec-123", 10, 20, "Hello", "World",
            new List<object>(), null, 5, true, DateTimeOffset.UtcNow
        );
        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<SecureMessagePacket>(json);

        Assert.NotNull(decoded);
        Assert.Equal(original.MessageId, decoded!.MessageId);
        Assert.Equal(original.Subject, decoded.Subject);
    }

    [Fact]
    public void MsgPackRoundtrip_PreservesData()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new SecureMessagePacket(
            "mp-sec", 100, 200, "Test", "Content",
            new List<object>(), new byte[] { 0xDE, 0xAD }, 3, false, DateTimeOffset.UtcNow
        );
        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<SecureMessagePacket>(bytes);

        Assert.Equal(original.MessageId, decoded.MessageId);
    }

    [Fact]
    public void DefaultConstructor_SetsDefaults()
    {
        var p = new SecureMessagePacket();
        Assert.Equal(SecureMessagePacket.TYPE, p.Type);
    }
}

/// <summary>
/// Security-critical payload test
/// </summary>
public class SecurityCriticalTests
{
    [Fact]
    public void SecurityPayload_JsonRoundtrip_PreservesIntegrity()
    {
        if (!TestModeHelper.HasJson) return;
        var secureMap = new Dictionary<string, object>
        {
            { "source_account", "ACC-12345" },
            { "dest_account", "ACC-67890" },
            { "amount_cents", 9999999 }
        };

        var original = new ComprehensivePacket(
            1234567890123456789L, 99999.99, 88888.88, "TRANSFER:ACC-12345→ACC-67890", true,
            DateTimeOffset.UtcNow, TimeSpan.FromHours(12),
            new List<object> { "audit1", "audit2" },
            new List<long> { 1, 2, 3 },
            new List<string> { "log1" },
            secureMap, new Dictionary<string, object>(), new Dictionary<string, object>(),
            new byte[] { 0xDE, 0xAD, 0xBE, 0xEF }
        );

        var json = TestModeHelper.InvokeToJson(original);
        var decoded = TestModeHelper.InvokeFromJson<ComprehensivePacket>(json);

        Assert.Equal(original.IntField, decoded!.IntField);
        Assert.Equal(original.StringField, decoded.StringField);
        Assert.True(decoded.BoolField);
    }

    [Fact]
    public void SecurityPayload_MsgPackRoundtrip_PreservesIntegrity()
    {
        if (!TestModeHelper.HasMsgPack) return;
        var original = new ComprehensivePacket(
            1234567890123456789L, 99999.99, 88888.88, "TRANSFER:ACC-12345→ACC-67890", true,
            DateTimeOffset.UtcNow, TimeSpan.FromHours(12),
            new List<object>(), new List<long>(), new List<string>(),
            new Dictionary<string, object>(), new Dictionary<string, object>(),
            new Dictionary<string, object>(), new byte[] { 0xDE, 0xAD, 0xBE, 0xEF }
        );

        var bytes = TestModeHelper.InvokeToMsgPack(original);
        var decoded = TestModeHelper.InvokeFromMsgPack<ComprehensivePacket>(bytes);

        Assert.Equal(original.IntField, decoded.IntField);
        Assert.Equal(original.StringField, decoded.StringField);
    }
}
