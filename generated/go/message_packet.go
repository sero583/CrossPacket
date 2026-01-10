package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type MessagePacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	SenderId string `json:"sender_id" msgpack:"sender_id"`
	Content string `json:"content" msgpack:"content"`
	Timestamp time.Time `json:"timestamp" msgpack:"timestamp"`
}

func (p *MessagePacket) GetType() string {
	return "/chat/MessagePacket"
}

func (p *MessagePacket) ToJSON() ([]byte, error) {
	p.Type = "/chat/MessagePacket"
	return json.Marshal(p)
}

func MessagePacketFromJSON(data []byte) (*MessagePacket, error) {
	var p MessagePacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *MessagePacket) ToMsgPack() ([]byte, error) {
	p.Type = "/chat/MessagePacket"
	return msgpack.Marshal(p)
}

func MessagePacketFromMsgPack(data []byte) (*MessagePacket, error) {
	var p MessagePacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}