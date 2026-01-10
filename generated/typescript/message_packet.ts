// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface MessagePacketData {
  packetType: string;
  senderId: string;
  content: string;
  timestamp: string;
}

export interface MessagePacketInput {
  senderId: string;
  content: string;
  timestamp: Date | string;
}

export class MessagePacket {
  static readonly TYPE = "/chat/MessagePacket";

  senderId: string;
  content: string;
  timestamp: Date;

  constructor(data: MessagePacketInput) {
    this.senderId = data.senderId;
    this.content = data.content;
    this.timestamp = data.timestamp instanceof Date ? data.timestamp : new Date(data.timestamp);
  }

  private _toData(): MessagePacketData {
    return {
      packetType: MessagePacket.TYPE,
      senderId: this.senderId,
      content: this.content,
      timestamp: this.timestamp.toISOString(),
    };
  }

  private static _fromData(data: MessagePacketData): MessagePacket {
    return new MessagePacket({
      senderId: data.senderId,
      content: data.content,
      timestamp: new Date(data.timestamp),
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): MessagePacket {
    return MessagePacket._fromData(JSON.parse(json) as MessagePacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): MessagePacket {
    const data = msgpack.decode(bytes) as MessagePacketData;
    return MessagePacket._fromData(data);
  }
}