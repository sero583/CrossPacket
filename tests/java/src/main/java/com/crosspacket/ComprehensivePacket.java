package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Test packet containing ALL supported types for comprehensive testing
 */
public class ComprehensivePacket extends DataPacket {

    public static final String TYPE = "/test/ComprehensivePacket";

    private long intField;
    private double floatField;
    private double doubleField;
    private String stringField;
    private boolean boolField;
    private ZonedDateTime datetimeField;
    private LocalTime timeField;
    private List<Object> listField;
    private List<Long> listIntField;
    private List<String> listStringField;
    private Map<String, Object> mapField;
    private Map<Object, Object> embeddedMapField;
    private Map<String, Object> mapStringDynamicField;
    private byte[] bytesField;

    public ComprehensivePacket() {}

    public ComprehensivePacket(long intField, double floatField, double doubleField, String stringField, boolean boolField, ZonedDateTime datetimeField, LocalTime timeField, List<Object> listField, List<Long> listIntField, List<String> listStringField, Map<String, Object> mapField, Map<Object, Object> embeddedMapField, Map<String, Object> mapStringDynamicField, byte[] bytesField) {
        this.intField = intField;
        this.floatField = floatField;
        this.doubleField = doubleField;
        this.stringField = stringField;
        this.boolField = boolField;
        this.datetimeField = datetimeField;
        this.timeField = timeField;
        this.listField = listField;
        this.listIntField = listIntField;
        this.listStringField = listStringField;
        this.mapField = mapField;
        this.embeddedMapField = embeddedMapField;
        this.mapStringDynamicField = mapStringDynamicField;
        this.bytesField = bytesField;
    }

    public long getIntField() {
        return intField;
    }

    public void setIntField(long intField) {
        this.intField = intField;
    }

    public double getFloatField() {
        return floatField;
    }

    public void setFloatField(double floatField) {
        this.floatField = floatField;
    }

    public double getDoubleField() {
        return doubleField;
    }

    public void setDoubleField(double doubleField) {
        this.doubleField = doubleField;
    }

    public String getStringField() {
        return stringField;
    }

    public void setStringField(String stringField) {
        this.stringField = stringField;
    }

    public boolean getBoolField() {
        return boolField;
    }

    public void setBoolField(boolean boolField) {
        this.boolField = boolField;
    }

    public ZonedDateTime getDatetimeField() {
        return datetimeField;
    }

    public void setDatetimeField(ZonedDateTime datetimeField) {
        this.datetimeField = datetimeField;
    }

    public LocalTime getTimeField() {
        return timeField;
    }

    public void setTimeField(LocalTime timeField) {
        this.timeField = timeField;
    }

    public List<Object> getListField() {
        return listField;
    }

    public void setListField(List<Object> listField) {
        this.listField = listField;
    }

    public List<Long> getListIntField() {
        return listIntField;
    }

    public void setListIntField(List<Long> listIntField) {
        this.listIntField = listIntField;
    }

    public List<String> getListStringField() {
        return listStringField;
    }

    public void setListStringField(List<String> listStringField) {
        this.listStringField = listStringField;
    }

    public Map<String, Object> getMapField() {
        return mapField;
    }

    public void setMapField(Map<String, Object> mapField) {
        this.mapField = mapField;
    }

    public Map<Object, Object> getEmbeddedMapField() {
        return embeddedMapField;
    }

    public void setEmbeddedMapField(Map<Object, Object> embeddedMapField) {
        this.embeddedMapField = embeddedMapField;
    }

    public Map<String, Object> getMapStringDynamicField() {
        return mapStringDynamicField;
    }

    public void setMapStringDynamicField(Map<String, Object> mapStringDynamicField) {
        this.mapStringDynamicField = mapStringDynamicField;
    }

    public byte[] getBytesField() {
        return bytesField;
    }

    public void setBytesField(byte[] bytesField) {
        this.bytesField = bytesField;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("int_field", intField);
        map.put("float_field", floatField);
        map.put("double_field", doubleField);
        map.put("string_field", stringField);
        map.put("bool_field", boolField);
        map.put("datetime_field", datetimeField != null ? datetimeField.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) : null);
        map.put("time_field", timeField != null ? timeField.toString() : null);
        map.put("list_field", listField);
        map.put("list_int_field", listIntField);
        map.put("list_string_field", listStringField);
        map.put("map_field", mapField);
        map.put("embedded_map_field", embeddedMapField);
        map.put("map_string_dynamic_field", mapStringDynamicField);
        map.put("bytes_field", bytesField);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(15);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("int_field");
        packer.packLong(intField);
        packer.packString("float_field");
        packer.packDouble(floatField);
        packer.packString("double_field");
        packer.packDouble(doubleField);
        packer.packString("string_field");
        if (stringField != null) packer.packString(stringField); else packer.packNil();
        packer.packString("bool_field");
        packer.packBoolean(boolField);
        packer.packString("datetime_field");
        if (datetimeField != null) packer.packString(datetimeField.toString()); else packer.packNil();
        packer.packString("time_field");
        if (timeField != null) packer.packString(timeField.toString()); else packer.packNil();
        packer.packString("list_field");
        if (listField != null) { packList(packer, listField); } else packer.packNil();
        packer.packString("list_int_field");
        if (listIntField != null) { packList(packer, listIntField); } else packer.packNil();
        packer.packString("list_string_field");
        if (listStringField != null) { packList(packer, listStringField); } else packer.packNil();
        packer.packString("map_field");
        if (mapField != null) { packMap(packer, mapField); } else packer.packNil();
        packer.packString("embedded_map_field");
        if (embeddedMapField != null) { packMap(packer, embeddedMapField); } else packer.packNil();
        packer.packString("map_string_dynamic_field");
        if (mapStringDynamicField != null) { packMap(packer, mapStringDynamicField); } else packer.packNil();
        packer.packString("bytes_field");
        if (bytesField != null) { packer.packBinaryHeader(bytesField.length); packer.writePayload(bytesField); } else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static ComprehensivePacket fromMsgPack(byte[] data) throws Exception {
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

    private static ComprehensivePacket fromMap(Map<String, Object> map) {
        ComprehensivePacket packet = new ComprehensivePacket();
        packet.setIntField(((Number) map.get("int_field")).longValue());
        packet.setFloatField(((Number) map.get("float_field")).doubleValue());
        packet.setDoubleField(((Number) map.get("double_field")).doubleValue());
        packet.setStringField((String) map.get("string_field"));
        packet.setBoolField((Boolean) map.get("bool_field"));
        Object datetimeFieldVal = map.get("datetime_field");
        if (datetimeFieldVal != null) packet.setDatetimeField(ZonedDateTime.parse(datetimeFieldVal.toString()));
        Object timeFieldVal = map.get("time_field");
        if (timeFieldVal != null) packet.setTimeField(LocalTime.parse(timeFieldVal.toString()));
        packet.setListField((List<Object>) map.get("list_field"));
        packet.setListIntField((List<Long>) map.get("list_int_field"));
        packet.setListStringField((List<String>) map.get("list_string_field"));
        packet.setMapField((Map<String, Object>) map.get("map_field"));
        packet.setEmbeddedMapField((Map<Object, Object>) map.get("embedded_map_field"));
        packet.setMapStringDynamicField((Map<String, Object>) map.get("map_string_dynamic_field"));
        Object bytesFieldVal = map.get("bytes_field");
        if (bytesFieldVal instanceof byte[]) {
            packet.setBytesField((byte[]) bytesFieldVal);
        } else if (bytesFieldVal instanceof String) {
            packet.setBytesField(java.util.Base64.getDecoder().decode((String) bytesFieldVal));
        }
        return packet;
    }

    public static ComprehensivePacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}