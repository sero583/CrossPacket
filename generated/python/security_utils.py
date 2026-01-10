"""
CrossPacket Security Utilities

Provides validation functions for securing packet data:
- ValidationError: Exception for validation failures
- SecurityLimits: Configurable limits for validation
- validate_int: Integer bounds checking
- validate_float: Float validation (NaN/Infinity handling)
- validate_string: String length limits
- validate_list: List size limits
- validate_map: Map size limits
- validate_required_fields: Required field checking
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar
import math


class ValidationError(Exception):
    """Exception raised when validation fails."""

    def __init__(self, field: str, message: str, value: Any = None):
        """
        Initialize a validation error.
        
        Args:
            field: Name of the field that failed validation
            message: Human-readable error message
            value: The invalid value (optional)
        """
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"{field}: {message}")

    def __repr__(self) -> str:
        return f"ValidationError(field={self.field!r}, message={self.message!r})"


@dataclass
class SecurityLimits:
    """
    Configurable limits for packet validation.
    
    Attributes:
        max_int: Maximum allowed integer value (default: 2^63-1)
        min_int: Minimum allowed integer value (default: -2^63)
        max_list_size: Maximum number of items in a list (default: 100000)
        max_map_size: Maximum number of keys in a map (default: 100000)
        max_string_length: Maximum string length in characters (default: 10MB)
        max_bytes_length: Maximum bytes length (default: 100MB)
        allow_nan: Whether to allow NaN float values (default: True)
        allow_infinity: Whether to allow Infinity float values (default: True)
    """

    max_int: int = 9223372036854775807  # 2^63 - 1
    min_int: int = -9223372036854775808  # -2^63
    max_list_size: int = 100000
    max_map_size: int = 100000
    max_string_length: int = 10000000  # 10MB
    max_bytes_length: int = 100000000  # 100MB
    allow_nan: bool = True
    allow_infinity: bool = True


# Default global limits
DEFAULT_LIMITS = SecurityLimits()


def validate_int(
    value: Any,
    field_name: str,
    limits: Optional[SecurityLimits] = None,
    *,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    allow_none: bool = False,
) -> Optional[int]:
    """
    Validate an integer value with bounds checking.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        limits: Security limits to apply (default: global limits)
        min_val: Minimum allowed value (overrides limits.min_int)
        max_val: Maximum allowed value (overrides limits.max_int)
        allow_none: Whether None values are allowed
    
    Returns:
        The validated integer value, or None if allow_none=True and value is None
    
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        if allow_none:
            return None
        raise ValidationError(field_name, "Value is required", value)

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationError(field_name, f"Expected int, got {type(value).__name__}", value)

    int_value = int(value)
    limits = limits or DEFAULT_LIMITS

    effective_min = min_val if min_val is not None else limits.min_int
    effective_max = max_val if max_val is not None else limits.max_int

    if int_value < effective_min:
        raise ValidationError(field_name, f"Value {int_value} is less than minimum {effective_min}", value)

    if int_value > effective_max:
        raise ValidationError(field_name, f"Value {int_value} exceeds maximum {effective_max}", value)

    return int_value


def validate_float(
    value: Any,
    field_name: str,
    limits: Optional[SecurityLimits] = None,
    *,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    allow_none: bool = False,
    allow_nan: Optional[bool] = None,
    allow_infinity: Optional[bool] = None,
) -> Optional[float]:
    """
    Validate a float value with NaN/Infinity handling.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        limits: Security limits to apply (default: global limits)
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        allow_none: Whether None values are allowed
        allow_nan: Whether NaN is allowed (overrides limits)
        allow_infinity: Whether Infinity is allowed (overrides limits)
    
    Returns:
        The validated float value
    
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        if allow_none:
            return None
        raise ValidationError(field_name, "Value is required", value)

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationError(field_name, f"Expected float, got {type(value).__name__}", value)

    float_value = float(value)
    limits = limits or DEFAULT_LIMITS

    effective_allow_nan = allow_nan if allow_nan is not None else limits.allow_nan
    effective_allow_infinity = allow_infinity if allow_infinity is not None else limits.allow_infinity

    if math.isnan(float_value) and not effective_allow_nan:
        raise ValidationError(field_name, "NaN values are not allowed", value)

    if math.isinf(float_value) and not effective_allow_infinity:
        raise ValidationError(field_name, "Infinity values are not allowed", value)

    if min_val is not None and float_value < min_val:
        raise ValidationError(field_name, f"Value {float_value} is less than minimum {min_val}", value)

    if max_val is not None and float_value > max_val:
        raise ValidationError(field_name, f"Value {float_value} exceeds maximum {max_val}", value)

    return float_value


def validate_string(
    value: Any,
    field_name: str,
    limits: Optional[SecurityLimits] = None,
    *,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_none: bool = False,
    allow_empty: bool = True,
    pattern: Optional[str] = None,
) -> Optional[str]:
    """
    Validate a string value with length limits.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        limits: Security limits to apply (default: global limits)
        min_length: Minimum string length
        max_length: Maximum string length (overrides limits.max_string_length)
        allow_none: Whether None values are allowed
        allow_empty: Whether empty strings are allowed
        pattern: Regex pattern to match (optional)
    
    Returns:
        The validated string value
    
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        if allow_none:
            return None
        raise ValidationError(field_name, "Value is required", value)

    if not isinstance(value, str):
        raise ValidationError(field_name, f"Expected string, got {type(value).__name__}", value)

    limits = limits or DEFAULT_LIMITS
    effective_max = max_length if max_length is not None else limits.max_string_length

    if not allow_empty and len(value) == 0:
        raise ValidationError(field_name, "Empty string not allowed", value)

    if min_length is not None and len(value) < min_length:
        raise ValidationError(field_name, f"String length {len(value)} is less than minimum {min_length}", value)

    if len(value) > effective_max:
        raise ValidationError(field_name, f"String length {len(value)} exceeds maximum {effective_max}", value)

    if pattern is not None:
        import re
        if not re.match(pattern, value):
            raise ValidationError(field_name, f"String does not match pattern: {pattern}", value)

    return value


T = TypeVar("T")


def validate_list(
    value: Any,
    field_name: str,
    limits: Optional[SecurityLimits] = None,
    *,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    allow_none: bool = False,
    item_validator: Optional[Callable[[Any, str], T]] = None,
) -> Optional[List[Any]]:
    """
    Validate a list with size limits.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        limits: Security limits to apply (default: global limits)
        min_size: Minimum number of items
        max_size: Maximum number of items (overrides limits.max_list_size)
        allow_none: Whether None values are allowed
        item_validator: Optional validator function for each item
    
    Returns:
        The validated list
    
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        if allow_none:
            return None
        raise ValidationError(field_name, "Value is required", value)

    if not isinstance(value, list):
        raise ValidationError(field_name, f"Expected list, got {type(value).__name__}", value)

    limits = limits or DEFAULT_LIMITS
    effective_max = max_size if max_size is not None else limits.max_list_size

    if min_size is not None and len(value) < min_size:
        raise ValidationError(field_name, f"List size {len(value)} is less than minimum {min_size}", value)

    if len(value) > effective_max:
        raise ValidationError(field_name, f"List size {len(value)} exceeds maximum {effective_max}", value)

    if item_validator:
        validated = []
        for i, item in enumerate(value):
            validated.append(item_validator(item, f"{field_name}[{i}]"))
        return validated

    return list(value)


def validate_map(
    value: Any,
    field_name: str,
    limits: Optional[SecurityLimits] = None,
    *,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    allow_none: bool = False,
    key_validator: Optional[Callable[[Any, str], Any]] = None,
    value_validator: Optional[Callable[[Any, str], Any]] = None,
) -> Optional[Dict[Any, Any]]:
    """
    Validate a map/dict with size limits.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        limits: Security limits to apply (default: global limits)
        min_size: Minimum number of keys
        max_size: Maximum number of keys (overrides limits.max_map_size)
        allow_none: Whether None values are allowed
        key_validator: Optional validator function for keys
        value_validator: Optional validator function for values
    
    Returns:
        The validated map
    
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        if allow_none:
            return None
        raise ValidationError(field_name, "Value is required", value)

    if not isinstance(value, dict):
        raise ValidationError(field_name, f"Expected dict, got {type(value).__name__}", value)

    limits = limits or DEFAULT_LIMITS
    effective_max = max_size if max_size is not None else limits.max_map_size

    if min_size is not None and len(value) < min_size:
        raise ValidationError(field_name, f"Map size {len(value)} is less than minimum {min_size}", value)

    if len(value) > effective_max:
        raise ValidationError(field_name, f"Map size {len(value)} exceeds maximum {effective_max}", value)

    if key_validator or value_validator:
        validated = {}
        for k, v in value.items():
            validated_key = key_validator(k, f"{field_name}.key") if key_validator else k
            validated_value = value_validator(v, f"{field_name}[{k!r}]") if value_validator else v
            validated[validated_key] = validated_value
        return validated

    return dict(value)


def validate_required_fields(
    data: Dict[str, Any],
    required_fields: List[str],
    packet_name: str,
) -> None:
    """
    Validate that all required fields are present in data.
    
    Args:
        data: The data dictionary to check
        required_fields: List of field names that must be present
        packet_name: Name of the packet (for error messages)
    
    Raises:
        ValidationError: If any required fields are missing
    """
    if not isinstance(data, dict):
        raise ValidationError("data", f"Expected dict for {packet_name}, got {type(data).__name__}", data)

    missing = [f for f in required_fields if f not in data]
    if missing:
        missing_str = ", ".join(missing)
        raise ValidationError(
            "required_fields",
            f"Missing required fields in {packet_name}: {missing_str}",
            missing,
        )
