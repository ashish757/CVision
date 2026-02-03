import { Module } from '@nestjs/common';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtService } from './jwt.service';
import { PrismaModule } from '../prisma/prisma.module';
import { AuthGuard } from '../../common/guards/auth.guard';

@Module({
  imports: [PrismaModule],
  controllers: [AuthController],
  providers: [AuthService, JwtService, AuthGuard],
  exports: [JwtService, AuthGuard],
})
export class AuthModule {}
