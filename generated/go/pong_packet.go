package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type PongPacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	OriginalTimestamp time.Time `json:"original_timestamp" msgpack:"original_timestamp"`
	ResponseTimestamp time.Time `json:"response_timestamp" msgpack:"response_timestamp"`
	LatencyMs int64 `json:"latency_ms" msgpack:"latency_ms"`
}

func (p *PongPacket) GetType() string {
	return "/example/PongPacket"
}

func (p *PongPacket) ToJSON() ([]byte, error) {
	p.Type = "/example/PongPacket"
	return json.Marshal(p)
}

func PongPacketFromJSON(data []byte) (*PongPacket, error) {
	var p PongPacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *PongPacket) ToMsgPack() ([]byte, error) {
	p.Type = "/example/PongPacket"
	return msgpack.Marshal(p)
}

func PongPacketFromMsgPack(data []byte) (*PongPacket, error) {
	var p PongPacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}