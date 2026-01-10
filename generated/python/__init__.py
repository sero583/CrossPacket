"""
Auto-generated packet module.
"""

from .message_packet import MessagePacket
from .ping_packet import PingPacket
from .pong_packet import PongPacket
from .data_chunk_packet import DataChunkPacket
from .comprehensive_packet import ComprehensivePacket
from .user_profile_packet import UserProfilePacket
from .secure_message_packet import SecureMessagePacket


def deserialize_packet(data):
    """Deserialize a packet based on its packetType field."""
    packet_type = data.get("packetType") if isinstance(data, dict) else None

    if packet_type == "/chat/MessagePacket":
        return MessagePacket._from_dict(data)
    if packet_type == "/example/PingPacket":
        return PingPacket._from_dict(data)
    if packet_type == "/example/PongPacket":
        return PongPacket._from_dict(data)
    if packet_type == "/example/DataChunkPacket":
        return DataChunkPacket._from_dict(data)
    if packet_type == "/test/ComprehensivePacket":
        return ComprehensivePacket._from_dict(data)
    if packet_type == "/example/UserProfilePacket":
        return UserProfilePacket._from_dict(data)
    if packet_type == "/example/SecureMessagePacket":
        return SecureMessagePacket._from_dict(data)

    raise ValueError(f"Unknown packet type: {packet_type}")