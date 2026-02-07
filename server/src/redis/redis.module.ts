import { Module, Global } from '@nestjs/common';
import { CacheService } from './cache.service';
import { OtpService } from './otp.service';

@Global()
@Module({
  providers: [CacheService, OtpService],
  exports: [CacheService, OtpService],
})
export class RedisModule {}
