package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Example packet demonstrating field-level validation overrides
 */
public class UserProfilePacket extends DataPacket {

    public static final String TYPE = "/example/UserProfilePacket";

    private long userId;
    private String username;
    private String email;
    private String bio;
    private long age;
    private double balance;
    private List<String> tags;
    private Map<String, Object> preferences;
    private byte[] avatar;
    private ZonedDateTime createdAt;
    private ZonedDateTime lastLogin;

    public UserProfilePacket() {}

    public UserProfilePacket(long userId, String username, String email, String bio, long age, double balance, List<String> tags, Map<String, Object> preferences, byte[] avatar, ZonedDateTime createdAt, ZonedDateTime lastLogin) {
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.bio = bio;
        this.age = age;
        this.balance = balance;
        this.tags = tags;
        this.preferences = preferences;
        this.avatar = avatar;
        this.createdAt = createdAt;
        this.lastLogin = lastLogin;
    }

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getBio() {
        return bio;
    }

    public void setBio(String bio) {
        this.bio = bio;
    }

    public long getAge() {
        return age;
    }

    public void setAge(long age) {
        this.age = age;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }

    public Map<String, Object> getPreferences() {
        return preferences;
    }

    public void setPreferences(Map<String, Object> preferences) {
        this.preferences = preferences;
    }

    public byte[] getAvatar() {
        return avatar;
    }

    public void setAvatar(byte[] avatar) {
        this.avatar = avatar;
    }

    public ZonedDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(ZonedDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public ZonedDateTime getLastLogin() {
        return lastLogin;
    }

    public void setLastLogin(ZonedDateTime lastLogin) {
        this.lastLogin = lastLogin;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("user_id", userId);
        map.put("username", username);
        map.put("email", email);
        map.put("bio", bio);
        map.put("age", age);
        map.put("balance", balance);
        map.put("tags", tags);
        map.put("preferences", preferences);
        map.put("avatar", avatar);
        map.put("created_at", createdAt != null ? createdAt.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        map.put("last_login", lastLogin != null ? lastLogin.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(12);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("user_id");
        packer.packLong(userId);
        packer.packString("username");
        if (username != null) packer.packString(username); else packer.packNil();
        packer.packString("email");
        if (email != null) packer.packString(email); else packer.packNil();
        packer.packString("bio");
        if (bio != null) packer.packString(bio); else packer.packNil();
        packer.packString("age");
        packer.packLong(age);
        packer.packString("balance");
        packer.packDouble(balance);
        packer.packString("tags");
        if (tags != null) { packList(packer, tags); } else packer.packNil();
        packer.packString("preferences");
        if (preferences != null) { packMap(packer, preferences); } else packer.packNil();
        packer.packString("avatar");
        if (avatar != null) { packer.packBinaryHeader(avatar.length); packer.writePayload(avatar); } else packer.packNil();
        packer.packString("created_at");
        if (createdAt != null) packer.packString(createdAt.toString()); else packer.packNil();
        packer.packString("last_login");
        if (lastLogin != null) packer.packString(lastLogin.toString()); else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static UserProfilePacket fromMsgPack(byte[] data) throws Exception {
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

    private static UserProfilePacket fromMap(Map<String, Object> map) {
        UserProfilePacket packet = new UserProfilePacket();
        packet.setUserId(((Number) map.get("user_id")).longValue());
        packet.setUsername((String) map.get("username"));
        packet.setEmail((String) map.get("email"));
        packet.setBio((String) map.get("bio"));
        packet.setAge(((Number) map.get("age")).longValue());
        packet.setBalance(((Number) map.get("balance")).doubleValue());
        packet.setTags((List<String>) map.get("tags"));
        packet.setPreferences((Map<String, Object>) map.get("preferences"));
        Object avatarVal = map.get("avatar");
        if (avatarVal instanceof byte[]) {
            packet.setAvatar((byte[]) avatarVal);
        } else if (avatarVal instanceof String) {
            packet.setAvatar(java.util.Base64.getDecoder().decode((String) avatarVal));
        }
        Object createdAtVal = map.get("created_at");
        if (createdAtVal != null) packet.setCreatedAt(ZonedDateTime.parse(createdAtVal.toString()));
        Object lastLoginVal = map.get("last_login");
        if (lastLoginVal != null) packet.setLastLogin(ZonedDateTime.parse(lastLoginVal.toString()));
        return packet;
    }

    public static UserProfilePacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}