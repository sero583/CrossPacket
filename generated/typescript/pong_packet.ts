// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface PongPacketData {
  packetType: string;
  originalTimestamp: string;
  responseTimestamp: string;
  latencyMs: number;
}

export interface PongPacketInput {
  originalTimestamp: Date | string;
  responseTimestamp: Date | string;
  latencyMs: number;
}

export class PongPacket {
  static readonly TYPE = "/example/PongPacket";

  originalTimestamp: Date;
  responseTimestamp: Date;
  latencyMs: number;

  constructor(data: PongPacketInput) {
    this.originalTimestamp = data.originalTimestamp instanceof Date ? data.originalTimestamp : new Date(data.originalTimestamp);
    this.responseTimestamp = data.responseTimestamp instanceof Date ? data.responseTimestamp : new Date(data.responseTimestamp);
    this.latencyMs = data.latencyMs;
  }

  private _toData(): PongPacketData {
    return {
      packetType: PongPacket.TYPE,
      originalTimestamp: this.originalTimestamp.toISOString(),
      responseTimestamp: this.responseTimestamp.toISOString(),
      latencyMs: this.latencyMs,
    };
  }

  private static _fromData(data: PongPacketData): PongPacket {
    return new PongPacket({
      originalTimestamp: new Date(data.originalTimestamp),
      responseTimestamp: new Date(data.responseTimestamp),
      latencyMs: data.latencyMs,
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): PongPacket {
    return PongPacket._fromData(JSON.parse(json) as PongPacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): PongPacket {
    const data = msgpack.decode(bytes) as PongPacketData;
    return PongPacket._fromData(data);
  }
}