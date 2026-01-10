"""
Auto-generated packet: DataChunkPacket
Chunked data packet for progressive loading of large datasets
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False

@dataclass
class DataChunkPacket:
    """Chunked data packet for progressive loading of large datasets"""

    TYPE: ClassVar[str] = "/example/DataChunkPacket"

    chunk_index: Optional[int] = None
    total_chunks: Optional[int] = None
    data: Optional[Dict[Any, Any]] = None
    checksum: Optional[str] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "data": self.data,
            "checksum": self.checksum,
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
    def _from_dict(cls, data: Dict[str, Any]) -> DataChunkPacket:
        """Create instance from dictionary (internal)."""
        return cls(
            chunk_index=int(data.get('chunk_index')) if data.get('chunk_index') is not None else None,
            total_chunks=int(data.get('total_chunks')) if data.get('total_chunks') is not None else None,
            data=data.get('data'),
            checksum=data.get('checksum'),
        )

    @classmethod
    def from_json(cls, json_str: str) -> DataChunkPacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> DataChunkPacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))