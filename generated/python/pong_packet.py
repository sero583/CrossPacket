"""
Auto-generated packet: PongPacket
Response to a ping packet
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional
from datetime import datetime, timezone

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False

@dataclass
class PongPacket:
    """Response to a ping packet"""

    TYPE: ClassVar[str] = "/example/PongPacket"

    original_timestamp: Optional[datetime] = None
    response_timestamp: Optional[datetime] = None
    latency_ms: Optional[int] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "original_timestamp": self.original_timestamp.isoformat() if self.original_timestamp else None,
            "response_timestamp": self.response_timestamp.isoformat() if self.response_timestamp else None,
            "latency_ms": self.latency_ms,
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
    def _from_dict(cls, data: Dict[str, Any]) -> PongPacket:
        """Create instance from dictionary (internal)."""
        return cls(
            original_timestamp=datetime.fromisoformat(data.get('original_timestamp')) if data.get('original_timestamp') else None,
            response_timestamp=datetime.fromisoformat(data.get('response_timestamp')) if data.get('response_timestamp') else None,
            latency_ms=int(data.get('latency_ms')) if data.get('latency_ms') is not None else None,
        )

    @classmethod
    def from_json(cls, json_str: str) -> PongPacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> PongPacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))