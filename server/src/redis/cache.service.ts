import { Injectable } from '@nestjs/common';
import {Logger} from '@nestjs/common';
import * as jwt from 'jsonwebtoken';
import { RedisService } from './redis.service';

@Injectable()
export class CacheService {
  private readonly logger = new Logger(CacheService.name);

  constructor(private readonly redis: RedisService) {

  }

  async blacklistToken(token: string): Promise<void> {
    try {
      const decoded = jwt.decode(token) as { exp?: number };

      if (!decoded || !decoded.exp) {
        this.logger.warn(
          'Token has no expiration, using default TTL of 15 minutes',
        );
        await this.redis.client.set(`blacklist:${token}`, 'true', 'EX', 900); // 15 min default
        return;
      }

      // Calculate remaining TTL (time until token expires)
      const currentTime = Math.floor(Date.now() / 1000);
      const ttlSeconds = decoded.exp - currentTime;

      if (ttlSeconds > 0) {
        await this.redis.client.set(`blacklist:${token}`, 'true', 'EX', ttlSeconds);
        this.logger.debug(`Token blacklisted with TTL: ${ttlSeconds}s`);
      } else {
        this.logger.debug('Token already expired, skipping blacklist');
      }
    } catch (error) {
      this.logger.error('Error blacklisting token:', error.message);
      // Don't throw - allow logout to continue even if Redis fails
    }
  }

  async isTokenBlacklisted(token: string): Promise<boolean> {

    try {
      const res = await this.redis.client.get(`blacklist:${token}`);
      return res === 'true';
    } catch (error) {
      this.logger.error('Error checking token blacklist:', error.message);
      // On error, assume token is not blacklisted to avoid blocking valid requests
      return false;
    }
  }

  /**
   * Generic set method for caching objects
   * @param key Redis key
   * @param value Data to store (will be stringified)
   * @param ttl Time to live in seconds
   */
  async set(key: string, value: any, ttl: number): Promise<void> {
    try {
      const stringValue = JSON.stringify(value);
      await this.redis.client.set(key, stringValue, 'EX', ttl);
    } catch (error) {
      this.logger.error(`Error setting cache for ${key}:`, error.message);
    }
  }

  /**
   * Generic get method for cached objects
   */
  async get<T>(key: string): Promise<T | null> {
    try {
      const data = await this.redis.client.get(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      this.logger.error(`Error getting cache for ${key}:`, error.message);
      return null;
    }
  }

}