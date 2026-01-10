package packets

import (
	"encoding/json"
	"github.com/vmihailenco/msgpack/v5"
)

type DataChunkPacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	ChunkIndex int64 `json:"chunk_index" msgpack:"chunk_index"`
	TotalChunks int64 `json:"total_chunks" msgpack:"total_chunks"`
	Data map[string]interface{} `json:"data" msgpack:"data"`
	Checksum string `json:"checksum" msgpack:"checksum"`
}

func (p *DataChunkPacket) GetType() string {
	return "/example/DataChunkPacket"
}

func (p *DataChunkPacket) ToJSON() ([]byte, error) {
	p.Type = "/example/DataChunkPacket"
	return json.Marshal(p)
}

func DataChunkPacketFromJSON(data []byte) (*DataChunkPacket, error) {
	var p DataChunkPacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *DataChunkPacket) ToMsgPack() ([]byte, error) {
	p.Type = "/example/DataChunkPacket"
	return msgpack.Marshal(p)
}

func DataChunkPacketFromMsgPack(data []byte) (*DataChunkPacket, error) {
	var p DataChunkPacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}