"""
Auto-generated packet: ComprehensivePacket
Test packet containing ALL supported types for comprehensive testing
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional
from datetime import datetime, timezone
from datetime import time

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False

@dataclass
class ComprehensivePacket:
    """Test packet containing ALL supported types for comprehensive testing"""

    TYPE: ClassVar[str] = "/test/ComprehensivePacket"

    int_field: Optional[int] = None
    float_field: Optional[float] = None
    double_field: Optional[float] = None
    string_field: Optional[str] = None
    bool_field: Optional[bool] = None
    datetime_field: Optional[datetime] = None
    time_field: Optional[time] = None
    list_field: Optional[List[Any]] = None
    list_int_field: Optional[List[int]] = None
    list_string_field: Optional[List[str]] = None
    map_field: Optional[Dict[str, Any]] = None
    embedded_map_field: Optional[Dict[Any, Any]] = None
    map_string_dynamic_field: Optional[Dict[str, Any]] = None
    bytes_field: Optional[bytes] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "int_field": self.int_field,
            "float_field": self.float_field,
            "double_field": self.double_field,
            "string_field": self.string_field,
            "bool_field": self.bool_field,
            "datetime_field": self.datetime_field.isoformat() if self.datetime_field else None,
            "time_field": self.time_field.isoformat() if self.time_field else None,
            "list_field": self.list_field,
            "list_int_field": self.list_int_field,
            "list_string_field": self.list_string_field,
            "map_field": self.map_field,
            "embedded_map_field": self.embedded_map_field,
            "map_string_dynamic_field": self.map_string_dynamic_field,
            "bytes_field": self.bytes_field,
        }

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self._to_dict(), default=str)

    def to_msgpack(self) -> bytes:
        """Serialize to MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary serialization")
        return msgpack.packb(self._to_dict(), use_bin_type=True)

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> ComprehensivePacket:
        """Create instance from dictionary (internal)."""
        return cls(
            int_field=int(data.get('int_field')) if data.get('int_field') is not None else None,
            float_field=float(data.get('float_field')) if data.get('float_field') is not None else None,
            double_field=float(data.get('double_field')) if data.get('double_field') is not None else None,
            string_field=data.get('string_field'),
            bool_field=bool(data.get('bool_field')) if data.get('bool_field') is not None else None,
            datetime_field=datetime.fromisoformat(data.get('datetime_field')) if data.get('datetime_field') else None,
            time_field=time.fromisoformat(data.get('time_field')) if data.get('time_field') else None,
            list_field=data.get('list_field'),
            list_int_field=[int(x) for x in data.get('list_int_field')] if data.get('list_int_field') else None,
            list_string_field=[str(x) for x in data.get('list_string_field')] if data.get('list_string_field') else None,
            map_field=data.get('map_field'),
            embedded_map_field=data.get('embedded_map_field'),
            map_string_dynamic_field=data.get('map_string_dynamic_field'),
            bytes_field=data.get('bytes_field'),
        )

    @classmethod
    def from_json(cls, json_str: str) -> ComprehensivePacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> ComprehensivePacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))