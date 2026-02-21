import {
  Controller,
  Post,
  Get,
  Param,
  Query,
  UseInterceptors,
  UploadedFile,
  BadRequestException,
  UseGuards,
  Req,
  HttpStatus,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { extname } from 'path';
import type { Request } from 'express';
import { ResumeService } from './resume.service';
import { AuthGuard } from '../../common/guards/auth.guard';
import { ResumeStatusQueryDto } from './DTO/resume.dto';

// Extend Request interface to include user
interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email: string;
    name?: string;
  };
}

@Controller('resumes')
@UseGuards(AuthGuard)
export class ResumeController {
  constructor(private readonly resumeService: ResumeService) {}

  @Post('upload')
  @UseInterceptors(
    FileInterceptor('file', {
      storage: diskStorage({
        destination: './uploads/resumes',
        filename: (req, file, callback) => {
          const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
          callback(null, `${uniqueSuffix}${extname(file.originalname)}`);
        },
      }),
      fileFilter: (req, file, callback) => {
        const allowedTypes = [
          'application/pdf',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          'application/msword',
        ];

        if (allowedTypes.includes(file.mimetype)) {
          callback(null, true);
        } else {
          callback(new BadRequestException('Only PDF and DOCX files are allowed'), false);
        }
      },
      limits: {
        fileSize: 5 * 1024 * 1024, // 5MB
      },
    }),
  )
  async uploadResume(
    @UploadedFile() file: Express.Multer.File,
    @Req() req: AuthenticatedRequest,
  ) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user?.id;
    if (!userId) {
      throw new BadRequestException('User not authenticated');
    }

    const result = await this.resumeService.uploadResume(
      userId,
      file.originalname,
      file.path,
    );

    return {
      status: 'success',
      statusCode: HttpStatus.CREATED,
      message: 'Resume uploaded successfully',
      data: result,
    };
  }

  @Get(':id/status')
  async getResumeStatus(
    @Param('id') resumeId: string,
    @Req() req: AuthenticatedRequest,
  ) {
    const userId = req.user?.id;
    if (!userId) {
      throw new BadRequestException('User not authenticated');
    }

    const result = await this.resumeService.getResumeStatus(resumeId, userId);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Resume status retrieved successfully',
      data: result,
    };
  }

  @Get(':id')
  async getResumeDetails(
    @Param('id') resumeId: string,
    @Req() req: AuthenticatedRequest,
  ) {
    const userId = req.user?.id;
    if (!userId) {
      throw new BadRequestException('User not authenticated');
    }

    const result = await this.resumeService.getResumeStatus(resumeId, userId);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Resume details retrieved successfully',
      data: result,
    };
  }

  @Get()
  async listResumes(
    @Query() query: ResumeStatusQueryDto,
    @Req() req: AuthenticatedRequest,
  ) {
    const userId = req.user?.id;
    if (!userId) {
      throw new BadRequestException('User not authenticated');
    }

    const page = parseInt(query.page || '1');
    const limit = parseInt(query.limit || '10');

    const result = await this.resumeService.listResumes(userId, page, limit);

    return {
      status: 'success',
      statusCode: HttpStatus.OK,
      message: 'Resumes retrieved successfully',
      data: result,
    };
  }
}
