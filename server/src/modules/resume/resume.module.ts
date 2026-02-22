import { Module } from '@nestjs/common';
import { ResumeController } from './resume.controller';
import { ResumeService } from './resume.service';
import { PrismaModule } from '../prisma/prisma.module';
import { AiModule } from '../ai/ai.module';
import { JwtService } from '../auth/jwt.service';

@Module({
  imports: [PrismaModule, AiModule],
  controllers: [ResumeController],
  providers: [ResumeService, JwtService],
  exports: [ResumeService],
})
export class ResumeModule {}
