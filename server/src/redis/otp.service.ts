// otp.service.ts
import { Injectable } from '@nestjs/common';
import { RedisService } from './redis.service';
import { generateOTP } from '../utils/otp';

@Injectable()
export class OtpService {
  constructor(private redis: RedisService) {}

  async saveOtp(email: string, ttl: number = 300) {
    const otp = generateOTP();

    try {
      await this.redis.client.set(`otp:${email}`, otp, 'EX', ttl);
      return true;
    } catch {
      return false;
    }

  }

  async verifyOtp(email: string, userOtp: string) {
    const storedOtp = await this.redis.client.get(`otp:${email}`);

    if (!storedOtp || storedOtp !== userOtp) {
      return false;
    }

    // Success! Delete the OTP so it can't be reused
    await this.redis.client.del(`otp:${email}`);

    return true;
  }

}
