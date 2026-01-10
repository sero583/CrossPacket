package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type UserProfilePacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	UserId int64 `json:"user_id" msgpack:"user_id"`
	Username string `json:"username" msgpack:"username"`
	Email string `json:"email" msgpack:"email"`
	Bio *string `json:"bio" msgpack:"bio"`
	Age *int64 `json:"age" msgpack:"age"`
	Balance float64 `json:"balance" msgpack:"balance"`
	Tags []string `json:"tags" msgpack:"tags"`
	Preferences map[string]interface{} `json:"preferences" msgpack:"preferences"`
	Avatar []byte `json:"avatar" msgpack:"avatar"`
	CreatedAt time.Time `json:"created_at" msgpack:"created_at"`
	LastLogin time.Time `json:"last_login" msgpack:"last_login"`
}

func (p *UserProfilePacket) GetType() string {
	return "/example/UserProfilePacket"
}

func (p *UserProfilePacket) ToJSON() ([]byte, error) {
	p.Type = "/example/UserProfilePacket"
	return json.Marshal(p)
}

func UserProfilePacketFromJSON(data []byte) (*UserProfilePacket, error) {
	var p UserProfilePacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *UserProfilePacket) ToMsgPack() ([]byte, error) {
	p.Type = "/example/UserProfilePacket"
	return msgpack.Marshal(p)
}

func UserProfilePacketFromMsgPack(data []byte) (*UserProfilePacket, error) {
	var p UserProfilePacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}