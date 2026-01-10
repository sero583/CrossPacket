// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface DataChunkPacketData {
  packetType: string;
  chunkIndex: number;
  totalChunks: number;
  data: Map<any, any>;
  checksum: string;
}

export interface DataChunkPacketInput {
  chunkIndex: number;
  totalChunks: number;
  data: Map<any, any>;
  checksum: string;
}

export class DataChunkPacket {
  static readonly TYPE = "/example/DataChunkPacket";

  chunkIndex: number;
  totalChunks: number;
  data: Map<any, any>;
  checksum: string;

  constructor(data: DataChunkPacketInput) {
    this.chunkIndex = data.chunkIndex;
    this.totalChunks = data.totalChunks;
    this.data = data.data;
    this.checksum = data.checksum;
  }

  private _toData(): DataChunkPacketData {
    return {
      packetType: DataChunkPacket.TYPE,
      chunkIndex: this.chunkIndex,
      totalChunks: this.totalChunks,
      data: this.data,
      checksum: this.checksum,
    };
  }

  private static _fromData(data: DataChunkPacketData): DataChunkPacket {
    return new DataChunkPacket({
      chunkIndex: data.chunkIndex,
      totalChunks: data.totalChunks,
      data: data.data,
      checksum: data.checksum,
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): DataChunkPacket {
    return DataChunkPacket._fromData(JSON.parse(json) as DataChunkPacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): DataChunkPacket {
    const data = msgpack.decode(bytes) as DataChunkPacketData;
    return DataChunkPacket._fromData(data);
  }
}