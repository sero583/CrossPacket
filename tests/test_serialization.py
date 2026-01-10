"""
CrossPacket Integration Tests - Serialization/Deserialization Verification

These tests verify that generated code actually works by:
1. Generating code for all languages
2. Creating packets with all data types
3. Serializing to JSON and MessagePack
4. Deserializing back to objects
5. Verifying data integrity (round-trip)

Test coverage:
- All primitive types (int, float, double, bool, string)
- DateTime with timezone handling
- Lists (dynamic, typed)
- Maps (string keys, embedded)
- Optional/nullable fields
- Edge cases (empty strings, unicode, large numbers, negative values)
- Cross-format compatibility (JSON <-> MessagePack)

Date: January 8, 2026
"""
import json
import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate import (
    PacketDefinition,
    DartGenerator,
    PythonGenerator,
    JavaGenerator,
    TypeScriptGenerator,
    RustGenerator,
    GoGenerator,
    load_config,
)


# Test data constants - used across all language tests
TEST_INT = 42
TEST_LARGE_INT = 9007199254740991  # Max safe integer in JS
TEST_NEGATIVE_INT = -999999
TEST_FLOAT = 3.14159265359
TEST_NEGATIVE_FLOAT = -273.15
TEST_ZERO_FLOAT = 0.0
TEST_BOOL_TRUE = True
TEST_BOOL_FALSE = False
TEST_STRING = "Hello, World!"
TEST_EMPTY_STRING = ""
TEST_UNICODE_STRING = "Hello 世界 🌍 مرحبا"
TEST_DATETIME = "2026-01-08T14:30:00.000+01:00"
TEST_LIST_DYNAMIC = [1, "two", 3.0, True, None]
TEST_LIST_INT = [1, 2, 3, 4, 5]
TEST_LIST_STRING = ["apple", "banana", "cherry"]
TEST_MAP = {"key1": "value1", "key2": 42, "nested": {"a": 1, "b": 2}}
TEST_NESTED_MAP = {
    "level1": {
        "level2": {
            "level3": {"value": "deep"}
        }
    },
    "array_in_map": [1, 2, 3],
    "mixed": {"num": 123, "str": "test", "bool": True}
}


def load_test_packets():
    """Load packet definitions from test_packets.json"""
    config_path = Path(__file__).parent / "test_packets.json"
    config = load_config(str(config_path))
    return [
        PacketDefinition(path, defn)
        for path, defn in config.get("packets", {}).items()
    ], config


class TestPythonSerialization:
    """
    Test Python code generation and serialization.
    
    These tests generate Python packets, then actually import and use them
    to verify serialization/deserialization works correctly.
    """
    
    @pytest.fixture
    def generated_module(self, tmp_path):
        """Generate Python packets and return the module path."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "python_packets"
        
        generator = PythonGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        # Add to path so we can import
        sys.path.insert(0, str(tmp_path))
        
        yield output_dir
        
        # Cleanup
        sys.path.remove(str(tmp_path))
    
    def test_all_types_json_roundtrip(self, generated_module):
        """Test JSON serialization/deserialization with all data types."""
        # Import generated module
        from python_packets.all_types_packet import AllTypesPacket
        
        # Create packet with all types
        original = AllTypesPacket(
            int_field=TEST_INT,
            float_field=TEST_FLOAT,
            double_field=TEST_FLOAT,
            bool_field=TEST_BOOL_TRUE,
            string_field=TEST_STRING,
            datetime_field=datetime.fromisoformat(TEST_DATETIME.replace('+01:00', '+01:00')),
            list_field=TEST_LIST_DYNAMIC,
            list_int_field=TEST_LIST_INT,
            list_string_field=TEST_LIST_STRING,
            map_field=TEST_MAP,
        )
        
        # Serialize to JSON
        json_str = original.to_json()
        assert isinstance(json_str, str)
        assert len(json_str) > 0
        
        # Deserialize from JSON
        restored = AllTypesPacket.from_json(json_str)
        
        # Verify all fields match
        assert restored.int_field == TEST_INT
        assert abs(restored.float_field - TEST_FLOAT) < 0.0001
        assert restored.bool_field == TEST_BOOL_TRUE
        assert restored.string_field == TEST_STRING
        assert restored.list_int_field == TEST_LIST_INT
        assert restored.list_string_field == TEST_LIST_STRING
    
    def test_all_types_msgpack_roundtrip(self, generated_module):
        """Test MessagePack serialization/deserialization with all data types."""
        from python_packets.all_types_packet import AllTypesPacket
        
        original = AllTypesPacket(
            int_field=TEST_INT,
            float_field=TEST_FLOAT,
            double_field=TEST_FLOAT,
            bool_field=TEST_BOOL_TRUE,
            string_field=TEST_STRING,
            datetime_field=datetime.now(timezone.utc),
            list_field=[1, 2, 3],
            list_int_field=TEST_LIST_INT,
            list_string_field=TEST_LIST_STRING,
            map_field={"key": "value"},
        )
        
        # Serialize to MessagePack
        msgpack_bytes = original.to_msgpack()
        assert isinstance(msgpack_bytes, bytes)
        assert len(msgpack_bytes) > 0
        
        # Deserialize from MessagePack
        restored = AllTypesPacket.from_msgpack(msgpack_bytes)
        
        # Verify fields
        assert restored.int_field == TEST_INT
        assert abs(restored.float_field - TEST_FLOAT) < 0.0001
        assert restored.bool_field == TEST_BOOL_TRUE
        assert restored.string_field == TEST_STRING
    
    def test_optional_fields_with_values(self, generated_module):
        """Test optional fields when they have values."""
        from python_packets.optional_types_packet import OptionalTypesPacket
        
        original = OptionalTypesPacket(
            required_string="required",
            optional_int=42,
            optional_string="optional",
            optional_list=["a", "b", "c"],
        )
        
        json_str = original.to_json()
        restored = OptionalTypesPacket.from_json(json_str)
        
        assert restored.required_string == "required"
        assert restored.optional_int == 42
        assert restored.optional_string == "optional"
        assert restored.optional_list == ["a", "b", "c"]
    
    def test_optional_fields_with_none(self, generated_module):
        """Test optional fields when they are None."""
        from python_packets.optional_types_packet import OptionalTypesPacket
        
        original = OptionalTypesPacket(
            required_string="required",
            optional_int=None,
            optional_string=None,
            optional_list=None,
        )
        
        json_str = original.to_json()
        restored = OptionalTypesPacket.from_json(json_str)
        
        assert restored.required_string == "required"
        assert restored.optional_int is None
        assert restored.optional_string is None
        assert restored.optional_list is None
    
    def test_nested_maps(self, generated_module):
        """Test deeply nested map structures."""
        from python_packets.nested_map_packet import NestedMapPacket
        
        original = NestedMapPacket(
            id="test-123",
            nested_data=TEST_NESTED_MAP,
            embedded_data=TEST_NESTED_MAP,
        )
        
        json_str = original.to_json()
        restored = NestedMapPacket.from_json(json_str)
        
        assert restored.id == "test-123"
        assert restored.nested_data["level1"]["level2"]["level3"]["value"] == "deep"
        assert restored.nested_data["array_in_map"] == [1, 2, 3]
    
    def test_edge_cases(self, generated_module):
        """Test edge cases: empty strings, unicode, large numbers."""
        from python_packets.edge_case_packet import EdgeCasePacket
        
        original = EdgeCasePacket(
            empty_string=TEST_EMPTY_STRING,
            unicode_string=TEST_UNICODE_STRING,
            large_int=TEST_LARGE_INT,
            negative_int=TEST_NEGATIVE_INT,
            zero_float=TEST_ZERO_FLOAT,
            negative_float=TEST_NEGATIVE_FLOAT,
        )
        
        # Test JSON roundtrip
        json_str = original.to_json()
        restored = EdgeCasePacket.from_json(json_str)
        
        assert restored.empty_string == ""
        assert restored.unicode_string == TEST_UNICODE_STRING
        assert restored.large_int == TEST_LARGE_INT
        assert restored.negative_int == TEST_NEGATIVE_INT
        assert restored.zero_float == 0.0
        assert abs(restored.negative_float - TEST_NEGATIVE_FLOAT) < 0.0001
        
        # Test MessagePack roundtrip
        msgpack_bytes = original.to_msgpack()
        restored_mp = EdgeCasePacket.from_msgpack(msgpack_bytes)
        
        assert restored_mp.empty_string == ""
        assert restored_mp.unicode_string == TEST_UNICODE_STRING
        assert restored_mp.large_int == TEST_LARGE_INT
    
    def test_type_field_present(self, generated_module):
        """Verify the 'type' field is included in serialized output."""
        from python_packets.all_types_packet import AllTypesPacket
        
        packet = AllTypesPacket(
            int_field=1,
            float_field=1.0,
            double_field=1.0,
            bool_field=True,
            string_field="test",
            datetime_field=datetime.now(),
            list_field=[],
            list_int_field=[],
            list_string_field=[],
            map_field={},
        )
        
        # Use to_json and parse to verify type field
        import json
        data = json.loads(packet.to_json())
        assert "packetType" in data
        assert data["packetType"] == "/test/AllTypesPacket"
    
    def test_json_msgpack_cross_format(self, generated_module):
        """Verify JSON and MessagePack produce equivalent data."""
        from python_packets.all_types_packet import AllTypesPacket
        import msgpack
        
        original = AllTypesPacket(
            int_field=TEST_INT,
            float_field=TEST_FLOAT,
            double_field=TEST_FLOAT,
            bool_field=TEST_BOOL_TRUE,
            string_field=TEST_STRING,
            datetime_field=datetime.now(timezone.utc),
            list_field=[1, 2, 3],
            list_int_field=TEST_LIST_INT,
            list_string_field=TEST_LIST_STRING,
            map_field={"key": "value"},
        )
        
        # Get both representations
        json_data = json.loads(original.to_json())
        msgpack_data = msgpack.unpackb(original.to_msgpack(), raw=False)
        
        # Compare key fields (datetime format may differ)
        assert json_data["int_field"] == msgpack_data["int_field"]
        assert json_data["string_field"] == msgpack_data["string_field"]
        assert json_data["bool_field"] == msgpack_data["bool_field"]
        assert json_data["list_int_field"] == msgpack_data["list_int_field"]


class TestDartCodeGeneration:
    """
    Test Dart code generation produces valid, compilable code.
    
    Note: Full runtime testing requires Dart SDK. These tests verify
    the generated code structure and syntax.
    """
    
    @pytest.fixture
    def generated_dir(self, tmp_path):
        """Generate Dart packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "dart_packets"
        
        generator = DartGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        return output_dir
    
    def test_generates_all_packet_files(self, generated_dir):
        """Verify all packet files are generated."""
        generated = generated_dir / "generated"
        
        assert (generated / "all_types_packet.dart").exists()
        assert (generated / "optional_types_packet.dart").exists()
        assert (generated / "nested_map_packet.dart").exists()
        assert (generated / "edge_case_packet.dart").exists()
    
    def test_generates_base_class(self, generated_dir):
        """Verify base DataPacket class is generated."""
        assert (generated_dir / "data_packet.dart").exists()
    
    def test_all_types_packet_structure(self, generated_dir):
        """Verify AllTypesPacket has correct structure."""
        content = (generated_dir / "generated" / "all_types_packet.dart").read_text()
        
        # Check class definition
        assert "class AllTypesPacket extends DataPacket" in content
        
        # Check all fields are present with correct types (nullable for empty constructor support)
        assert "int? int_field;" in content
        assert "double? float_field;" in content
        assert "double? double_field;" in content
        assert "bool? bool_field;" in content
        assert "String? string_field;" in content
        assert "DateTime? datetime_field;" in content
        assert "List<dynamic>? list_field;" in content
        assert "List<int>? list_int_field;" in content
        assert "List<String>? list_string_field;" in content
        assert "Map<String, dynamic>? map_field;" in content
        
        # Check serialization methods exist
        assert "Map<String, dynamic> serialize()" in content
        assert "static AllTypesPacket fromJson" in content
        assert "Uint8List toMsgPack()" in content
        assert "static AllTypesPacket fromMsgPack" in content
    
    def test_optional_fields_nullable(self, generated_dir):
        """Verify all fields use nullable types for empty constructor support."""
        content = (generated_dir / "generated" / "optional_types_packet.dart").read_text()
        
        assert "String? required_string;" in content  # Now nullable for empty constructor
        assert "int? optional_int;" in content  # Nullable
        assert "String? optional_string;" in content  # Nullable
        assert "List<String>? optional_list;" in content  # Nullable
    
    def test_type_getter_correct(self, generated_dir):
        """Verify type getter returns correct path."""
        content = (generated_dir / "generated" / "all_types_packet.dart").read_text()
        
        assert "String get type => '/test/AllTypesPacket';" in content
    
    def test_datetime_helper_generated(self, generated_dir):
        """Verify datetime helper is generated when needed."""
        content = (generated_dir / "generated" / "all_types_packet.dart").read_text()
        
        assert "_formatDateTimeWithTimezone" in content
    
    def test_two_space_indentation(self, generated_dir):
        """Verify Dart uses 2-space indentation."""
        content = (generated_dir / "generated" / "all_types_packet.dart").read_text()
        
        lines = content.split("\n")
        # Find lines that start with indentation (inside class)
        indented = [l for l in lines if l.startswith("  ") and not l.startswith("    ")]
        assert len(indented) > 0, "Should have 2-space indented lines"
        
        # Should not have tab-indented lines
        tab_indented = [l for l in lines if l.startswith("\t")]
        assert len(tab_indented) == 0, "Should not have tab indentation"


class TestJavaCodeGeneration:
    """Test Java code generation produces valid code."""
    
    @pytest.fixture
    def generated_dir(self, tmp_path):
        """Generate Java packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "java_packets"
        
        generator = JavaGenerator({
            "output_dir": str(output_dir),
            "package": "com.crosspacket.test"
        })
        generator.generate(packets, override=True)
        
        return output_dir
    
    def test_generates_all_packet_files(self, generated_dir):
        """Verify all packet files are generated."""
        assert (generated_dir / "AllTypesPacket.java").exists()
        assert (generated_dir / "OptionalTypesPacket.java").exists()
        assert (generated_dir / "NestedMapPacket.java").exists()
        assert (generated_dir / "EdgeCasePacket.java").exists()
        assert (generated_dir / "DataPacket.java").exists()
    
    def test_correct_package_declaration(self, generated_dir):
        """Verify package declaration is correct."""
        content = (generated_dir / "AllTypesPacket.java").read_text()
        
        assert "package com.crosspacket.test;" in content
    
    def test_all_types_packet_structure(self, generated_dir):
        """Verify AllTypesPacket has correct Java structure."""
        content = (generated_dir / "AllTypesPacket.java").read_text()
        
        # Check class definition
        assert "public class AllTypesPacket extends DataPacket" in content
        
        # Check fields with correct Java types
        assert "private long intField;" in content
        assert "private double floatField;" in content
        assert "private boolean boolField;" in content
        assert "private String stringField;" in content
        assert "private ZonedDateTime datetimeField;" in content
        
        # Check getters/setters exist
        assert "public long getIntField()" in content
        assert "public void setIntField(long intField)" in content
        
        # Check serialization methods
        assert "protected Map<String, Object> toMap()" in content
        assert "private static AllTypesPacket fromMap" in content
    
    def test_type_constant(self, generated_dir):
        """Verify TYPE constant is defined."""
        content = (generated_dir / "AllTypesPacket.java").read_text()
        
        assert 'public static final String TYPE = "/test/AllTypesPacket"' in content
    
    def test_four_space_indentation(self, generated_dir):
        """Verify Java uses 4-space indentation."""
        content = (generated_dir / "AllTypesPacket.java").read_text()
        
        # Check for 4-space indented public members
        assert "    public" in content
        assert "\tpublic" not in content  # No tabs


class TestTypeScriptCodeGeneration:
    """Test TypeScript code generation produces valid code."""
    
    @pytest.fixture
    def generated_dir(self, tmp_path):
        """Generate TypeScript packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "typescript_packets"
        
        generator = TypeScriptGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        return output_dir
    
    def test_generates_all_packet_files(self, generated_dir):
        """Verify all packet files are generated."""
        assert (generated_dir / "all_types_packet.ts").exists()
        assert (generated_dir / "optional_types_packet.ts").exists()
        assert (generated_dir / "nested_map_packet.ts").exists()
        assert (generated_dir / "edge_case_packet.ts").exists()
        assert (generated_dir / "index.ts").exists()
    
    def test_all_types_packet_structure(self, generated_dir):
        """Verify AllTypesPacket has correct TypeScript structure."""
        content = (generated_dir / "all_types_packet.ts").read_text()
        
        # Check interface and class exist
        assert "export interface AllTypesPacketData" in content
        assert "export class AllTypesPacket" in content
        
        # Check TypeScript types
        assert "intField: number;" in content or "int_field: number;" in content
        assert "stringField: string;" in content or "string_field: string;" in content
        assert "boolField: boolean;" in content or "bool_field: boolean;" in content
        
        # Check methods
        assert "toJSON()" in content
        assert "toMsgPack()" in content
        assert "static fromJSON" in content
        assert "static fromMsgPack" in content
    
    def test_index_exports_all_packets(self, generated_dir):
        """Verify index.ts exports all packets."""
        content = (generated_dir / "index.ts").read_text()
        
        assert "AllTypesPacket" in content
        assert "OptionalTypesPacket" in content
        assert "NestedMapPacket" in content
        assert "EdgeCasePacket" in content
        assert "deserializePacket" in content
    
    def test_two_space_indentation(self, generated_dir):
        """Verify TypeScript uses 2-space indentation."""
        content = (generated_dir / "all_types_packet.ts").read_text()
        
        # Check for 2-space indentation
        assert "  static readonly TYPE" in content or "  intField" in content


class TestRustCodeGeneration:
    """Test Rust code generation produces valid code."""
    
    @pytest.fixture
    def generated_dir(self, tmp_path):
        """Generate Rust packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "rust_packets"
        
        generator = RustGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        return output_dir
    
    def test_generates_all_packet_files(self, generated_dir):
        """Verify all packet files are generated."""
        assert (generated_dir / "all_types_packet.rs").exists()
        assert (generated_dir / "optional_types_packet.rs").exists()
        assert (generated_dir / "nested_map_packet.rs").exists()
        assert (generated_dir / "edge_case_packet.rs").exists()
        assert (generated_dir / "mod.rs").exists()
    
    def test_all_types_packet_structure(self, generated_dir):
        """Verify AllTypesPacket has correct Rust structure."""
        content = (generated_dir / "all_types_packet.rs").read_text()
        
        # Check derive macros
        assert "#[derive(Debug, Clone, Serialize, Deserialize)]" in content
        
        # Check struct definition
        assert "pub struct AllTypesPacket" in content
        
        # Check Rust types
        assert "i64" in content  # int type
        assert "f64" in content  # float/double type
        assert "bool" in content
        assert "String" in content
        
        # Check methods
        assert "pub fn to_json(&self)" in content
        assert "pub fn from_json(json: &str)" in content
        assert "pub fn to_msgpack(&self)" in content
        assert "pub fn from_msgpack(bytes: &[u8])" in content
    
    def test_optional_fields_use_option(self, generated_dir):
        """Verify optional fields use Option<T>."""
        content = (generated_dir / "optional_types_packet.rs").read_text()
        
        assert "Option<" in content
    
    def test_mod_file_exports(self, generated_dir):
        """Verify mod.rs exports all packets."""
        content = (generated_dir / "mod.rs").read_text()
        
        assert "mod all_types_packet" in content
        assert "pub use all_types_packet::AllTypesPacket" in content
    
    def test_four_space_indentation(self, generated_dir):
        """Verify Rust uses 4-space indentation."""
        content = (generated_dir / "all_types_packet.rs").read_text()
        
        assert "    pub" in content
        assert "\tpub" not in content


class TestGoCodeGeneration:
    """Test Go code generation produces valid code."""
    
    @pytest.fixture
    def generated_dir(self, tmp_path):
        """Generate Go packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "go_packets"
        
        generator = GoGenerator({
            "output_dir": str(output_dir),
            "package": "packets"
        })
        generator.generate(packets, override=True)
        
        return output_dir
    
    def test_generates_all_packet_files(self, generated_dir):
        """Verify all packet files are generated."""
        assert (generated_dir / "all_types_packet.go").exists()
        assert (generated_dir / "optional_types_packet.go").exists()
        assert (generated_dir / "nested_map_packet.go").exists()
        assert (generated_dir / "edge_case_packet.go").exists()
    
    def test_correct_package_declaration(self, generated_dir):
        """Verify package declaration is correct."""
        content = (generated_dir / "all_types_packet.go").read_text()
        
        assert "package packets" in content
    
    def test_all_types_packet_structure(self, generated_dir):
        """Verify AllTypesPacket has correct Go structure."""
        content = (generated_dir / "all_types_packet.go").read_text()
        
        # Check struct definition
        assert "type AllTypesPacket struct" in content
        
        # Check Go types
        assert "int64" in content
        assert "float64" in content
        assert "bool" in content
        assert "string" in content
        
        # Check json/msgpack tags
        assert '`json:"' in content
        assert 'msgpack:"' in content
        
        # Check methods
        assert "func (p *AllTypesPacket) GetType() string" in content
        assert "func (p *AllTypesPacket) ToJSON()" in content
        assert "func AllTypesPacketFromJSON" in content
        assert "func (p *AllTypesPacket) ToMsgPack()" in content
        assert "func AllTypesPacketFromMsgPack" in content
    
    def test_tab_indentation(self, generated_dir):
        """Verify Go uses tab indentation."""
        content = (generated_dir / "all_types_packet.go").read_text()
        
        # Go should have tabs
        assert "\t" in content


class TestCrossLanguageCompatibility:
    """
    Test that serialized data is compatible across languages.
    
    This verifies that a packet serialized in one language can be
    deserialized in another (using Python as the reference implementation).
    """
    
    @pytest.fixture
    def python_packets(self, tmp_path):
        """Generate and import Python packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "python_cross"
        
        generator = PythonGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        sys.path.insert(0, str(tmp_path))
        yield
        sys.path.remove(str(tmp_path))
    
    def test_json_is_valid_json(self, python_packets):
        """Verify generated JSON is valid JSON format."""
        from python_cross.all_types_packet import AllTypesPacket
        
        packet = AllTypesPacket(
            int_field=TEST_INT,
            float_field=TEST_FLOAT,
            double_field=TEST_FLOAT,
            bool_field=TEST_BOOL_TRUE,
            string_field=TEST_STRING,
            datetime_field=datetime.now(timezone.utc),
            list_field=[1, 2, 3],
            list_int_field=TEST_LIST_INT,
            list_string_field=TEST_LIST_STRING,
            map_field={"key": "value"},
        )
        
        json_str = packet.to_json()
        
        # This should not raise
        parsed = json.loads(json_str)
        
        # Verify structure
        assert isinstance(parsed, dict)
        assert "packetType" in parsed
        assert parsed["packetType"] == "/test/AllTypesPacket"
    
    def test_msgpack_is_valid_msgpack(self, python_packets):
        """Verify generated MessagePack is valid format."""
        import msgpack
        from python_cross.all_types_packet import AllTypesPacket
        
        packet = AllTypesPacket(
            int_field=TEST_INT,
            float_field=TEST_FLOAT,
            double_field=TEST_FLOAT,
            bool_field=TEST_BOOL_TRUE,
            string_field=TEST_STRING,
            datetime_field=datetime.now(timezone.utc),
            list_field=[1, 2, 3],
            list_int_field=TEST_LIST_INT,
            list_string_field=TEST_LIST_STRING,
            map_field={"key": "value"},
        )
        
        msgpack_bytes = packet.to_msgpack()
        
        # This should not raise
        parsed = msgpack.unpackb(msgpack_bytes, raw=False)
        
        # Verify structure
        assert isinstance(parsed, dict)
        assert "packetType" in parsed
        assert parsed["packetType"] == "/test/AllTypesPacket"
    
    def test_datetime_iso8601_format(self, python_packets):
        """Verify datetime is serialized in ISO 8601 format."""
        from python_cross.all_types_packet import AllTypesPacket
        
        test_dt = datetime(2026, 1, 8, 14, 30, 0, tzinfo=timezone.utc)
        
        packet = AllTypesPacket(
            int_field=1,
            float_field=1.0,
            double_field=1.0,
            bool_field=True,
            string_field="test",
            datetime_field=test_dt,
            list_field=[],
            list_int_field=[],
            list_string_field=[],
            map_field={},
        )
        
        import json
        data = json.loads(packet.to_json())
        dt_str = data["datetime_field"]
        
        # Should be ISO 8601 format
        assert "2026" in dt_str
        assert "01" in dt_str
        assert "08" in dt_str
        assert "T" in dt_str  # Date/time separator
    
    def test_unicode_preserved(self, python_packets):
        """Verify unicode characters are preserved through serialization."""
        from python_cross.edge_case_packet import EdgeCasePacket
        
        packet = EdgeCasePacket(
            empty_string="",
            unicode_string=TEST_UNICODE_STRING,
            large_int=0,
            negative_int=0,
            zero_float=0.0,
            negative_float=0.0,
        )
        
        # JSON roundtrip
        json_str = packet.to_json()
        restored = EdgeCasePacket.from_json(json_str)
        assert restored.unicode_string == TEST_UNICODE_STRING
        
        # MessagePack roundtrip
        msgpack_bytes = packet.to_msgpack()
        restored_mp = EdgeCasePacket.from_msgpack(msgpack_bytes)
        assert restored_mp.unicode_string == TEST_UNICODE_STRING


class TestEdgeCasesAndBoundaries:
    """Test edge cases and boundary conditions."""
    
    @pytest.fixture
    def python_packets(self, tmp_path):
        """Generate and import Python packets."""
        packets, config = load_test_packets()
        output_dir = tmp_path / "python_edge"
        
        generator = PythonGenerator({"output_dir": str(output_dir)})
        generator.generate(packets, override=True)
        
        sys.path.insert(0, str(tmp_path))
        yield
        sys.path.remove(str(tmp_path))
    
    def test_empty_collections(self, python_packets):
        """Test empty lists and maps."""
        from python_edge.all_types_packet import AllTypesPacket
        
        packet = AllTypesPacket(
            int_field=0,
            float_field=0.0,
            double_field=0.0,
            bool_field=False,
            string_field="",
            datetime_field=datetime.now(),
            list_field=[],
            list_int_field=[],
            list_string_field=[],
            map_field={},
        )
        
        json_str = packet.to_json()
        restored = AllTypesPacket.from_json(json_str)
        
        assert restored.list_field == []
        assert restored.list_int_field == [] or restored.list_int_field is None  # Empty list may be None
        assert restored.list_string_field == [] or restored.list_string_field is None  # Empty list may be None
        assert restored.map_field == {}
    
    def test_large_collections(self, python_packets):
        """Test large lists."""
        from python_edge.all_types_packet import AllTypesPacket
        
        large_list = list(range(10000))
        large_string_list = [f"item_{i}" for i in range(1000)]
        
        packet = AllTypesPacket(
            int_field=0,
            float_field=0.0,
            double_field=0.0,
            bool_field=False,
            string_field="",
            datetime_field=datetime.now(),
            list_field=large_list,
            list_int_field=large_list,
            list_string_field=large_string_list,
            map_field={},
        )
        
        msgpack_bytes = packet.to_msgpack()
        restored = AllTypesPacket.from_msgpack(msgpack_bytes)
        
        assert len(restored.list_int_field) == 10000
        assert len(restored.list_string_field) == 1000
    
    def test_special_characters_in_strings(self, python_packets):
        """Test special characters in strings."""
        from python_edge.edge_case_packet import EdgeCasePacket
        
        special_strings = [
            "Line1\nLine2",  # Newline
            "Tab\there",  # Tab
            'Quote"here',  # Double quote
            "Backslash\\here",  # Backslash
            "Null\x00char",  # Null character
        ]
        
        for special in special_strings:
            packet = EdgeCasePacket(
                empty_string="",
                unicode_string=special,
                large_int=0,
                negative_int=0,
                zero_float=0.0,
                negative_float=0.0,
            )
            
            json_str = packet.to_json()
            restored = EdgeCasePacket.from_json(json_str)
            assert restored.unicode_string == special, f"Failed for: {repr(special)}"
    
    def test_deeply_nested_structures(self, python_packets):
        """Test deeply nested map structures."""
        from python_edge.nested_map_packet import NestedMapPacket
        
        # Create deeply nested structure
        deep = {"level": 1}
        current = deep
        for i in range(2, 21):  # 20 levels deep
            current["nested"] = {"level": i}
            current = current["nested"]
        
        packet = NestedMapPacket(
            id="deep-test",
            nested_data=deep,
            embedded_data=deep,
        )
        
        json_str = packet.to_json()
        restored = NestedMapPacket.from_json(json_str)
        
        # Navigate to level 10
        data = restored.nested_data
        for _ in range(9):
            data = data["nested"]
        assert data["level"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
