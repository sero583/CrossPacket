package packets

import (
	"encoding/json"
	"time"
	"github.com/vmihailenco/msgpack/v5"
)

type ComprehensivePacket struct {
	Type string `json:"packetType" msgpack:"packetType"`
	IntField int64 `json:"int_field" msgpack:"int_field"`
	FloatField float64 `json:"float_field" msgpack:"float_field"`
	DoubleField float64 `json:"double_field" msgpack:"double_field"`
	StringField string `json:"string_field" msgpack:"string_field"`
	BoolField bool `json:"bool_field" msgpack:"bool_field"`
	DatetimeField time.Time `json:"datetime_field" msgpack:"datetime_field"`
	TimeField string `json:"time_field" msgpack:"time_field"`
	ListField []interface{} `json:"list_field" msgpack:"list_field"`
	ListIntField []int64 `json:"list_int_field" msgpack:"list_int_field"`
	ListStringField []string `json:"list_string_field" msgpack:"list_string_field"`
	MapField map[string]interface{} `json:"map_field" msgpack:"map_field"`
	EmbeddedMapField map[string]interface{} `json:"embedded_map_field" msgpack:"embedded_map_field"`
	MapStringDynamicField map[string]interface{} `json:"map_string_dynamic_field" msgpack:"map_string_dynamic_field"`
	BytesField []byte `json:"bytes_field" msgpack:"bytes_field"`
}

func (p *ComprehensivePacket) GetType() string {
	return "/test/ComprehensivePacket"
}

func (p *ComprehensivePacket) ToJSON() ([]byte, error) {
	p.Type = "/test/ComprehensivePacket"
	return json.Marshal(p)
}

func ComprehensivePacketFromJSON(data []byte) (*ComprehensivePacket, error) {
	var p ComprehensivePacket
	err := json.Unmarshal(data, &p)
	return &p, err
}

func (p *ComprehensivePacket) ToMsgPack() ([]byte, error) {
	p.Type = "/test/ComprehensivePacket"
	return msgpack.Marshal(p)
}

func ComprehensivePacketFromMsgPack(data []byte) (*ComprehensivePacket, error) {
	var p ComprehensivePacket
	err := msgpack.Unmarshal(data, &p)
	return &p, err
}