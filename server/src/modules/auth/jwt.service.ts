import * as jwt from 'jsonwebtoken';
import { Injectable } from '@nestjs/common';
import type { JwtPayload, SignOptions } from 'jsonwebtoken';

type TokenType = 'access' | 'refresh';

interface VerifyResult {
  payload?: JwtPayload | string;
  error?: boolean | { name: string; message: string };
}

@Injectable()
export class JwtService {
  private readonly expType: Record<TokenType, string> = {
    access: '15min',
    refresh: '7d',
  };

  private readonly secretType: Record<TokenType, string>;

  constructor() {
    // Validate secrets exist at service initialization
    this.secretType = {
      access: process.env.JWT_ACCESS_SECRET!,
      refresh: process.env.JWT_REFRESH_SECRET!,
    };
  }

  sign(payload: object, type: TokenType, options?: SignOptions): string {
    const signOption =
      options || ({ expiresIn: this.expType[type] } as SignOptions);

    return jwt.sign(payload, this.secretType[type], signOption);
  }

  verify(token: string, type: TokenType): VerifyResult {
    try {
      const payload = jwt.verify(token, this.secretType[type]);
      return { payload, error: false };
    } catch (err: unknown) {
      const error = err as Error;
      return {
        error: {
          name: error.name || 'JwtError',
          message: error.message || 'Invalid token',
        },
      };
    }
  }
}
