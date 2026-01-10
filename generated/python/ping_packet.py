"""
Auto-generated packet: PingPacket
Simple ping packet for connection testing
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
class PingPacket:
    """Simple ping packet for connection testing"""

    TYPE: ClassVar[str] = "/example/PingPacket"

    timestamp: Optional[datetime] = None
    message: Optional[str] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "message": self.message,
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
    def _from_dict(cls, data: Dict[str, Any]) -> PingPacket:
        """Create instance from dictionary (internal)."""
        return cls(
            timestamp=datetime.fromisoformat(data.get('timestamp')) if data.get('timestamp') else None,
            message=data.get('message'),
        )

    @classmethod
    def from_json(cls, json_str: str) -> PingPacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> PingPacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))