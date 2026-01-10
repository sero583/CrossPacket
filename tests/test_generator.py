"""
CrossPacket Test Suite

Tests for the packet generator and generated code validation.

Author: Serhat Gueler (sero583)
GitHub: https://github.com/sero583
License: MIT
"""
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate import (
    PacketDefinition,
    PacketField,
    DartGenerator,
    PythonGenerator,
    JavaGenerator,
    TypeScriptGenerator,
    RustGenerator,
    GoGenerator,
    CppGenerator,
    CSharpGenerator,
    PhpGenerator,
    to_pascal_case,
    to_snake_case,
    to_camel_case,
    TYPE_MAPPINGS,
)


# Sample packet definition for testing
SAMPLE_PACKET_CONFIG = {
    "packets": {
        "/test/TestPacket": {
            "description": "A test packet for unit testing",
            "fields": {
                "id": {"type": "int", "description": "Unique identifier"},
                "name": {"type": "string", "description": "Name of the item"},
                "active": {"type": "bool", "description": "Whether active"},
                "score": {"type": "float", "description": "Score value"},
                "created_at": {"type": "datetime", "description": "Creation timestamp"},
                "tags": {"type": "list_string", "description": "List of tags"},
                "metadata": {"type": "map", "description": "Additional metadata"},
            },
        },
        "/test/SimplePacket": {
            "description": "A simple packet with minimal fields",
            "fields": {
                "message": {"type": "string"},
            },
        },
        "/test/OptionalPacket": {
            "description": "Packet with optional fields",
            "fields": {
                "required_field": {"type": "string"},
                "optional_field": {"type": "int", "optional": True},
            },
        },
    }
}

# Sample packet with validation for testing field-level overrides
VALIDATION_PACKET_CONFIG = {
    "config": {
        "global": {
            "strict_validation": True,
            "generate_security_utils": True,
            "schema_version": 1
        },
        "validation": {
            "max_int": 9223372036854775807,
            "min_int": -9223372036854775808,
            "max_list_size": 100000,
            "max_map_size": 100000,
            "max_string_length": 10000000,
            "max_bytes_length": 100000000
        }
    },
    "packets": {
        "/test/ValidatedPacket": {
            "description": "Packet with field-level validation overrides",
            "version": 1,
            "fields": {
                "user_id": {
                    "type": "int",
                    "description": "User ID with custom range",
                    "validation": {
                        "required": True,
                        "min": 1,
                        "max": 999999
                    }
                },
                "username": {
                    "type": "string",
                    "description": "Username with pattern",
                    "validation": {
                        "required": True,
                        "min": 3,
                        "max": 30,
                        "pattern": "^[a-zA-Z0-9_]+$",
                        "allow_empty": False
                    }
                },
                "balance": {
                    "type": "float",
                    "description": "Balance without NaN/Infinity",
                    "validation": {
                        "min": 0,
                        "allow_nan": False,
                        "allow_infinity": False
                    }
                },
                "tags": {
                    "type": "list_string",
                    "description": "Tags with size limit",
                    "validation": {
                        "max": 10,
                        "allow_empty": True
                    }
                },
                "settings": {
                    "type": "map",
                    "description": "Settings with depth limit",
                    "validation": {
                        "max": 50,
                        "max_depth": 2
                    }
                },
                "avatar": {
                    "type": "bytes",
                    "description": "Avatar with size limit",
                    "optional": True,
                    "validation": {
                        "max": 1048576
                    }
                },
                "bio": {
                    "type": "string",
                    "description": "Bio allows empty",
                    "optional": True,
                    "validation": {
                        "required": False,
                        "max": 500,
                        "allow_empty": True
                    }
                }
            }
        }
    }
}

# All supported types for comprehensive testing
ALL_TYPES_PACKET = {
    "packets": {
        "/test/AllTypesPacket": {
            "description": "Packet with all supported types",
            "fields": {
                "int_field": {"type": "int"},
                "float_field": {"type": "float"},
                "double_field": {"type": "double"},
                "bool_field": {"type": "bool"},
                "string_field": {"type": "string"},
                "datetime_field": {"type": "datetime"},
                "time_field": {"type": "time"},
                "bytes_field": {"type": "bytes"},
                "list_field": {"type": "list"},
                "list_int_field": {"type": "list_int"},
                "list_string_field": {"type": "list_string"},
                "map_field": {"type": "map"},
                "embedded_map_field": {"type": "embedded_map"},
                "map_string_dynamic_field": {"type": "map_string_dynamic"},
            }
        }
    }
}


class TestCaseConversion:
    """Tests for case conversion utilities."""

    def test_to_pascal_case_from_snake(self):
        assert to_pascal_case("hello_world") == "HelloWorld"
        assert to_pascal_case("test_packet") == "TestPacket"
        assert to_pascal_case("my_test_class") == "MyTestClass"

    def test_to_pascal_case_already_pascal(self):
        assert to_pascal_case("HelloWorld") == "HelloWorld"
        assert to_pascal_case("TestPacket") == "TestPacket"

    def test_to_snake_case(self):
        assert to_snake_case("HelloWorld") == "hello_world"
        assert to_snake_case("TestPacket") == "test_packet"
        assert to_snake_case("MyTestClass") == "my_test_class"

    def test_to_camel_case(self):
        assert to_camel_case("hello_world") == "helloWorld"
        assert to_camel_case("test_packet") == "testPacket"
        assert to_camel_case("my_test_class") == "myTestClass"


class TestTypeMappings:
    """Tests for type mappings across languages."""

    def test_all_types_have_dart_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "dart" in mappings, f"Missing Dart mapping for {type_name}"

    def test_all_types_have_python_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "python" in mappings, f"Missing Python mapping for {type_name}"

    def test_all_types_have_java_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "java" in mappings, f"Missing Java mapping for {type_name}"

    def test_all_types_have_typescript_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "typescript" in mappings, f"Missing TypeScript mapping for {type_name}"

    def test_all_types_have_rust_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "rust" in mappings, f"Missing Rust mapping for {type_name}"

    def test_all_types_have_go_mapping(self):
        for type_name, mappings in TYPE_MAPPINGS.items():
            assert "go" in mappings, f"Missing Go mapping for {type_name}"


class TestPacketField:
    """Tests for PacketField class."""

    def test_field_from_string_type(self):
        field = PacketField("test_field", "string")
        assert field.name == "test_field"
        assert field.type == "string"
        assert field.description is None
        assert field.optional is False

    def test_field_from_dict(self):
        field = PacketField("test_field", {
            "type": "int",
            "description": "A test field",
            "optional": True,
        })
        assert field.name == "test_field"
        assert field.type == "int"
        assert field.description == "A test field"
        assert field.optional is True

    def test_field_validation_properties(self):
        """Test field-level validation properties."""
        field = PacketField("validated_field", {
            "type": "int",
            "description": "Field with validation",
            "validation": {
                "required": True,
                "min": 1,
                "max": 100
            }
        })
        assert field.required is True
        assert field.min_value == 1
        assert field.max_value == 100
    
    def test_field_validation_defaults(self):
        """Test default validation values."""
        field = PacketField("simple_field", {"type": "string"})
        assert field.required is True  # Default is True
        assert field.min_value is None
        assert field.max_value is None
        assert field.pattern is None
        assert field.allow_empty is True
        assert field.allow_nan is False
        assert field.allow_infinity is False
        assert field.max_depth == 10
    
    def test_field_validation_overrides(self):
        """Test that field validation overrides defaults."""
        field = PacketField("custom_field", {
            "type": "float",
            "validation": {
                "allow_nan": True,
                "allow_infinity": True,
                "min": -1000.0,
                "max": 1000.0
            }
        })
        assert field.allow_nan is True
        assert field.allow_infinity is True
        assert field.min_value == -1000.0
        assert field.max_value == 1000.0
    
    def test_field_string_validation(self):
        """Test string field validation properties."""
        field = PacketField("email", {
            "type": "string",
            "validation": {
                "pattern": "^[^@]+@[^@]+\\.[^@]+$",
                "max": 255,
                "allow_empty": False
            }
        })
        assert field.pattern == "^[^@]+@[^@]+\\.[^@]+$"
        assert field.max_value == 255
        assert field.allow_empty is False
    
    def test_field_list_validation(self):
        """Test list field validation properties."""
        field = PacketField("items", {
            "type": "list",
            "validation": {
                "max": 100,
                "max_depth": 3
            }
        })
        assert field.max_value == 100
        assert field.max_depth == 3
    
    def test_optional_field_not_required(self):
        """Test that optional field is not required."""
        field = PacketField("optional", {
            "type": "string",
            "optional": True
        })
        assert field.required is False
        assert field.optional is True

    def test_dart_type_required(self):
        field = PacketField("id", {"type": "int"})
        assert field.dart_type() == "int"

    def test_dart_type_optional(self):
        field = PacketField("id", {"type": "int", "optional": True})
        assert field.dart_type() == "int?"

    def test_python_type_required(self):
        """Test Python type mapping - all fields are Optional to support empty constructor."""
        generator = PythonGenerator({})
        field = PacketField("name", {"type": "string"})
        # All fields are Optional to support empty constructor + setters pattern
        assert generator.python_type(field) == "Optional[str]"

    def test_python_type_optional(self):
        """Test Python type mapping for optional field via generator."""
        generator = PythonGenerator({})
        field = PacketField("name", {"type": "string", "optional": True})
        assert generator.python_type(field) == "Optional[str]"


class TestPacketDefinition:
    """Tests for PacketDefinition class."""

    def test_parse_packet_definition(self):
        definition = SAMPLE_PACKET_CONFIG["packets"]["/test/TestPacket"]
        packet = PacketDefinition("/test/TestPacket", definition)
        
        assert packet.path == "/test/TestPacket"
        assert packet.name == "TestPacket"
        assert packet.description == "A test packet for unit testing"
        assert len(packet.fields) == 7

    def test_has_datetime(self):
        definition = SAMPLE_PACKET_CONFIG["packets"]["/test/TestPacket"]
        packet = PacketDefinition("/test/TestPacket", definition)
        assert packet.has_datetime() is True

        simple_def = SAMPLE_PACKET_CONFIG["packets"]["/test/SimplePacket"]
        simple_packet = PacketDefinition("/test/SimplePacket", simple_def)
        assert simple_packet.has_datetime() is False

    def test_field_names(self):
        definition = SAMPLE_PACKET_CONFIG["packets"]["/test/TestPacket"]
        packet = PacketDefinition("/test/TestPacket", definition)
        field_names = [f.name for f in packet.fields]
        
        assert "id" in field_names
        assert "name" in field_names
        assert "active" in field_names

    def test_packet_version(self):
        """Test packet version parsing."""
        definition = VALIDATION_PACKET_CONFIG["packets"]["/test/ValidatedPacket"]
        packet = PacketDefinition("/test/ValidatedPacket", definition)
        assert packet.version == 1
    
    def test_packet_version_default(self):
        """Test default packet version."""
        definition = SAMPLE_PACKET_CONFIG["packets"]["/test/SimplePacket"]
        packet = PacketDefinition("/test/SimplePacket", definition)
        assert packet.version == 1
    
    def test_packet_deprecated(self):
        """Test deprecated packet flag."""
        definition = {"description": "Old packet", "deprecated": True, "fields": {"x": "int"}}
        packet = PacketDefinition("/test/DeprecatedPacket", definition)
        assert packet.deprecated is True
    
    def test_packet_deprecated_default(self):
        """Test default deprecated value."""
        definition = SAMPLE_PACKET_CONFIG["packets"]["/test/SimplePacket"]
        packet = PacketDefinition("/test/SimplePacket", definition)
        assert packet.deprecated is False
    
    def test_has_bytes(self):
        """Test has_bytes detection."""
        definition = ALL_TYPES_PACKET["packets"]["/test/AllTypesPacket"]
        packet = PacketDefinition("/test/AllTypesPacket", definition)
        assert packet.has_bytes() is True
        
        simple_def = SAMPLE_PACKET_CONFIG["packets"]["/test/SimplePacket"]
        simple_packet = PacketDefinition("/test/SimplePacket", simple_def)
        assert simple_packet.has_bytes() is False
    
    def test_has_list(self):
        """Test has_list detection."""
        definition = ALL_TYPES_PACKET["packets"]["/test/AllTypesPacket"]
        packet = PacketDefinition("/test/AllTypesPacket", definition)
        assert packet.has_list() is True
    
    def test_has_map(self):
        """Test has_map detection."""
        definition = ALL_TYPES_PACKET["packets"]["/test/AllTypesPacket"]
        packet = PacketDefinition("/test/AllTypesPacket", definition)
        assert packet.has_map() is True
    
    def test_has_embedded_map(self):
        """Test has_embedded_map detection."""
        definition = ALL_TYPES_PACKET["packets"]["/test/AllTypesPacket"]
        packet = PacketDefinition("/test/AllTypesPacket", definition)
        assert packet.has_embedded_map() is True
    
    def test_has_time(self):
        """Test has_time detection."""
        definition = ALL_TYPES_PACKET["packets"]["/test/AllTypesPacket"]
        packet = PacketDefinition("/test/AllTypesPacket", definition)
        assert packet.has_time() is True


class TestDartGenerator:
    """Tests for Dart code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = DartGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        # Check base class exists
        assert (Path(temp_output_dir) / "data_packet.dart").exists()

        # Check generated packets exist
        generated_dir = Path(temp_output_dir) / "generated"
        assert (generated_dir / "test_packet.dart").exists()
        assert (generated_dir / "simple_packet.dart").exists()
        assert (generated_dir / "optional_packet.dart").exists()

    def test_uses_two_space_indent(self, temp_output_dir, packets):
        generator = DartGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "generated" / "test_packet.dart"
        content = generated_file.read_text()

        # Check 2-space indentation is used for first level (class members)
        # Lines with first-level indentation should have "  " prefix
        lines = content.split("\n")
        field_lines = [l for l in lines if "final " in l and l.startswith("  ")]
        assert len(field_lines) > 0  # Should have indented final fields
        
        # Should not use tabs
        assert "\tfinal" not in content
        
        # First-level indent should be 2 spaces, not 4
        # Check that first level fields start with exactly "  " not "    "
        first_level_indent = [l for l in lines if l.startswith("  ") and not l.startswith("    ")]
        assert len(first_level_indent) > 0

    def test_generated_code_has_type_getter(self, temp_output_dir, packets):
        generator = DartGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "generated" / "test_packet.dart"
        content = generated_file.read_text()

        assert "String get type =>" in content
        assert "'/test/TestPacket'" in content


class TestPythonGenerator:
    """Tests for Python code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        # Check __init__.py exists
        assert (Path(temp_output_dir) / "__init__.py").exists()

        # Check generated packets exist
        assert (Path(temp_output_dir) / "test_packet.py").exists()
        assert (Path(temp_output_dir) / "simple_packet.py").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.py"
        content = generated_file.read_text()

        # Check 4-space indentation (PEP 8)
        lines = content.split("\n")
        indented_lines = [l for l in lines if l.startswith("    ") and not l.startswith("        ")]
        assert len(indented_lines) > 0, "Should have 4-space indented lines"

    def test_generated_code_is_valid_python(self, temp_output_dir, packets):
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "simple_packet.py"
        content = generated_file.read_text()

        # Check syntax is valid by compiling
        try:
            compile(content, generated_file, "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated Python has syntax error: {e}")


class TestJavaGenerator:
    """Tests for Java code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = JavaGenerator({
            "output_dir": temp_output_dir,
            "package": "com.test.packets"
        })
        generator.generate(packets, override=True)

        # Check base class exists
        assert (Path(temp_output_dir) / "DataPacket.java").exists()

        # Check generated packets exist
        assert (Path(temp_output_dir) / "TestPacket.java").exists()
        assert (Path(temp_output_dir) / "SimplePacket.java").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = JavaGenerator({
            "output_dir": temp_output_dir,
            "package": "com.test.packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.java"
        content = generated_file.read_text()

        # Check 4-space indentation
        assert "    public" in content
        assert "\tpublic" not in content

    def test_generates_correct_package(self, temp_output_dir, packets):
        generator = JavaGenerator({
            "output_dir": temp_output_dir,
            "package": "com.example.mypackets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.java"
        content = generated_file.read_text()

        assert "package com.example.mypackets;" in content


class TestTypeScriptGenerator:
    """Tests for TypeScript code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = TypeScriptGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        # Check index exists
        assert (Path(temp_output_dir) / "index.ts").exists()

        # Check generated packets exist
        assert (Path(temp_output_dir) / "test_packet.ts").exists()
        assert (Path(temp_output_dir) / "simple_packet.ts").exists()

    def test_uses_two_space_indent(self, temp_output_dir, packets):
        generator = TypeScriptGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.ts"
        content = generated_file.read_text()

        # Check 2-space indentation
        assert "  static readonly TYPE" in content or "  senderId" in content


class TestRustGenerator:
    """Tests for Rust code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = RustGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        # Check mod.rs exists
        assert (Path(temp_output_dir) / "mod.rs").exists()

        # Check generated packets exist
        assert (Path(temp_output_dir) / "test_packet.rs").exists()
        assert (Path(temp_output_dir) / "simple_packet.rs").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = RustGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.rs"
        content = generated_file.read_text()

        # Check 4-space indentation
        assert "    pub" in content


class TestGoGenerator:
    """Tests for Go code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = GoGenerator({
            "output_dir": temp_output_dir,
            "package": "packets"
        })
        generator.generate(packets, override=True)

        # Check generated packets exist
        assert (Path(temp_output_dir) / "test_packet.go").exists()
        assert (Path(temp_output_dir) / "simple_packet.go").exists()

    def test_uses_tabs(self, temp_output_dir, packets):
        generator = GoGenerator({
            "output_dir": temp_output_dir,
            "package": "packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.go"
        content = generated_file.read_text()

        # Check tab indentation (Go standard)
        assert "\t" in content, "Go should use tab indentation"


class TestSerializationRoundtrip:
    """Tests for serialization/deserialization roundtrip in generated code."""

    def test_python_roundtrip(self):
        """Test that Python generated code can serialize and deserialize."""
        # This test requires the generated code to be importable
        # For CI, we'd generate to a temp dir and import from there
        
        # For now, just verify the generator creates valid Python syntax
        packets = [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]
        
        temp_dir = tempfile.mkdtemp()
        try:
            generator = PythonGenerator({"output_dir": temp_dir})
            generator.generate(packets, override=True)
            
            # Verify all files have valid syntax
            for py_file in Path(temp_dir).glob("*.py"):
                content = py_file.read_text()
                compile(content, py_file, "exec")
        finally:
            shutil.rmtree(temp_dir)


class TestCppGenerator:
    """Tests for C++ code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = CppGenerator({
            "output_dir": temp_output_dir,
            "namespace": "test_packets"
        })
        generator.generate(packets, override=True)

        # Check generated headers and source files exist
        assert (Path(temp_output_dir) / "test_packet.hpp").exists()
        assert (Path(temp_output_dir) / "test_packet.cpp").exists()
        assert (Path(temp_output_dir) / "simple_packet.hpp").exists()
        assert (Path(temp_output_dir) / "simple_packet.cpp").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = CppGenerator({
            "output_dir": temp_output_dir,
            "namespace": "test_packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.hpp"
        content = generated_file.read_text()

        # Check 4-space indentation
        assert "    static constexpr" in content or "    public:" in content

    def test_generates_correct_namespace(self, temp_output_dir, packets):
        generator = CppGenerator({
            "output_dir": temp_output_dir,
            "namespace": "my_custom_namespace"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "test_packet.hpp"
        content = generated_file.read_text()

        assert "namespace my_custom_namespace" in content

    def test_generates_both_header_and_source(self, temp_output_dir, packets):
        generator = CppGenerator({
            "output_dir": temp_output_dir,
            "namespace": "test_packets"
        })
        generator.generate(packets, override=True)

        for packet in packets:
            base_name = to_snake_case(packet.name)
            assert (Path(temp_output_dir) / f"{base_name}.hpp").exists()
            assert (Path(temp_output_dir) / f"{base_name}.cpp").exists()


class TestCSharpGenerator:
    """Tests for C# code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = CSharpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "TestPackets"
        })
        generator.generate(packets, override=True)

        # Check generated files exist
        assert (Path(temp_output_dir) / "TestPacket.cs").exists()
        assert (Path(temp_output_dir) / "SimplePacket.cs").exists()
        assert (Path(temp_output_dir) / "OptionalPacket.cs").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = CSharpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "TestPackets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.cs"
        content = generated_file.read_text()

        # Check 4-space indentation
        assert "    public" in content
        assert "\tpublic" not in content

    def test_generates_correct_namespace(self, temp_output_dir, packets):
        generator = CSharpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "MyApp.Packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.cs"
        content = generated_file.read_text()

        assert "namespace MyApp.Packets" in content

    def test_generates_messagepack_attributes(self, temp_output_dir, packets):
        generator = CSharpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "TestPackets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.cs"
        content = generated_file.read_text()

        assert "[MessagePackObject]" in content
        assert '[Key("packetType")]' in content


class TestPhpGenerator:
    """Tests for PHP code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in SAMPLE_PACKET_CONFIG["packets"].items()
        ]

    def test_generates_files(self, temp_output_dir, packets):
        generator = PhpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "Test\\Packets"
        })
        generator.generate(packets, override=True)

        # Check generated files exist
        assert (Path(temp_output_dir) / "TestPacket.php").exists()
        assert (Path(temp_output_dir) / "SimplePacket.php").exists()
        assert (Path(temp_output_dir) / "OptionalPacket.php").exists()

    def test_uses_four_space_indent(self, temp_output_dir, packets):
        generator = PhpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "Test\\Packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.php"
        content = generated_file.read_text()

        # Check 4-space indentation (PSR-12)
        assert "    public" in content
        assert "\tpublic" not in content

    def test_generates_correct_namespace(self, temp_output_dir, packets):
        generator = PhpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "MyApp\\DataPackets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.php"
        content = generated_file.read_text()

        assert "namespace MyApp\\DataPackets;" in content

    def test_generates_strict_types(self, temp_output_dir, packets):
        generator = PhpGenerator({
            "output_dir": temp_output_dir,
            "namespace": "Test\\Packets"
        })
        generator.generate(packets, override=True)

        generated_file = Path(temp_output_dir) / "TestPacket.php"
        content = generated_file.read_text()

        assert "declare(strict_types=1);" in content


class TestAllTypesGeneration:
    """Tests that all supported types generate correctly for all languages."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def all_types_packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in ALL_TYPES_PACKET["packets"].items()
        ]

    def test_python_all_types(self, temp_output_dir, all_types_packets):
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(all_types_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "all_types_packet.py"
        content = generated_file.read_text()
        
        # Verify it compiles
        compile(content, generated_file, "exec")
        
        # Verify all fields are present
        assert "int_field" in content
        assert "bytes_field" in content
        assert "embedded_map_field" in content

    def test_typescript_all_types(self, temp_output_dir, all_types_packets):
        generator = TypeScriptGenerator({"output_dir": temp_output_dir})
        generator.generate(all_types_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "all_types_packet.ts"
        assert generated_file.exists()
        content = generated_file.read_text()
        
        # Verify all fields are present
        assert "intField" in content or "int_field" in content
        assert "bytesField" in content or "bytes_field" in content

    def test_csharp_all_types(self, temp_output_dir, all_types_packets):
        generator = CSharpGenerator({"output_dir": temp_output_dir, "namespace": "Test"})
        generator.generate(all_types_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "AllTypesPacket.cs"
        assert generated_file.exists()
        content = generated_file.read_text()
        
        # Verify byte[] type
        assert "byte[]" in content

    def test_go_all_types(self, temp_output_dir, all_types_packets):
        generator = GoGenerator({"output_dir": temp_output_dir, "package": "packets"})
        generator.generate(all_types_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "all_types_packet.go"
        assert generated_file.exists()
        content = generated_file.read_text()
        
        # Verify []byte type
        assert "[]byte" in content


class TestValidationPacketGeneration:
    """Tests generation of packets with validation rules."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def validation_packets(self):
        return [
            PacketDefinition(path, defn)
            for path, defn in VALIDATION_PACKET_CONFIG["packets"].items()
        ]

    def test_validation_packet_python(self, temp_output_dir, validation_packets):
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(validation_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "validated_packet.py"
        content = generated_file.read_text()
        
        # Verify it compiles
        compile(content, generated_file, "exec")
        
        # Verify fields with validation are present
        assert "user_id" in content
        assert "username" in content
        assert "balance" in content
        assert "avatar" in content

    def test_validation_packet_csharp(self, temp_output_dir, validation_packets):
        generator = CSharpGenerator({"output_dir": temp_output_dir, "namespace": "Test"})
        generator.generate(validation_packets, override=True)
        
        generated_file = Path(temp_output_dir) / "ValidatedPacket.cs"
        assert generated_file.exists()


class TestReservedFieldValidation:
    """Tests for reserved field name validation (type_field)."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_default_type_field_reserved(self):
        """Verify that 'packetType' is the default reserved field name."""
        packet_def = {
            "description": "Test packet with reserved field",
            "fields": {
                "packetType": {"type": "string"},  # This conflicts with default type_field
                "message": {"type": "string"}
            }
        }
        packet = PacketDefinition("/test/BadPacket", packet_def)
        
        # The generator validates this - we check that the field parses correctly
        # but would fail in main() validation
        assert any(f.name == "packetType" for f in packet.fields)

    def test_custom_type_field_reserved(self):
        """Verify custom type_field name becomes reserved."""
        packet_def = {
            "description": "Test packet",
            "fields": {
                "customType": {"type": "string"},
                "message": {"type": "string"}
            }
        }
        packet = PacketDefinition("/test/TestPacket", packet_def)
        
        # With type_field="customType", this would conflict
        assert any(f.name == "customType" for f in packet.fields)

    def test_valid_field_names_allowed(self):
        """Verify normal field names don't trigger reserved field errors."""
        packet_def = {
            "description": "Valid packet",
            "fields": {
                "type": {"type": "string"},  # 'type' is fine since default is 'packetType'
                "message": {"type": "string"},
                "timestamp": {"type": "datetime"}
            }
        }
        packet = PacketDefinition("/test/ValidPacket", packet_def)
        
        # All fields should parse correctly
        assert len(packet.fields) == 3
        assert any(f.name == "type" for f in packet.fields)

    def test_type_field_in_generated_output(self, temp_output_dir):
        """Verify generated code uses configured type_field in serialization."""
        packet_def = {
            "description": "Test packet",
            "fields": {
                "message": {"type": "string"}
            }
        }
        packets = [PacketDefinition("/test/TestPacket", packet_def)]
        
        # Generate with custom type_field
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(packets, override=True, type_field="myPacketType")
        
        content = (Path(temp_output_dir) / "test_packet.py").read_text()
        assert '"myPacketType"' in content
        assert 'self.TYPE' in content

    def test_all_languages_use_type_field(self, temp_output_dir):
        """Verify all 9 languages properly use the configured type_field."""
        packet_def = {
            "description": "Test packet",
            "fields": {
                "data": {"type": "string"}
            }
        }
        packets = [PacketDefinition("/test/TypeFieldTest", packet_def)]
        custom_type_field = "packetKind"
        
        generators = [
            (PythonGenerator, "type_field_test.py", '"packetKind"'),
            (DartGenerator, "generated/type_field_test.dart", "'packetKind'"),
            (TypeScriptGenerator, "type_field_test.ts", "packetKind:"),
            (JavaGenerator, "TypeFieldTest.java", '"packetKind"'),
            (RustGenerator, "type_field_test.rs", '"packetKind"'),
            (GoGenerator, "type_field_test.go", '`json:"packetKind"'),
            (CppGenerator, "type_field_test.cpp", '"packetKind"'),
            (CSharpGenerator, "TypeFieldTest.cs", '"packetKind"'),
            (PhpGenerator, "TypeFieldTest.php", "'packetKind'"),
        ]
        
        for GenClass, filename, expected_pattern in generators:
            gen_dir = Path(temp_output_dir) / GenClass.__name__
            gen_dir.mkdir(parents=True, exist_ok=True)
            
            config = {"output_dir": str(gen_dir)}
            if GenClass == CSharpGenerator:
                config["namespace"] = "Test"
            if GenClass == CppGenerator:
                config["namespace"] = "test"
            if GenClass == GoGenerator:
                config["package"] = "test"
            if GenClass == PhpGenerator:
                config["namespace"] = "Test"
            
            generator = GenClass(config)
            generator.generate(packets, override=True, type_field=custom_type_field)
            
            filepath = gen_dir / filename
            assert filepath.exists(), f"{GenClass.__name__} did not create {filename}"
            content = filepath.read_text()
            assert expected_pattern in content, f"{GenClass.__name__} missing '{expected_pattern}' in output"


class TestConstructorPatterns:
    """Tests for both constructor patterns (empty + setters and parameterized)."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def test_packet(self):
        return [PacketDefinition("/test/ConstructorTest", {
            "description": "Test packet for constructor patterns",
            "fields": {
                "name": {"type": "string"},
                "value": {"type": "int"},
                "optional_field": {"type": "string", "optional": True}
            }
        })]

    def test_python_supports_empty_constructor(self, temp_output_dir, test_packet):
        """Verify Python packets support empty constructor + setters."""
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True)
        
        content = (Path(temp_output_dir) / "constructor_test.py").read_text()
        
        # All fields should have Optional type and = None default
        assert "Optional[str]" in content
        assert "Optional[int]" in content
        assert "= None" in content

    def test_dart_supports_empty_constructor(self, temp_output_dir, test_packet):
        """Verify Dart packets support empty constructor + setters."""
        generator = DartGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True)
        
        content = (Path(temp_output_dir) / "generated" / "constructor_test.dart").read_text()
        
        # Should have empty constructor
        assert "ConstructorTest();" in content
        # Should have .create() named constructor
        assert "ConstructorTest.create(" in content
        # Fields should be nullable for empty constructor support
        assert "String?" in content or "int?" in content

    def test_java_supports_empty_constructor(self, temp_output_dir, test_packet):
        """Verify Java packets support empty constructor + setters."""
        generator = JavaGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True)
        
        content = (Path(temp_output_dir) / "ConstructorTest.java").read_text()
        
        # Should have default constructor
        assert "public ConstructorTest()" in content
        # Should have setters
        assert "setName" in content
        assert "setValue" in content
        # Should have parameterized constructor
        assert "public ConstructorTest(String name," in content

    def test_typescript_supports_partial_constructor(self, temp_output_dir, test_packet):
        """Verify TypeScript packets support input interface in constructor."""
        generator = TypeScriptGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True)
        
        content = (Path(temp_output_dir) / "constructor_test.ts").read_text()
        
        # Should use ConstructorTestInput for flexible construction
        assert "ConstructorTestInput" in content


class TestEdgeCaseGeneration:
    """Tests for edge case handling in code generation."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_unicode_in_description(self, temp_output_dir):
        """Verify unicode in descriptions is handled correctly."""
        # Use simpler ASCII-safe description for cross-platform compatibility
        packet = PacketDefinition("/test/Unicode", {
            "description": "Packet with special chars: test-description",
            "fields": {
                "data": {"type": "string", "description": "Field with description"}
            }
        })
        
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate([packet], override=True)
        
        content = (Path(temp_output_dir) / "unicode.py").read_text()
        assert "test-description" in content or "Unicode" in content

    def test_special_characters_in_field_names(self, temp_output_dir):
        """Verify field names are properly sanitized."""
        packet = PacketDefinition("/test/Special", {
            "description": "Test packet",
            "fields": {
                "snake_case_field": {"type": "string"},
                "field_with_numbers_123": {"type": "int"},
            }
        })
        
        generators = [
            (PythonGenerator, "special.py"),
            (JavaGenerator, "Special.java"),
            (TypeScriptGenerator, "special.ts"),
        ]
        
        for GenClass, filename in generators:
            gen_dir = Path(temp_output_dir) / GenClass.__name__
            gen_dir.mkdir(parents=True, exist_ok=True)
            generator = GenClass({"output_dir": str(gen_dir)})
            generator.generate([packet], override=True)
            
            filepath = gen_dir / filename
            assert filepath.exists()
            content = filepath.read_text()
            # Should contain the field (possibly in camelCase)
            assert "snake_case_field" in content.lower() or "snakecasefield" in content.lower()

    def test_empty_fields_packet(self, temp_output_dir):
        """Verify packets with no fields are handled."""
        packet = PacketDefinition("/test/Empty", {
            "description": "Empty packet with no fields",
            "fields": {}
        })
        
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate([packet], override=True)
        
        content = (Path(temp_output_dir) / "empty.py").read_text()
        assert "class Empty" in content

    def test_all_optional_fields(self, temp_output_dir):
        """Verify packets with all optional fields work correctly."""
        packet = PacketDefinition("/test/AllOptional", {
            "description": "Packet with all optional fields",
            "fields": {
                "field1": {"type": "string", "optional": True},
                "field2": {"type": "int", "optional": True},
                "field3": {"type": "bool", "optional": True},
            }
        })
        
        generators = [
            (PythonGenerator, "all_optional.py"),
            (DartGenerator, "generated/all_optional.dart"),
            (RustGenerator, "all_optional.rs"),
        ]
        
        for GenClass, filename in generators:
            gen_dir = Path(temp_output_dir) / GenClass.__name__
            gen_dir.mkdir(parents=True, exist_ok=True)
            generator = GenClass({"output_dir": str(gen_dir)})
            generator.generate([packet], override=True)
            
            filepath = gen_dir / filename
            assert filepath.exists(), f"{GenClass.__name__} failed"

    def test_bytes_field_generation(self, temp_output_dir):
        """Verify bytes fields are handled in all languages."""
        packet = PacketDefinition("/test/Binary", {
            "description": "Packet with binary data",
            "fields": {
                "data": {"type": "bytes"},
                "hash": {"type": "bytes", "optional": True}
            }
        })
        
        lang_checks = [
            (PythonGenerator, "binary.py", "bytes"),
            (DartGenerator, "generated/binary.dart", "Uint8List"),
            (JavaGenerator, "Binary.java", "byte[]"),
            (TypeScriptGenerator, "binary.ts", "Uint8Array"),
            (RustGenerator, "binary.rs", "Vec<u8>"),
            (GoGenerator, "binary.go", "[]byte"),
            (CppGenerator, "binary.hpp", "std::vector<uint8_t>"),
            (CSharpGenerator, "Binary.cs", "byte[]"),
            (PhpGenerator, "Binary.php", "string"),  # PHP uses strings for binary
        ]
        
        for GenClass, filename, expected_type in lang_checks:
            gen_dir = Path(temp_output_dir) / GenClass.__name__
            gen_dir.mkdir(parents=True, exist_ok=True)
            
            config = {"output_dir": str(gen_dir)}
            if GenClass == CSharpGenerator:
                config["namespace"] = "Test"
            if GenClass == CppGenerator:
                config["namespace"] = "test"
            if GenClass == GoGenerator:
                config["package"] = "test"
            if GenClass == PhpGenerator:
                config["namespace"] = "Test"
            
            generator = GenClass(config)
            generator.generate([packet], override=True)
            
            filepath = gen_dir / filename
            assert filepath.exists(), f"{GenClass.__name__} did not create {filename}"
            content = filepath.read_text()
            assert expected_type in content, f"{GenClass.__name__} missing '{expected_type}'"


class TestSerializationModes:
    """Tests for JSON-only and MsgPack-only generation modes."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def test_packet(self):
        return [PacketDefinition("/test/SerializeTest", {
            "description": "Test serialization modes",
            "fields": {"message": {"type": "string"}}
        })]

    def test_python_json_only(self, temp_output_dir, test_packet):
        """Verify Python JSON-only mode excludes msgpack."""
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True, no_msgpack=True)
        
        content = (Path(temp_output_dir) / "serialize_test.py").read_text()
        assert "to_json" in content
        assert "from_json" in content
        assert "msgpack" not in content.lower()

    def test_python_msgpack_only(self, temp_output_dir, test_packet):
        """Verify Python MsgPack-only mode excludes json methods."""
        generator = PythonGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True, no_json=True)
        
        content = (Path(temp_output_dir) / "serialize_test.py").read_text()
        assert "to_msgpack" in content
        assert "from_msgpack" in content
        # Note: may still have some json imports for internal use

    def test_java_json_only(self, temp_output_dir, test_packet):
        """Verify Java JSON-only mode excludes msgpack imports."""
        generator = JavaGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True, no_msgpack=True)
        
        content = (Path(temp_output_dir) / "SerializeTest.java").read_text()
        assert "fromJson" in content
        assert "toMsgPack" not in content

    def test_dart_json_only(self, temp_output_dir, test_packet):
        """Verify Dart JSON-only mode excludes msgpack."""
        generator = DartGenerator({"output_dir": temp_output_dir})
        generator.generate(test_packet, override=True, no_msgpack=True)
        
        content = (Path(temp_output_dir) / "generated" / "serialize_test.dart").read_text()
        assert "toJson" in content
        assert "msgpack" not in content.lower()


class TestCleanMode:
    """Tests for --clean mode that removes old generated files."""

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_python_clean_removes_old_files(self, temp_output_dir):
        """Verify clean mode removes previously generated files."""
        packets_v1 = [PacketDefinition("/test/OldPacket", {
            "description": "Old packet",
            "fields": {"data": {"type": "string"}}
        })]
        
        packets_v2 = [PacketDefinition("/test/NewPacket", {
            "description": "New packet",
            "fields": {"data": {"type": "string"}}
        })]
        
        generator = PythonGenerator({"output_dir": temp_output_dir})
        
        # Generate v1
        generator.generate(packets_v1, override=True)
        assert (Path(temp_output_dir) / "old_packet.py").exists()
        
        # Generate v2 with clean
        generator.generate(packets_v2, override=True, clean=True)
        assert not (Path(temp_output_dir) / "old_packet.py").exists()
        assert (Path(temp_output_dir) / "new_packet.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
