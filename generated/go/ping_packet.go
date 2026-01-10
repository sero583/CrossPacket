package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type PingPacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	Timestamp time.Time `json:"timestamp" msgpack:"timestamp"`
	Message string `json:"message" msgpack:"message"`
}

func (p *PingPacket) GetType() string {
	return "/example/PingPacket"
}

func (p *PingPacket) ToJSON() ([]byte, error) {
	p.Type = "/example/PingPacket"
	return json.Marshal(p)
}

func PingPacketFromJSON(data []byte) (*PingPacket, error) {
	var p PingPacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *PingPacket) ToMsgPack() ([]byte, error) {
	p.Type = "/example/PingPacket"
	return msgpack.Marshal(p)
}

func PingPacketFromMsgPack(data []byte) (*PingPacket, error) {
	var p PingPacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}