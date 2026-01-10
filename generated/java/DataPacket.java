package com.crosspacket;

import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Base class for all data packets.
 */
public abstract class DataPacket {

    private static final ObjectMapper mapper = new ObjectMapper();

    /**
     * Get the packet type identifier.
     */
    public abstract String getType();

    /**
     * Convert to Map for serialization (internal).
     */
    protected abstract Map<String, Object> toMap();

    /**
     * Serialize to JSON string.
     */
    public String toJson() throws Exception {
        return mapper.writeValueAsString(toMap());
    }

    // =========== Shared MsgPack utilities ===========

    protected static void packList(MessageBufferPacker packer, List<?> list) throws Exception {
        packer.packArrayHeader(list.size());
        for (Object item : list) {
            packValue(packer, item);
        }
    }

    protected static void packMap(MessageBufferPacker packer, Map<?, ?> map) throws Exception {
        packer.packMapHeader(map.size());
        for (Map.Entry<?, ?> entry : map.entrySet()) {
            packValue(packer, entry.getKey());
            packValue(packer, entry.getValue());
        }
    }

    protected static void packValue(MessageBufferPacker packer, Object value) throws Exception {
        if (value == null) { packer.packNil(); }
        else if (value instanceof String) { packer.packString((String) value); }
        else if (value instanceof Long) { packer.packLong((Long) value); }
        else if (value instanceof Integer) { packer.packInt((Integer) value); }
        else if (value instanceof Double) { packer.packDouble((Double) value); }
        else if (value instanceof Float) { packer.packFloat((Float) value); }
        else if (value instanceof Boolean) { packer.packBoolean((Boolean) value); }
        else if (value instanceof byte[]) { byte[] b = (byte[]) value; packer.packBinaryHeader(b.length); packer.writePayload(b); }
        else if (value instanceof List) { packList(packer, (List<?>) value); }
        else if (value instanceof Map) { packMap(packer, (Map<?, ?>) value); }
        else { packer.packString(value.toString()); }
    }

    protected static Object unpackValue(MessageUnpacker unpacker) throws Exception {
        MessageFormat format = unpacker.getNextFormat();
        switch (format.getValueType()) {
            case STRING: return unpacker.unpackString();
            case INTEGER: return unpacker.unpackLong();
            case FLOAT: return unpacker.unpackDouble();
            case BOOLEAN: return unpacker.unpackBoolean();
            case NIL: unpacker.unpackNil(); return null;
            case BINARY: {
                int len = unpacker.unpackBinaryHeader();
                byte[] bytes = new byte[len];
                unpacker.readPayload(bytes);
                return bytes;
            }
            case ARRAY: {
                int len = unpacker.unpackArrayHeader();
                List<Object> list = new ArrayList<>(len);
                for (int j = 0; j < len; j++) { list.add(unpackValue(unpacker)); }
                return list;
            }
            case MAP: {
                int len = unpacker.unpackMapHeader();
                Map<Object, Object> m = new HashMap<>(len);
                for (int j = 0; j < len; j++) { m.put(unpackValue(unpacker), unpackValue(unpacker)); }
                return m;
            }
            default: unpacker.skipValue(); return null;
        }
    }
}