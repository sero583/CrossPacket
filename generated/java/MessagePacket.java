package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * A chat message packet for real-time communication
 */
public class MessagePacket extends DataPacket {

    public static final String TYPE = "/chat/MessagePacket";

    private String senderId;
    private String content;
    private ZonedDateTime timestamp;

    public MessagePacket() {}

    public MessagePacket(String senderId, String content, ZonedDateTime timestamp) {
        this.senderId = senderId;
        this.content = content;
        this.timestamp = timestamp;
    }

    public String getSenderId() {
        return senderId;
    }

    public void setSenderId(String senderId) {
        this.senderId = senderId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public ZonedDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(ZonedDateTime timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("sender_id", senderId);
        map.put("content", content);
        map.put("timestamp", timestamp != null ? timestamp.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(4);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("sender_id");
        if (senderId != null) packer.packString(senderId); else packer.packNil();
        packer.packString("content");
        if (content != null) packer.packString(content); else packer.packNil();
        packer.packString("timestamp");
        if (timestamp != null) packer.packString(timestamp.toString()); else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static MessagePacket fromMsgPack(byte[] data) throws Exception {
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

    private static MessagePacket fromMap(Map<String, Object> map) {
        MessagePacket packet = new MessagePacket();
        packet.setSenderId((String) map.get("sender_id"));
        packet.setContent((String) map.get("content"));
        Object timestampVal = map.get("timestamp");
        if (timestampVal != null) packet.setTimestamp(ZonedDateTime.parse(timestampVal.toString()));
        return packet;
    }

    public static MessagePacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}