import {
  Controller,
  Post,
  Body,
  HttpStatus,
  UnauthorizedException,
  Res,
  Req,
  UseGuards,
} from '@nestjs/common';
import type { Response, Request } from 'express';
import { AuthService } from './auth.service';
import { SendOtpDto, AuthDto, LoginDto } from './DTO/auth.dto';
import { AuthGuard } from '../../common/guards/auth.guard';
import { CookieConfig } from '../../utils/cookie';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('/send-otp')
  async sendOtp(@Body() req: SendOtpDto) {
    const data = await this.authService.sendOtp(req);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'OTP sent',
      data: data,
    };
  }

  @Post('/register')
  async register(
    @Body() req: AuthDto,
    @Res({ passthrough: true }) res: Response,
  ) {
    const data = await this.authService.register(req);

    // Set refresh token in HttpOnly cookie
    CookieConfig.setRefreshTokenCookie(res, data.refreshToken);

    return {
      status: 'success',
      statusCode: HttpStatus.CREATED,
      message: 'User Registered successfully',
      data: {
        accessToken: data.accessToken,
        user: {
          name: data.user.name,
          email: data.user.email,
          id: data.user.id,
        },
      },
    };
  }

  @Post('/login')
  async login(
    @Body() req: LoginDto,
    @Res({ passthrough: true }) res: Response,
  ) {
    const data = await this.authService.login(req);

    // Set refresh token in HttpOnly cookie
    CookieConfig.setRefreshTokenCookie(res, data.refreshToken);

    // Only send access token in response body
    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Login successful',
      data: {
        accessToken: data.accessToken,
        user: data.user,
      },
    };
  }


  @Post('/refresh-token')
  async refreshToken(
    @Req() req: Request,
    @Res({ passthrough: true }) res: Response,
  ) {
    // Read refresh token from HttpOnly cookie
    const refreshToken = req.cookies?.refreshToken;

    if (!refreshToken) {
      throw new UnauthorizedException('Refresh token not found');
    }

    const data = await this.authService.refreshToken(refreshToken);

    // Set new refresh token in HttpOnly cookie
    CookieConfig.setRefreshTokenCookie(res, data.refreshToken);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Token refreshed successfully',
      data: {
        accessToken: data.accessToken,
        user: data.user,
      },
    };
  }

  @Post('/logout')
  @UseGuards(AuthGuard)
  async logout(@Req() req: Request, @Res({ passthrough: true }) res: Response) {
    const refreshToken = req.cookies?.refreshToken;
    const user = (req as any).user; // Set by AuthGuard

    if (refreshToken && user) {
      await this.authService.logout(user.sub, refreshToken);
    }

    // Clear refresh token cookie
    CookieConfig.clearRefreshTokenCookie(res);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Logged out successfully',
    };
  }

}
