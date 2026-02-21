import { Injectable, Logger, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class RedisService implements OnModuleDestroy {
  public client: Redis;
  private readonly logger = new Logger(RedisService.name);
  private isConnected = false;
  private hasLoggedError = false;

  constructor() {
    const host = process.env.REDIS_HOST || 'localhost';
    const port = Number(process.env.REDIS_PORT) || 6379;
    const password = process.env.REDIS_PASSWORD;

    // Detect Azure Redis automatically
    const isAzureRedis = host.includes('windows.net');

    this.logger.log(
      `Initializing Redis connection → Host: ${host}, Mode: ${
        isAzureRedis ? 'Azure TLS' : 'Local'
      }`,
    );

    this.client = new Redis({
      host,
      port,
      password,

      // Azure-specific TLS config
      ...(isAzureRedis && {
        tls: {
          servername: host,
        },
        connectTimeout: 10000,
        keepAlive: 10000,
      }),

      retryStrategy: (times) => {
        // Retry connection with exponential backoff
        if (times > 100) {
          // Stop retrying after 3 attempts
          this.logger.error(
            'Redis connection failed after 100 attempts. Stopping retries.',
          );
          return null; // Stop retrying
        }

        return Math.min(times * 1000, 3000); // delay
      },

      maxRetriesPerRequest: 2,
      enableReadyCheck: true,
      lazyConnect: false,
    });

    // EVENT HANDLERS

    this.client.on('connect', () => {
      this.isConnected = true;
      this.hasLoggedError = false;
      this.logger.log('Redis connected successfully');
    });

    this.client.on('ready', () => {
      this.isConnected = true;
      this.logger.log('Redis is ready to accept commands');
    });

    this.client.on('error', (error) => {
      this.isConnected = false;

      if (!this.hasLoggedError) {
        this.logger.error(
          'Redis connection error. Token blacklisting will be disabled.',
          error.message,
        );

        if (!isAzureRedis) {
          this.logger.warn(
            'Make sure Redis is running locally: docker-compose up redis',
          );
        }

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

  // HEALTH CHECK METHOD

  async isHealthy(): Promise<boolean> {
    try {
      await this.client.ping();
      return true;
    } catch {
      return false;
    }
  }

  // CLEAN SHUTDOWN
  onModuleDestroy() {
    this.logger.log('Closing Redis connection');
    this.client.quit();
  }
}
