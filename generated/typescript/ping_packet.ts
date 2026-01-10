// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface PingPacketData {
  packetType: string;
  timestamp: string;
  message: string;
}

export interface PingPacketInput {
  timestamp: Date | string;
  message: string;
}

export class PingPacket {
  static readonly TYPE = "/example/PingPacket";

  timestamp: Date;
  message: string;

  constructor(data: PingPacketInput) {
    this.timestamp = data.timestamp instanceof Date ? data.timestamp : new Date(data.timestamp);
    this.message = data.message;
  }

  private _toData(): PingPacketData {
    return {
      packetType: PingPacket.TYPE,
      timestamp: this.timestamp.toISOString(),
      message: this.message,
    };
  }

  private static _fromData(data: PingPacketData): PingPacket {
    return new PingPacket({
      timestamp: new Date(data.timestamp),
      message: data.message,
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): PingPacket {
    return PingPacket._fromData(JSON.parse(json) as PingPacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): PingPacket {
    const data = msgpack.decode(bytes) as PingPacketData;
    return PingPacket._fromData(data);
  }
}