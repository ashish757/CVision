import {
  Injectable,
  UnauthorizedException,
  ConflictException,
  BadRequestException,
  Logger,
} from '@nestjs/common';
import { SendOtpDto, LoginDto, AuthDto } from './DTO/auth.dto';
import { PrismaService } from '../prisma/prisma.service';
import { JwtService } from './jwt.service';
import * as bcrypt from 'bcrypt';
import { generateOTP } from '../../utils/otp';
import { sendEmail } from '../../utils/email';
import { PASSWORD_SALT_ROUNDS } from '../../utils/constants';
import { otpTemplate } from '../../utils/emailTemplates';
import type { User } from '@prisma/client';
import * as crypto from 'node:crypto';

@Injectable()
export class AuthService {
  private readonly logger = new Logger(AuthService.name);

  constructor(
    private readonly jwtService: JwtService,
    private readonly prisma: PrismaService,
  ) {}

  async sendOtp(otpDto: SendOtpDto) {
    // Generate random 6-digit OTP
    const otp = generateOTP();

    this.logger.debug(`OTP generated for ${otpDto.email}: ${otp}`);
    this.logger.log(`Sending OTP to: ${otpDto.email}`);

    // Send email
    await sendEmail(
      otpDto.email,
      'CVision - Email Verification Code',
      otpTemplate(otpDto.name, otp),
    );
    return { emailId: otpDto.email };
  }

  async register(dto: AuthDto) {
    // verify the opt first
    // TODO: verify OTP, setup redis

    // after opt verification=, check if user with email already exists
    const existing = await this.prisma.user.findUnique({
      where: { email: dto.user.email },
      select: { id: true },
    });

    if (existing) throw new ConflictException('Email already in use');

    // user doesn't exists
    const hashed = await bcrypt.hash(dto.user.password, PASSWORD_SALT_ROUNDS);

    // Create user first to get the ID
    const user = await this.prisma.user.create({
      data: {
        name: dto.user.name,
        email: dto.user.email,
        password: hashed,
      },
    });

    return this.authenticateUser(user);
  }

  async authenticateUser(usr: User) {
    // Generate JWTs
    const payload = { sub: usr.id, email: usr.email };

    const accessToken = this.jwtService.sign(payload, 'access', {
      expiresIn: '15min',
    });

    const refreshToken = this.jwtService.sign(payload, 'refresh', {
      expiresIn: '7d',
    });


    // Save refresh token hash to database
    const hashedRefreshToken = crypto.createHash('sha256').update(refreshToken).digest('hex');


    // Limit refresh tokens to max 3
    let updatedTokens = [...usr.refreshTokens];
    if (updatedTokens.length >= 3) {
      updatedTokens = updatedTokens.slice(-2);
    }
    updatedTokens.push(hashedRefreshToken);

    // Update user with refresh Token
    // TODO: Create a dedicated table for refresh token (one-to-many)
    await this.prisma.user.update({
      where: { email: usr.email },
      data: { refreshTokens: updatedTokens },
    });

    return {
      accessToken,
      refreshToken,
      user: {
        id: usr.id,
        name: usr.name,
        email: usr.email,
        createdAt: usr.createdAt,
      },
    };
  }

  async login(dto: LoginDto) {
    // verify user from DB
    const user = await this.prisma.user.findUnique({
      where: { email: dto.email },
      select: {
        id: true,
        name: true,
        email: true,
        password: true,
        createdAt: true,
        updatedAt: true,
        refreshTokens: true,
      },
    });

    if (!user) throw new UnauthorizedException('Invalid email');

    // check if it's a social account (that is it has no password)
    if (user.password == null)
      throw new BadRequestException('Please Login with Google/Github');

    // Verify password
    const valid = await bcrypt.compare(dto.password, user.password);
    if (!valid) throw new UnauthorizedException('Invalid password');


    return this.authenticateUser(user)
  }

  async logout(userId: string, refreshToken: string): Promise<void> {
    const user = await this.prisma.user.findUnique({
      where: { id: userId },
      select: { refreshTokens: true },
    });

    if (!user) return;

    // Remove the specific refresh token
    const hashed = crypto.createHash('sha256').update(refreshToken).digest('hex');

    const updatedTokens: string[] = [];
    for (const hashedToken of user.refreshTokens) {
      const matches = hashed === hashedToken;
      if (!matches) {
        updatedTokens.push(hashedToken);
      }
    }

    await this.prisma.user.update({
      where: { id: userId },
      data: { refreshTokens: updatedTokens },
    });
  }

  async refreshToken(refreshToken: string) {
    const { payload, error } = this.jwtService.verify(
      refreshToken,
      'refresh',
    ) as { error: boolean | object; payload: any };

    if (error) throw new UnauthorizedException('Invalid refresh token');

    // check if user in the token really exists
    const user = await this.prisma.user.findUnique({
      where: { email: payload.email },
      select: {
        id: true,
        name: true,
        email: true,
        password: true,
        createdAt: true,
        updatedAt: true,
        refreshTokens: true,
      },
    });
    if (!user) throw new UnauthorizedException('User not found');

    // CRITICAL: Verify the refresh token exists in the database
    let tokenExists = false;
    const hashed = crypto.createHash('sha256').update(refreshToken).digest('hex');
    for (const hashedToken of user.refreshTokens) {
      if (hashed === hashedToken) {
        tokenExists = true;
        break;
      }
    }

    if (!tokenExists) {
      // SECURITY: Possible token reuse attack - invalidate all tokens
      this.logger.warn( `Token reuse detected for user ${user.id}. Invalidating all tokens.`);
      await this.prisma.user.update({
        where: { id: user.id },
        data: { refreshTokens: [] },
      });
      throw new UnauthorizedException(
        'Refresh token not found or has been revoked. All sessions invalidated.',
      );
    }

    // authenticate user - Generate new tokens
    return this.authenticateUser(user)
  }

}
