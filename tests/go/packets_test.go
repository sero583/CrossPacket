// CrossPacket - Comprehensive Go Test Suite
//
// Author: Serhat Gueler (sero583)
// GitHub: https://github.com/sero583
// License: MIT
//
// This test validates GENERATED PACKET runtime behavior with edge cases.
// Uses standard Go testing package for proper `go test` integration.

package main

import (
	"math"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/vmihailenco/msgpack/v5"
)

var testMode = getTestEnv("TEST_MODE", "BOTH")

// ============================================================================
// Copy generated packet structs here for testing
// ============================================================================

type PingPacket struct {
	Type      string    `json:"type" msgpack:"type"`
	Timestamp time.Time `json:"timestamp" msgpack:"timestamp"`
	Message   string    `json:"message" msgpack:"message"`
}

type ComprehensivePacket struct {
	Type             string                 `json:"type" msgpack:"type"`
	IntField         int64                  `json:"int_field" msgpack:"int_field"`
	FloatField       float64                `json:"float_field" msgpack:"float_field"`
	StringField      string                 `json:"string_field" msgpack:"string_field"`
	BoolField        bool                   `json:"bool_field" msgpack:"bool_field"`
	DatetimeField    time.Time              `json:"datetime_field" msgpack:"datetime_field"`
	ListField        []interface{}          `json:"list_field" msgpack:"list_field"`
	MapField         map[string]interface{} `json:"map_field" msgpack:"map_field"`
	EmbeddedMapField map[string]interface{} `json:"embedded_map_field" msgpack:"embedded_map_field"`
	BytesField       interface{}            `json:"bytes_field" msgpack:"bytes_field"`
}

// ============================================================================
// Test Helpers
// ============================================================================

func getTestEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return strings.ToUpper(value)
	}
	return fallback
}

func floatEquals(a, b float64) bool {
	diff := math.Abs(a - b)
	if diff < 1e-10 {
		return true
	}
	maxVal := math.Max(math.Abs(a), math.Abs(b))
	if maxVal > 0 && diff/maxVal < 1e-10 {
		return true
	}
	return a == b
}

func skipIfJsonOnly(t *testing.T) {
	if testMode == "JSON_ONLY" {
		t.Skip("Skipping MsgPack test in JSON_ONLY mode")
	}
}

func skipIfMsgPackOnly(t *testing.T) {
	if testMode == "MSGPACK_ONLY" {
		t.Skip("Skipping JSON test in MSGPACK_ONLY mode")
	}
}

// ============================================================================
// Import/Instantiation Tests
// ============================================================================

func TestInstantiatePingPacket(t *testing.T) {
	p := PingPacket{}
	// Verify we can create it - Type will be empty for zero-value struct
	if p.Type != "" {
		t.Logf("PingPacket type: %s", p.Type)
	}
}

func TestInstantiateComprehensivePacket(t *testing.T) {
	p := ComprehensivePacket{}
	// Verify we can create it - Type will be empty for zero-value struct
	if p.Type != "" {
		t.Logf("ComprehensivePacket type: %s", p.Type)
	}
}

// ============================================================================
// Integer Edge Cases
// ============================================================================

func TestIntZeroMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: 0}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != 0 {
		t.Errorf("Expected 0, got %d", decoded.IntField)
	}
}

func TestIntOneMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: 1}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != 1 {
		t.Errorf("Expected 1, got %d", decoded.IntField)
	}
}

func TestIntNegativeOneMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: -1}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != -1 {
		t.Errorf("Expected -1, got %d", decoded.IntField)
	}
}

func TestIntMax32MsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: 2147483647}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != 2147483647 {
		t.Errorf("Expected 2147483647, got %d", decoded.IntField)
	}
}

func TestIntMin32MsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: -2147483648}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != -2147483648 {
		t.Errorf("Expected -2147483648, got %d", decoded.IntField)
	}
}

func TestIntLargePositiveMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{IntField: 999999999999}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.IntField != 999999999999 {
		t.Errorf("Expected 999999999999, got %d", decoded.IntField)
	}
}

// ============================================================================
// Float Edge Cases
// ============================================================================

func TestFloatZeroMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{FloatField: 0.0}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if !floatEquals(decoded.FloatField, 0.0) {
		t.Errorf("Expected 0.0, got %f", decoded.FloatField)
	}
}

func TestFloatPiMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{FloatField: 3.141592653589793}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if !floatEquals(decoded.FloatField, 3.141592653589793) {
		t.Errorf("Expected pi, got %f", decoded.FloatField)
	}
}

func TestFloatSmallMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{FloatField: 0.0000001}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if !floatEquals(decoded.FloatField, 0.0000001) {
		t.Errorf("Expected 0.0000001, got %f", decoded.FloatField)
	}
}

// ============================================================================
// String Edge Cases
// ============================================================================

func TestStringEmptyMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{StringField: ""}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.StringField != "" {
		t.Errorf("Expected empty string, got %q", decoded.StringField)
	}
}

func TestStringUnicodeMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{StringField: "Hello World 日本語"}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.StringField != "Hello World 日本語" {
		t.Errorf("String mismatch")
	}
}

func TestStringSpecialCharsMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{StringField: "Quote: \"test\" Backslash: \\"}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.StringField != "Quote: \"test\" Backslash: \\" {
		t.Errorf("String mismatch")
	}
}

// ============================================================================
// Boolean Edge Cases
// ============================================================================

func TestBoolTrueMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{BoolField: true}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.BoolField != true {
		t.Errorf("Expected true, got false")
	}
}

func TestBoolFalseMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{BoolField: false}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if decoded.BoolField != false {
		t.Errorf("Expected false, got true")
	}
}

// ============================================================================
// List Edge Cases
// ============================================================================

func TestListEmptyMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{ListField: []interface{}{}}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if len(decoded.ListField) != 0 {
		t.Errorf("Expected empty list")
	}
}

func TestListMixedTypesMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{ListField: []interface{}{1, "two", 3.0, true, false}}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if len(decoded.ListField) != 5 {
		t.Errorf("Expected 5 elements, got %d", len(decoded.ListField))
	}
}

// ============================================================================
// Map Edge Cases
// ============================================================================

func TestMapEmptyMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{MapField: map[string]interface{}{}}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if len(decoded.MapField) != 0 {
		t.Errorf("Expected empty map")
	}
}

func TestMapMixedValuesMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{MapField: map[string]interface{}{
		"str":  "hello",
		"num":  123,
		"bool": true,
	}}
	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if len(decoded.MapField) != 3 {
		t.Errorf("Expected 3 entries, got %d", len(decoded.MapField))
	}
}

// ============================================================================
// Security-Critical Combined Payload
// ============================================================================

func TestSecurityPayloadMsgPack(t *testing.T) {
	skipIfJsonOnly(t)
	p := ComprehensivePacket{
		IntField:      1234567890123456789,
		FloatField:    99999.99,
		StringField:   "TRANSFER:ACC-12345→ACC-67890",
		BoolField:     true,
		DatetimeField: time.Now().UTC(),
		ListField:     []interface{}{"audit1", "audit2", 1704067200},
		MapField: map[string]interface{}{
			"source_account": "ACC-12345",
			"dest_account":   "ACC-67890",
			"amount_cents":   int64(9999999),
			"currency":       "USD",
			"verified":       true,
		},
		EmbeddedMapField: map[string]interface{}{"sig_version": 2},
		BytesField:       []byte{0xDE, 0xAD, 0xBE, 0xEF},
	}

	data, err := msgpack.Marshal(p)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}

	var decoded ComprehensivePacket
	if err := msgpack.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}

	if decoded.IntField != p.IntField {
		t.Errorf("IntField mismatch")
	}
	if decoded.StringField != p.StringField {
		t.Errorf("StringField mismatch")
	}
	if decoded.BoolField != p.BoolField {
		t.Errorf("BoolField mismatch")
	}
	if len(decoded.ListField) != len(p.ListField) {
		t.Errorf("ListField length mismatch")
	}
	if len(decoded.MapField) != len(p.MapField) {
		t.Errorf("MapField length mismatch")
	}
}
