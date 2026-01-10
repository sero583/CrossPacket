package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type SecureMessagePacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	MessageId string `json:"message_id" msgpack:"message_id"`
	SenderId int64 `json:"sender_id" msgpack:"sender_id"`
	RecipientId int64 `json:"recipient_id" msgpack:"recipient_id"`
	Subject string `json:"subject" msgpack:"subject"`
	Body string `json:"body" msgpack:"body"`
	Attachments []interface{} `json:"attachments" msgpack:"attachments"`
	EncryptedPayload []byte `json:"encrypted_payload" msgpack:"encrypted_payload"`
	Priority int64 `json:"priority" msgpack:"priority"`
	IsRead bool `json:"is_read" msgpack:"is_read"`
	SentAt time.Time `json:"sent_at" msgpack:"sent_at"`
}

func (p *SecureMessagePacket) GetType() string {
	return "/example/SecureMessagePacket"
}

func (p *SecureMessagePacket) ToJSON() ([]byte, error) {
	p.Type = "/example/SecureMessagePacket"
	return json.Marshal(p)
}

func SecureMessagePacketFromJSON(data []byte) (*SecureMessagePacket, error) {
	var p SecureMessagePacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *SecureMessagePacket) ToMsgPack() ([]byte, error) {
	p.Type = "/example/SecureMessagePacket"
	return msgpack.Marshal(p)
}

func SecureMessagePacketFromMsgPack(data []byte) (*SecureMessagePacket, error) {
	var p SecureMessagePacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}