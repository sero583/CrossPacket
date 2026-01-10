#!/usr/bin/env python3
"""
Test the security utilities module.

Author: Serhat Güler (sero583)
GitHub: https://github.com/sero583
License: MIT
"""
import os
import sys
import math
import pytest

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Add generated/python to path (relative to script location or CWD)
# Uses the committed generated folder for consistent CI testing
GENERATED_DIR = os.path.join(SCRIPT_DIR, "..", "..", "generated", "python")
if os.path.exists(GENERATED_DIR):
    sys.path.insert(0, GENERATED_DIR)
# JUSTIFICATION: This fallback branch only executes if the generated/python directory
# doesn't exist locally. In CI, the generated folder is always present in the repo.
else:  # pragma: no cover
    sys.path.insert(0, "generated/python")
    sys.path.insert(0, "../../generated/python")

from security_utils import (
    ValidationError,
    SecurityLimits,
    validate_int,
    validate_float,
    validate_string,
    validate_list,
    validate_map,
    validate_required_fields,
)


class TestValidationError:
    """Test ValidationError exception class."""

    def test_error_message(self):
        """Test error message formatting."""
        err = ValidationError("test_field", "test message")
        assert str(err) == "test_field: test message"
        assert err.field == "test_field"
        assert err.message == "test message"

    def test_error_with_value(self):
        """Test error with value."""
        err = ValidationError("field", "message", value=42)
        assert err.value == 42

    def test_error_repr(self):
        """Test error repr."""
        err = ValidationError("f", "m")
        assert "ValidationError" in repr(err)
        assert "f" in repr(err)
        assert "m" in repr(err)


class TestSecurityLimits:
    """Test SecurityLimits dataclass."""

    def test_default_limits(self):
        """Test default limit values."""
        limits = SecurityLimits()
        assert limits.max_int == 9223372036854775807
        assert limits.min_int == -9223372036854775808
        assert limits.max_list_size == 100000
        assert limits.max_map_size == 100000
        assert limits.max_string_length == 10000000
        assert limits.max_bytes_length == 100000000
        assert limits.allow_nan is True
        assert limits.allow_infinity is True

    def test_custom_limits(self):
        """Test custom limits."""
        limits = SecurityLimits(max_int=100, min_int=-50, max_list_size=10)
        assert limits.max_int == 100
        assert limits.min_int == -50
        assert limits.max_list_size == 10


class TestValidateInt:
    """Test validate_int function."""

    def test_normal_int(self):
        """Test normal integer validation."""
        assert validate_int(42, "field") == 42

    def test_negative_int(self):
        """Test negative integer."""
        assert validate_int(-100, "field") == -100

    def test_zero(self):
        """Test zero value."""
        assert validate_int(0, "field") == 0

    def test_float_to_int(self):
        """Test float coerced to int."""
        assert validate_int(42.5, "field") == 42

    def test_none_required(self):
        """Test None when required raises error."""
        with pytest.raises(ValidationError) as exc:
            validate_int(None, "field")
        assert "required" in exc.value.message

    def test_none_allowed(self):
        """Test None when allowed."""
        assert validate_int(None, "field", allow_none=True) is None

    def test_wrong_type(self):
        """Test wrong type raises error."""
        with pytest.raises(ValidationError) as exc:
            validate_int("not an int", "field")
        assert "Expected int" in exc.value.message

    def test_boolean_rejected(self):
        """Test boolean is rejected."""
        with pytest.raises(ValidationError):
            validate_int(True, "field")

    def test_overflow_max(self):
        """Test integer overflow max."""
        with pytest.raises(ValidationError) as exc:
            validate_int(2**64, "field")
        assert "exceeds maximum" in exc.value.message

    def test_underflow_min(self):
        """Test integer underflow min."""
        with pytest.raises(ValidationError) as exc:
            validate_int(-2**64, "field")
        assert "less than minimum" in exc.value.message

    def test_custom_min_val(self):
        """Test custom min_val."""
        with pytest.raises(ValidationError):
            validate_int(5, "field", min_val=10)

    def test_custom_max_val(self):
        """Test custom max_val."""
        with pytest.raises(ValidationError):
            validate_int(15, "field", max_val=10)

    def test_custom_limits(self):
        """Test with custom limits object."""
        limits = SecurityLimits(max_int=50, min_int=-50)
        with pytest.raises(ValidationError):
            validate_int(100, "field", limits=limits)


class TestValidateFloat:
    """Test validate_float function."""

    def test_normal_float(self):
        """Test normal float validation."""
        assert validate_float(3.14, "field") == 3.14

    def test_int_to_float(self):
        """Test int coerced to float."""
        assert validate_float(42, "field") == 42.0

    def test_none_required(self):
        """Test None when required raises error."""
        with pytest.raises(ValidationError) as exc:
            validate_float(None, "field")
        assert "required" in exc.value.message

    def test_none_allowed(self):
        """Test None when allowed."""
        assert validate_float(None, "field", allow_none=True) is None

    def test_wrong_type(self):
        """Test wrong type raises error."""
        with pytest.raises(ValidationError):
            validate_float("not a float", "field")

    def test_boolean_rejected(self):
        """Test boolean is rejected."""
        with pytest.raises(ValidationError):
            validate_float(True, "field")

    def test_nan_allowed(self):
        """Test NaN allowed by default."""
        result = validate_float(float("nan"), "field")
        assert math.isnan(result)

    def test_nan_disallowed(self):
        """Test NaN disallowed."""
        with pytest.raises(ValidationError) as exc:
            validate_float(float("nan"), "field", allow_nan=False)
        assert "NaN" in exc.value.message

    def test_infinity_allowed(self):
        """Test infinity allowed by default."""
        assert validate_float(float("inf"), "field") == float("inf")

    def test_infinity_disallowed(self):
        """Test infinity disallowed."""
        with pytest.raises(ValidationError) as exc:
            validate_float(float("inf"), "field", allow_infinity=False)
        assert "Infinity" in exc.value.message

    def test_min_val(self):
        """Test min_val enforcement."""
        with pytest.raises(ValidationError):
            validate_float(5.0, "field", min_val=10.0)

    def test_max_val(self):
        """Test max_val enforcement."""
        with pytest.raises(ValidationError):
            validate_float(15.0, "field", max_val=10.0)

    def test_custom_limits(self):
        """Test with custom limits object."""
        limits = SecurityLimits(allow_nan=False)
        with pytest.raises(ValidationError):
            validate_float(float("nan"), "field", limits=limits)


class TestValidateString:
    """Test validate_string function."""

    def test_normal_string(self):
        """Test normal string validation."""
        assert validate_string("hello", "field") == "hello"

    def test_empty_string_allowed(self):
        """Test empty string allowed by default."""
        assert validate_string("", "field") == ""

    def test_empty_string_disallowed(self):
        """Test empty string disallowed."""
        with pytest.raises(ValidationError) as exc:
            validate_string("", "field", allow_empty=False)
        assert "Empty" in exc.value.message

    def test_none_required(self):
        """Test None when required raises error."""
        with pytest.raises(ValidationError):
            validate_string(None, "field")

    def test_none_allowed(self):
        """Test None when allowed."""
        assert validate_string(None, "field", allow_none=True) is None

    def test_wrong_type(self):
        """Test wrong type raises error."""
        with pytest.raises(ValidationError):
            validate_string(123, "field")

    def test_too_long(self):
        """Test string too long."""
        limits = SecurityLimits(max_string_length=10)
        with pytest.raises(ValidationError) as exc:
            validate_string("x" * 100, "field", limits=limits)
        assert "exceeds maximum" in exc.value.message

    def test_custom_max_length(self):
        """Test custom max_length overrides limits."""
        with pytest.raises(ValidationError):
            validate_string("x" * 20, "field", max_length=10)

    def test_min_length(self):
        """Test min_length enforcement."""
        with pytest.raises(ValidationError) as exc:
            validate_string("ab", "field", min_length=5)
        assert "less than minimum" in exc.value.message

    def test_pattern_match(self):
        """Test pattern matching."""
        assert validate_string("abc123", "field", pattern=r"^[a-z]+\d+$") == "abc123"

    def test_pattern_no_match(self):
        """Test pattern no match."""
        with pytest.raises(ValidationError) as exc:
            validate_string("invalid!", "field", pattern=r"^[a-z]+$")
        assert "pattern" in exc.value.message


class TestValidateList:
    """Test validate_list function."""

    def test_normal_list(self):
        """Test normal list validation."""
        assert validate_list([1, 2, 3], "field") == [1, 2, 3]

    def test_empty_list(self):
        """Test empty list."""
        assert validate_list([], "field") == []

    def test_none_required(self):
        """Test None when required raises error."""
        with pytest.raises(ValidationError):
            validate_list(None, "field")

    def test_none_allowed(self):
        """Test None when allowed."""
        assert validate_list(None, "field", allow_none=True) is None

    def test_wrong_type(self):
        """Test wrong type raises error."""
        with pytest.raises(ValidationError):
            validate_list("not a list", "field")

    def test_too_large(self):
        """Test list too large."""
        limits = SecurityLimits(max_list_size=5)
        with pytest.raises(ValidationError) as exc:
            validate_list(list(range(100)), "field", limits=limits)
        assert "exceeds maximum" in exc.value.message

    def test_custom_max_size(self):
        """Test custom max_size overrides limits."""
        with pytest.raises(ValidationError):
            validate_list(list(range(20)), "field", max_size=10)

    def test_min_size(self):
        """Test min_size enforcement."""
        with pytest.raises(ValidationError) as exc:
            validate_list([1], "field", min_size=5)
        assert "less than minimum" in exc.value.message

    def test_item_validator(self):
        """Test item validator applied to each item."""
        result = validate_list(
            [1, 2, 3], "field",
            item_validator=lambda x, f: validate_int(x, f)
        )
        assert result == [1, 2, 3]


class TestValidateMap:
    """Test validate_map function."""

    def test_normal_map(self):
        """Test normal map validation."""
        assert validate_map({"a": 1, "b": 2}, "field") == {"a": 1, "b": 2}

    def test_empty_map(self):
        """Test empty map."""
        assert validate_map({}, "field") == {}

    def test_none_required(self):
        """Test None when required raises error."""
        with pytest.raises(ValidationError):
            validate_map(None, "field")

    def test_none_allowed(self):
        """Test None when allowed."""
        assert validate_map(None, "field", allow_none=True) is None

    def test_wrong_type(self):
        """Test wrong type raises error."""
        with pytest.raises(ValidationError):
            validate_map("not a map", "field")

    def test_too_large(self):
        """Test map too large."""
        limits = SecurityLimits(max_map_size=5)
        with pytest.raises(ValidationError) as exc:
            validate_map({f"k{i}": i for i in range(100)}, "field", limits=limits)
        assert "exceeds maximum" in exc.value.message

    def test_custom_max_size(self):
        """Test custom max_size overrides limits."""
        with pytest.raises(ValidationError):
            validate_map({f"k{i}": i for i in range(20)}, "field", max_size=10)

    def test_min_size(self):
        """Test min_size enforcement."""
        with pytest.raises(ValidationError) as exc:
            validate_map({"a": 1}, "field", min_size=5)
        assert "less than minimum" in exc.value.message

    def test_key_validator(self):
        """Test key validator applied to each key."""
        result = validate_map(
            {"a": 1}, "field",
            key_validator=lambda k, f: validate_string(k, f)
        )
        assert result == {"a": 1}

    def test_value_validator(self):
        """Test value validator applied to each value."""
        result = validate_map(
            {"a": 1, "b": 2}, "field",
            value_validator=lambda v, f: validate_int(v, f)
        )
        assert result == {"a": 1, "b": 2}

    def test_both_validators(self):
        """Test both key and value validators."""
        result = validate_map(
            {"key": 42}, "field",
            key_validator=lambda k, f: validate_string(k, f),
            value_validator=lambda v, f: validate_int(v, f)
        )
        assert result == {"key": 42}


class TestValidateRequiredFields:
    """Test validate_required_fields function."""

    def test_all_present(self):
        """Test all required fields present."""
        data = {"name": "John", "age": 30, "email": "john@example.com"}
        validate_required_fields(data, ["name", "age"], "UserPacket")

    def test_missing_field(self):
        """Test missing required field raises error."""
        data = {"name": "John"}
        with pytest.raises(ValidationError) as exc:
            validate_required_fields(data, ["name", "age", "email"], "UserPacket")
        assert "Missing required fields" in exc.value.message
        assert "age" in exc.value.message
        assert "email" in exc.value.message

    def test_empty_required_list(self):
        """Test empty required list always passes."""
        validate_required_fields({"a": 1}, [], "Packet")

    def test_wrong_data_type(self):
        """Test wrong data type raises error."""
        with pytest.raises(ValidationError) as exc:
            validate_required_fields("not a dict", ["field"], "Packet")
        assert "Expected dict" in exc.value.message
