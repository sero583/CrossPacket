// Auto-generated - do not modify manually
import * as msgpack from '@msgpack/msgpack';

export interface UserProfilePacketData {
  packetType: string;
  userId: number;
  username: string;
  email: string;
  bio: string | null;
  age: number | null;
  balance: number;
  tags: string[];
  preferences: Record<string, any>;
  avatar: Uint8Array | null;
  createdAt: string;
  lastLogin: string | null;
}

export interface UserProfilePacketInput {
  userId: number;
  username: string;
  email: string;
  bio?: string | null;
  age?: number | null;
  balance: number;
  tags: string[];
  preferences: Record<string, any>;
  avatar?: Uint8Array | null;
  createdAt: Date | string;
  lastLogin?: Date | string | null;
}

export class UserProfilePacket {
  static readonly TYPE = "/example/UserProfilePacket";

  userId: number;
  username: string;
  email: string;
  bio: string | null;
  age: number | null;
  balance: number;
  tags: string[];
  preferences: Record<string, any>;
  avatar: Uint8Array | null;
  createdAt: Date;
  lastLogin: Date | null;

  constructor(data: UserProfilePacketInput) {
    this.userId = data.userId;
    this.username = data.username;
    this.email = data.email;
    this.bio = data.bio ?? null;
    this.age = data.age ?? null;
    this.balance = data.balance;
    this.tags = data.tags;
    this.preferences = data.preferences;
    this.avatar = data.avatar ?? null;
    this.createdAt = data.createdAt instanceof Date ? data.createdAt : new Date(data.createdAt);
    this.lastLogin = data.lastLogin != null ? (data.lastLogin instanceof Date ? data.lastLogin : new Date(data.lastLogin)) : null;
  }

  private _toData(): UserProfilePacketData {
    return {
      packetType: UserProfilePacket.TYPE,
      userId: this.userId,
      username: this.username,
      email: this.email,
      bio: this.bio,
      age: this.age,
      balance: this.balance,
      tags: this.tags,
      preferences: this.preferences,
      avatar: this.avatar,
      createdAt: this.createdAt.toISOString(),
      lastLogin: this.lastLogin?.toISOString() ?? null,
    };
  }

  private static _fromData(data: UserProfilePacketData): UserProfilePacket {
    return new UserProfilePacket({
      userId: data.userId,
      username: data.username,
      email: data.email,
      bio: data.bio,
      age: data.age,
      balance: data.balance,
      tags: data.tags,
      preferences: data.preferences,
      avatar: data.avatar,
      createdAt: new Date(data.createdAt),
      lastLogin: data.lastLogin ? new Date(data.lastLogin) : null,
    });
  }

  toJSON(): string {
    return JSON.stringify(this._toData());
  }

  static fromJSON(json: string): UserProfilePacket {
    return UserProfilePacket._fromData(JSON.parse(json) as UserProfilePacketData);
  }

  toMsgPack(): Uint8Array {
    return msgpack.encode(this._toData());
  }

  static fromMsgPack(bytes: Uint8Array): UserProfilePacket {
    const data = msgpack.decode(bytes) as UserProfilePacketData;
    return UserProfilePacket._fromData(data);
  }
}