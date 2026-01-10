package com.crosspacket;

import java.time.ZonedDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.msgpack.core.*;

/**
 * Chunked data packet for progressive loading of large datasets
 */
public class DataChunkPacket extends DataPacket {

    public static final String TYPE = "/example/DataChunkPacket";

    private long chunkIndex;
    private long totalChunks;
    private Map<Object, Object> data;
    private String checksum;

    public DataChunkPacket() {}

    public DataChunkPacket(long chunkIndex, long totalChunks, Map<Object, Object> data, String checksum) {
        this.chunkIndex = chunkIndex;
        this.totalChunks = totalChunks;
        this.data = data;
        this.checksum = checksum;
    }

    public long getChunkIndex() {
        return chunkIndex;
    }

    public void setChunkIndex(long chunkIndex) {
        this.chunkIndex = chunkIndex;
    }

    public long getTotalChunks() {
        return totalChunks;
    }

    public void setTotalChunks(long totalChunks) {
        this.totalChunks = totalChunks;
    }

    public Map<Object, Object> getData() {
        return data;
    }

    public void setData(Map<Object, Object> data) {
        this.data = data;
    }

    public String getChecksum() {
        return checksum;
    }

    public void setChecksum(String checksum) {
        this.checksum = checksum;
    }

    @Override
    public String getType() {
        return TYPE;
    }

    @Override
    protected Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("packetType", TYPE);
        map.put("chunk_index", chunkIndex);
        map.put("total_chunks", totalChunks);
        map.put("data", data);
        map.put("checksum", checksum);
        return map;
    }

    public byte[] toMsgPack() throws Exception {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        packer.packMapHeader(5);
        packer.packString("packetType");
        packer.packString(TYPE);
        packer.packString("chunk_index");
        packer.packLong(chunkIndex);
        packer.packString("total_chunks");
        packer.packLong(totalChunks);
        packer.packString("data");
        if (data != null) { packMap(packer, data); } else packer.packNil();
        packer.packString("checksum");
        if (checksum != null) packer.packString(checksum); else packer.packNil();
        packer.close();
        return packer.toByteArray();
    }

    public static DataChunkPacket fromMsgPack(byte[] data) throws Exception {
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

    private static DataChunkPacket fromMap(Map<String, Object> map) {
        DataChunkPacket packet = new DataChunkPacket();
        packet.setChunkIndex(((Number) map.get("chunk_index")).longValue());
        packet.setTotalChunks(((Number) map.get("total_chunks")).longValue());
        packet.setData((Map<Object, Object>) map.get("data"));
        packet.setChecksum((String) map.get("checksum"));
        return packet;
    }

    public static DataChunkPacket fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        @SuppressWarnings("unchecked")
        Map<String, Object> map = mapper.readValue(json, Map.class);
        return fromMap(map);
    }
}