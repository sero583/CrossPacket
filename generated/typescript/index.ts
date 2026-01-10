// Auto-generated - do not modify manually

import { MessagePacket } from './message_packet';
import { PingPacket } from './ping_packet';
import { PongPacket } from './pong_packet';
import { DataChunkPacket } from './data_chunk_packet';
import { ComprehensivePacket } from './comprehensive_packet';
import { UserProfilePacket } from './user_profile_packet';
import { SecureMessagePacket } from './secure_message_packet';

export { MessagePacket } from './message_packet';
export { PingPacket } from './ping_packet';
export { PongPacket } from './pong_packet';
export { DataChunkPacket } from './data_chunk_packet';
export { ComprehensivePacket } from './comprehensive_packet';
export { UserProfilePacket } from './user_profile_packet';
export { SecureMessagePacket } from './secure_message_packet';

// Packet type map for deserialization
const packetTypes: Record<string, any> = {
  '/chat/MessagePacket': MessagePacket,
  '/example/PingPacket': PingPacket,
  '/example/PongPacket': PongPacket,
  '/example/DataChunkPacket': DataChunkPacket,
  '/test/ComprehensivePacket': ComprehensivePacket,
  '/example/UserProfilePacket': UserProfilePacket,
  '/example/SecureMessagePacket': SecureMessagePacket,
};

/**
 * Deserialize a packet from parsed JSON data.
 * @param data - The parsed JSON object with a packetType field
 * @returns The deserialized packet instance
 */
export function deserializePacket(data: any): any {
  const PacketClass = packetTypes[data.packetType];
  if (!PacketClass) throw new Error(`Unknown packet type: ${data.packetType}`);
  return PacketClass._fromData(data);
}