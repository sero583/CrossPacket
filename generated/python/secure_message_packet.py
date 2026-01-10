"""
Auto-generated packet: SecureMessagePacket
Security-hardened message packet with strict validation
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
class SecureMessagePacket:
    """Security-hardened message packet with strict validation"""

    TYPE: ClassVar[str] = "/example/SecureMessagePacket"

    message_id: Optional[str] = None
    sender_id: Optional[int] = None
    recipient_id: Optional[int] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[Any]] = None
    encrypted_payload: Optional[bytes] = None
    priority: Optional[int] = None
    is_read: Optional[bool] = None
    sent_at: Optional[datetime] = None

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (internal)."""
        return {
            "packetType": self.TYPE,
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "subject": self.subject,
            "body": self.body,
            "attachments": self.attachments,
            "encrypted_payload": self.encrypted_payload,
            "priority": self.priority,
            "is_read": self.is_read,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
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
    def _from_dict(cls, data: Dict[str, Any]) -> SecureMessagePacket:
        """Create instance from dictionary (internal)."""
        return cls(
            message_id=data.get('message_id'),
            sender_id=int(data.get('sender_id')) if data.get('sender_id') is not None else None,
            recipient_id=int(data.get('recipient_id')) if data.get('recipient_id') is not None else None,
            subject=data.get('subject'),
            body=data.get('body'),
            attachments=data.get('attachments'),
            encrypted_payload=data.get('encrypted_payload'),
            priority=int(data.get('priority')) if data.get('priority') is not None else None,
            is_read=bool(data.get('is_read')) if data.get('is_read') is not None else None,
            sent_at=datetime.fromisoformat(data.get('sent_at')) if data.get('sent_at') else None,
        )

    @classmethod
    def from_json(cls, json_str: str) -> SecureMessagePacket:
        """Deserialize from JSON string."""
        return cls._from_dict(json.loads(json_str))

    @classmethod
    def from_msgpack(cls, data: bytes) -> SecureMessagePacket:
        """Deserialize from MessagePack binary format."""
        if not HAS_MSGPACK:
            raise ImportError("msgpack is required for binary deserialization")
        return cls._from_dict(msgpack.unpackb(data, raw=False))