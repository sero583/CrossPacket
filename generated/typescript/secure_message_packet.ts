// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface SecureMessagePacketData {
  packetType: string;
  messageId: string;
  senderId: number;
  recipientId: number;
  subject: string;
  body: string;
  attachments: any[];
  encryptedPayload: Uint8Array | null;
  priority: number;
  isRead: boolean;
  sentAt: string;
}

export interface SecureMessagePacketInput {
  messageId: string;
  senderId: number;
  recipientId: number;
  subject: string;
  body: string;
  attachments: any[];
  encryptedPayload?: Uint8Array | null;
  priority: number;
  isRead: boolean;
  sentAt: Date | string;
}

export class SecureMessagePacket {
  static readonly TYPE = "/example/SecureMessagePacket";

  messageId: string;
  senderId: number;
  recipientId: number;
  subject: string;
  body: string;
  attachments: any[];
  encryptedPayload: Uint8Array | null;
  priority: number;
  isRead: boolean;
  sentAt: Date;

  constructor(data: SecureMessagePacketInput) {
    this.messageId = data.messageId;
    this.senderId = data.senderId;
    this.recipientId = data.recipientId;
    this.subject = data.subject;
    this.body = data.body;
    this.attachments = data.attachments;
    this.encryptedPayload = data.encryptedPayload ?? null;
    this.priority = data.priority;
    this.isRead = data.isRead;
    this.sentAt = data.sentAt instanceof Date ? data.sentAt : new Date(data.sentAt);
  }

  private _toData(): SecureMessagePacketData {
    return {
      packetType: SecureMessagePacket.TYPE,
      messageId: this.messageId,
      senderId: this.senderId,
      recipientId: this.recipientId,
      subject: this.subject,
      body: this.body,
      attachments: this.attachments,
      encryptedPayload: this.encryptedPayload,
      priority: this.priority,
      isRead: this.isRead,
      sentAt: this.sentAt.toISOString(),
    };
  }

  private static _fromData(data: SecureMessagePacketData): SecureMessagePacket {
    return new SecureMessagePacket({
      messageId: data.messageId,
      senderId: data.senderId,
      recipientId: data.recipientId,
      subject: data.subject,
      body: data.body,
      attachments: data.attachments,
      encryptedPayload: data.encryptedPayload,
      priority: data.priority,
      isRead: data.isRead,
      sentAt: new Date(data.sentAt),
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): SecureMessagePacket {
    return SecureMessagePacket._fromData(JSON.parse(json) as SecureMessagePacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): SecureMessagePacket {
    const data = msgpack.decode(bytes) as SecureMessagePacketData;
    return SecureMessagePacket._fromData(data);
  }
}