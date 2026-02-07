import { Module, Global } from '@nestjs/common';
import { CacheService } from './cache.service';

@Global()
@Module({
  providers: [
    CacheService,
    {
      provide: 'RedisService',
      useExisting: CacheService,
    },
  ],
  exports: [CacheService, 'RedisService'],
})
export class RedisModule {}
