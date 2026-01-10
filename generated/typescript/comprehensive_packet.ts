// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface ComprehensivePacketData {
  packetType: string;
  intField: number;
  floatField: number;
  doubleField: number;
  stringField: string;
  boolField: boolean;
  datetimeField: string;
  timeField: string;
  listField: any[];
  listIntField: number[];
  listStringField: string[];
  mapField: Record<string, any>;
  embeddedMapField: Map<any, any>;
  mapStringDynamicField: Record<string, any>;
  bytesField: Uint8Array;
}

export interface ComprehensivePacketInput {
  intField: number;
  floatField: number;
  doubleField: number;
  stringField: string;
  boolField: boolean;
  datetimeField: Date | string;
  timeField: string;
  listField: any[];
  listIntField: number[];
  listStringField: string[];
  mapField: Record<string, any>;
  embeddedMapField: Map<any, any>;
  mapStringDynamicField: Record<string, any>;
  bytesField: Uint8Array;
}

export class ComprehensivePacket {
  static readonly TYPE = "/test/ComprehensivePacket";

  intField: number;
  floatField: number;
  doubleField: number;
  stringField: string;
  boolField: boolean;
  datetimeField: Date;
  timeField: string;
  listField: any[];
  listIntField: number[];
  listStringField: string[];
  mapField: Record<string, any>;
  embeddedMapField: Map<any, any>;
  mapStringDynamicField: Record<string, any>;
  bytesField: Uint8Array;

  constructor(data: ComprehensivePacketInput) {
    this.intField = data.intField;
    this.floatField = data.floatField;
    this.doubleField = data.doubleField;
    this.stringField = data.stringField;
    this.boolField = data.boolField;
    this.datetimeField = data.datetimeField instanceof Date ? data.datetimeField : new Date(data.datetimeField);
    this.timeField = data.timeField;
    this.listField = data.listField;
    this.listIntField = data.listIntField;
    this.listStringField = data.listStringField;
    this.mapField = data.mapField;
    this.embeddedMapField = data.embeddedMapField;
    this.mapStringDynamicField = data.mapStringDynamicField;
    this.bytesField = data.bytesField;
  }

  private _toData(): ComprehensivePacketData {
    return {
      packetType: ComprehensivePacket.TYPE,
      intField: this.intField,
      floatField: this.floatField,
      doubleField: this.doubleField,
      stringField: this.stringField,
      boolField: this.boolField,
      datetimeField: this.datetimeField.toISOString(),
      timeField: this.timeField,
      listField: this.listField,
      listIntField: this.listIntField,
      listStringField: this.listStringField,
      mapField: this.mapField,
      embeddedMapField: this.embeddedMapField,
      mapStringDynamicField: this.mapStringDynamicField,
      bytesField: this.bytesField,
    };
  }

  private static _fromData(data: ComprehensivePacketData): ComprehensivePacket {
    return new ComprehensivePacket({
      intField: data.intField,
      floatField: data.floatField,
      doubleField: data.doubleField,
      stringField: data.stringField,
      boolField: data.boolField,
      datetimeField: new Date(data.datetimeField),
      timeField: data.timeField,
      listField: data.listField,
      listIntField: data.listIntField,
      listStringField: data.listStringField,
      mapField: data.mapField,
      embeddedMapField: data.embeddedMapField,
      mapStringDynamicField: data.mapStringDynamicField,
      bytesField: data.bytesField,
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): ComprehensivePacket {
    return ComprehensivePacket._fromData(JSON.parse(json) as ComprehensivePacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): ComprehensivePacket {
    const data = msgpack.decode(bytes) as ComprehensivePacketData;
    return ComprehensivePacket._fromData(data);
  }
}