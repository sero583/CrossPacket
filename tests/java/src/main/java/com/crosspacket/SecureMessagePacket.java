package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Security-hardened message packet with strict validation
 */
public class SecureMessagePacket extends DataPacket {

    public static final String TYPE = "/example/SecureMessagePacket";

    private String messageId;
    private long senderId;
    private long recipientId;
    private String subject;
    private String body;
    private List<Object> attachments;
    private byte[] encryptedPayload;
    private long priority;
    private boolean isRead;
    private ZonedDateTime sentAt;

    public SecureMessagePacket() {}

    public SecureMessagePacket(String messageId, long senderId, long recipientId, String subject, String body, List<Object> attachments, byte[] encryptedPayload, long priority, boolean isRead, ZonedDateTime sentAt) {
        this.messageId = messageId;
        this.senderId = senderId;
        this.recipientId = recipientId;
        this.subject = subject;
        this.body = body;
        this.attachments = attachments;
        this.encryptedPayload = encryptedPayload;
        this.priority = priority;
        this.isRead = isRead;
        this.sentAt = sentAt;
    }

    public String getMessageId() {
        return messageId;
    }

    public void setMessageId(String messageId) {
        this.messageId = messageId;
    }

    public long getSenderId() {
        return senderId;
    }

    public void setSenderId(long senderId) {
        this.senderId = senderId;
    }

    public long getRecipientId() {
        return recipientId;
    }

    public void setRecipientId(long recipientId) {
        this.recipientId = recipientId;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public String getBody() {
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public List<Object> getAttachments() {
        return attachments;
    }

    public void setAttachments(List<Object> attachments) {
        this.attachments = attachments;
    }

    public byte[] getEncryptedPayload() {
        return encryptedPayload;
    }

    public void setEncryptedPayload(byte[] encryptedPayload) {
        this.encryptedPayload = encryptedPayload;
    }

    public long getPriority() {
        return priority;
    }

    public void setPriority(long priority) {
        this.priority = priority;
    }

    public boolean getIsRead() {
        return isRead;
    }

    public void setIsRead(boolean isRead) {
        this.isRead = isRead;
    }

    public ZonedDateTime getSentAt() {
        return sentAt;
    }

    public void setSentAt(ZonedDateTime sentAt) {
        this.sentAt = sentAt;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("message_id", messageId);
        map.put("sender_id", senderId);
        map.put("recipient_id", recipientId);
        map.put("subject", subject);
        map.put("body", body);
        map.put("attachments", attachments);
        map.put("encrypted_payload", encryptedPayload);
        map.put("priority", priority);
        map.put("is_read", isRead);
        map.put("sent_at", sentAt != null ? sentAt.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(11);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("message_id");
        if (messageId != null) packer.packString(messageId); else packer.packNil();
        packer.packString("sender_id");
        packer.packLong(senderId);
        packer.packString("recipient_id");
        packer.packLong(recipientId);
        packer.packString("subject");
        if (subject != null) packer.packString(subject); else packer.packNil();
        packer.packString("body");
        if (body != null) packer.packString(body); else packer.packNil();
        packer.packString("attachments");
        if (attachments != null) { packList(packer, attachments); } else packer.packNil();
        packer.packString("encrypted_payload");
        if (encryptedPayload != null) { packer.packBinaryHeader(encryptedPayload.length); packer.writePayload(encryptedPayload); } else packer.packNil();
        packer.packString("priority");
        packer.packLong(priority);
        packer.packString("is_read");
        packer.packBoolean(isRead);
        packer.packString("sent_at");
        if (sentAt != null) packer.packString(sentAt.toString()); else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static SecureMessagePacket fromMsgPack(byte[] data) throws Exception {
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

    private static SecureMessagePacket fromMap(Map<String, Object> map) {
        SecureMessagePacket packet = new SecureMessagePacket();
        packet.setMessageId((String) map.get("message_id"));
        packet.setSenderId(((Number) map.get("sender_id")).longValue());
        packet.setRecipientId(((Number) map.get("recipient_id")).longValue());
        packet.setSubject((String) map.get("subject"));
        packet.setBody((String) map.get("body"));
        packet.setAttachments((List<Object>) map.get("attachments"));
        Object encryptedPayloadVal = map.get("encrypted_payload");
        if (encryptedPayloadVal instanceof byte[]) {
            packet.setEncryptedPayload((byte[]) encryptedPayloadVal);
        } else if (encryptedPayloadVal instanceof String) {
            packet.setEncryptedPayload(java.util.Base64.getDecoder().decode((String) encryptedPayloadVal));
        }
        packet.setPriority(((Number) map.get("priority")).longValue());
        packet.setIsRead((Boolean) map.get("is_read"));
        Object sentAtVal = map.get("sent_at");
        if (sentAtVal != null) packet.setSentAt(ZonedDateTime.parse(sentAtVal.toString()));
        return packet;
    }

    public static SecureMessagePacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}