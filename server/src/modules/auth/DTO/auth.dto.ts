import { IsEmail, IsString, MinLength, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';

export class UserDto {
  @IsEmail() email: string;
  @IsString() @MinLength(3) name: string;
  @IsString() @MinLength(6) password: string;
}

export class AuthDto {
  @IsString() otp: string;
  @ValidateNested() @Type(() => UserDto) user: UserDto;
}

export class SendOtpDto {
  @IsString() name: string;
  @IsEmail() email: string;
}

export class LoginDto {
  @IsEmail() email: string;
  @IsString() @MinLength(6) password: string;
}
