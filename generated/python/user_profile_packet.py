"""
Auto-generated packet: UserProfilePacket
Example packet demonstrating field-level validation overrides
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
class UserProfilePacket:
    """Example packet demonstrating field-level validation overrides"""

    TYPE: ClassVar[str] = "/example/UserProfilePacket"

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    age: Optional[int] = None
    balance: Optional[float] = None
    tags: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    avatar: Optional[bytes] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "age": self.age,
            "balance": self.balance,
            "tags": self.tags,
            "preferences": self.preferences,
            "avatar": self.avatar,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
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
    def _from_dict(cls, data: Dict[str, Any]) -> UserProfilePacket:
        """Create instance from dictionary (internal)."""
        return cls(
            user_id=int(data.get('user_id')) if data.get('user_id') is not None else None,
            username=data.get('username'),
            email=data.get('email'),
            bio=data.get('bio'),
            age=int(data.get('age')) if data.get('age') is not None else None,
            balance=float(data.get('balance')) if data.get('balance') is not None else None,
            tags=[str(x) for x in data.get('tags')] if data.get('tags') else None,
            preferences=data.get('preferences'),
            avatar=data.get('avatar'),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else None,
            last_login=datetime.fromisoformat(data.get('last_login')) if data.get('last_login') else None,
        )

    @classmethod
    def from_json(cls, json_str: str) -> UserProfilePacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> UserProfilePacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))