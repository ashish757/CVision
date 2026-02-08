import { Module, Global } from '@nestjs/common';
import { CacheService } from './cache.service';
import { OtpService } from './otp.service';
import { RedisService } from './redis.service';

@Global()
@Module({
  providers: [CacheService, OtpService, RedisService],
  exports: [CacheService, OtpService],
})
export class RedisModule {}
