package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Simple ping packet for connection testing
 */
public class PingPacket extends DataPacket {

    public static final String TYPE = "/example/PingPacket";

    private ZonedDateTime timestamp;
    private String message;

    public PingPacket() {}

    public PingPacket(ZonedDateTime timestamp, String message) {
        this.timestamp = timestamp;
        this.message = message;
    }

    public ZonedDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(ZonedDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("timestamp", timestamp != null ? timestamp.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        map.put("message", message);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(3);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("timestamp");
        if (timestamp != null) packer.packString(timestamp.toString()); else packer.packNil();
        packer.packString("message");
        if (message != null) packer.packString(message); else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static PingPacket fromMsgPack(byte[] data) throws Exception {
        MessageUnpacker unpacker = MessagePack.newDefaultUnpacker(data);
        Map<String, Object> map = new HashMap<>();
        int size = unpacker.unpackMapHeader();
        for (int i = 0; i < size; i++) {
            String key = unpacker.unpackString();
            map.put(key, unpackValue(unpacker));
        }
        unpacker.close();
        return fromMap(map);
    }

    private static PingPacket fromMap(Map<String, Object> map) {
        PingPacket packet = new PingPacket();
        Object timestampVal = map.get("timestamp");
        if (timestampVal != null) packet.setTimestamp(ZonedDateTime.parse(timestampVal.toString()));
        packet.setMessage((String) map.get("message"));
        return packet;
    }

    public static PingPacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}