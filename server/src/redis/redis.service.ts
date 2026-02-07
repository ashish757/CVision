import { Injectable, Logger, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class RedisService implements OnModuleDestroy {
  public client: Redis;
  private readonly logger = new Logger(RedisService.name);
  private isConnected = false;
  private hasLoggedError = false;

  constructor() {
    this.client = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: Number(process.env.REDIS_PORT) || 6379,

      retryStrategy: (times) => {
        // Retry connection with exponential backoff
        if (times > 3) {
          // Stop retrying after 3 attempts
          this.logger.error(
            'Redis connection failed after 3 attempts. Stopping retries.',
          );
          return null; // Stop retrying
        }

        return Math.min(times * 1000, 3000); // dellay
      },

      maxRetriesPerRequest: 2,
      enableReadyCheck: true,
      lazyConnect: false,
    });

    this.client.on('connect', () => {
      this.isConnected = true;
      this.hasLoggedError = false;
      this.logger.log('Redis connected successfully');
    });

    this.client.on('ready', () => {
      this.isConnected = true;
      this.hasLoggedError = false;
      this.logger.log('Redis is ready to accept commands');
    });

    this.client.on('error', (error) => {
      this.isConnected = false;
      // Only log error once to avoid spam
      if (!this.hasLoggedError) {
        this.logger.error(
          'Redis connection error. Token blacklisting will be disabled.',
          error.message,
        );
        this.logger.warn(
          'Make sure Redis is running: redis-server or docker-compose up redis',
        );
        this.hasLoggedError = true;
      }
    });

    this.client.on('close', () => {
      this.isConnected = false;
      this.logger.warn('Redis connection closed');
    });

    this.client.on('reconnecting', () => {
      this.logger.log('Attempting to reconnect to Redis...');
    });
  }

  onModuleDestroy() {
    this.logger.log('Closing Redis connection');
    this.client.quit();
  }
}
