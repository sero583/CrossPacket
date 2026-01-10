package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Response to a ping packet
 */
public class PongPacket extends DataPacket {

    public static final String TYPE = "/example/PongPacket";

    private ZonedDateTime originalTimestamp;
    private ZonedDateTime responseTimestamp;
    private long latencyMs;

    public PongPacket() {}

    public PongPacket(ZonedDateTime originalTimestamp, ZonedDateTime responseTimestamp, long latencyMs) {
        this.originalTimestamp = originalTimestamp;
        this.responseTimestamp = responseTimestamp;
        this.latencyMs = latencyMs;
    }

    public ZonedDateTime getOriginalTimestamp() {
        return originalTimestamp;
    }

    public void setOriginalTimestamp(ZonedDateTime originalTimestamp) {
        this.originalTimestamp = originalTimestamp;
    }

    public ZonedDateTime getResponseTimestamp() {
        return responseTimestamp;
    }

    public void setResponseTimestamp(ZonedDateTime responseTimestamp) {
        this.responseTimestamp = responseTimestamp;
    }

    public long getLatencyMs() {
        return latencyMs;
    }

    public void setLatencyMs(long latencyMs) {
        this.latencyMs = latencyMs;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("original_timestamp", originalTimestamp != null ? originalTimestamp.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        map.put("response_timestamp", responseTimestamp != null ? responseTimestamp.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        map.put("latency_ms", latencyMs);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(4);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("original_timestamp");
        if (originalTimestamp != null) packer.packString(originalTimestamp.toString()); else packer.packNil();
        packer.packString("response_timestamp");
        if (responseTimestamp != null) packer.packString(responseTimestamp.toString()); else packer.packNil();
        packer.packString("latency_ms");
        packer.packLong(latencyMs);
        packer.close();
        return packer.toByteArray();
    }

    public static PongPacket fromMsgPack(byte[] data) throws Exception {
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

    private static PongPacket fromMap(Map<String, Object> map) {
        PongPacket packet = new PongPacket();
        Object originalTimestampVal = map.get("original_timestamp");
        if (originalTimestampVal != null) packet.setOriginalTimestamp(ZonedDateTime.parse(originalTimestampVal.toString()));
        Object responseTimestampVal = map.get("response_timestamp");
        if (responseTimestampVal != null) packet.setResponseTimestamp(ZonedDateTime.parse(responseTimestampVal.toString()));
        packet.setLatencyMs(((Number) map.get("latency_ms")).longValue());
        return packet;
    }

    public static PongPacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}