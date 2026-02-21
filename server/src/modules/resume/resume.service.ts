import { Injectable, NotFoundException, } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export enum ResumeStatus {
  UPLOADED = 'UPLOADED',
  PROCESSING = 'PROCESSING',
  DONE = 'DONE',
  ERROR = 'ERROR'
}

@Injectable()
export class ResumeService {
  constructor(private prisma: PrismaService) {}

  async uploadResume(userId: string, filename: string, filePath: string) {
    // Create resume record in database
    const resume = await this.prisma.resume.create({
      data: {
        userId,
        filename,
        filePath,
        status: ResumeStatus.UPLOADED,
        uploadedAt: new Date(),
      },
    });

    // TODO: Queue for processing with AI service
    // For now, we'll simulate processing by updating status
    setTimeout(async () => {
      await this.updateResumeStatus(resume.id, ResumeStatus.PROCESSING);

      // Simulate processing time
      setTimeout(async () => {
        await this.completeProcessing(resume.id);
      }, 5000);
    }, 1000);

    return {
      resumeId: resume.id,
      filename: resume.filename,
      status: resume.status,
    };
  }

  async getResumeStatus(resumeId: string, userId: string) {
    const resume = await this.prisma.resume.findFirst({
      where: { id: resumeId, userId },
    });

    if (!resume) {
      throw new NotFoundException('Resume not found');
    }

    return {
      resumeId: resume.id,
      filename: resume.filename,
      status: resume.status,
      score: resume.score,
      extractedSkills: resume.extractedSkills || [],
      ranking: resume.ranking ? JSON.parse(resume.ranking) : null,
      processedAt: resume.processedAt,
      errorMessage: resume.errorMessage,
    };
  }

  async listResumes(userId: string, page: number = 1, limit: number = 10) {
    const skip = (page - 1) * limit;

    const [resumes, total] = await Promise.all([
      this.prisma.resume.findMany({
        where: { userId },
        skip,
        take: limit,
        orderBy: { uploadedAt: 'desc' },
        select: {
          id: true,
          filename: true,
          status: true,
          score: true,
          uploadedAt: true,
          processedAt: true,
        },
      }),
      this.prisma.resume.count({ where: { userId } }),
    ]);

    return {
      resumes,
      total,
      page,
      limit,
    };
  }

  private async updateResumeStatus(resumeId: string, status: ResumeStatus) {
    await this.prisma.resume.update({
      where: { id: resumeId },
      data: { status },
    });
  }

  private async completeProcessing(resumeId: string) {
    // Simulate AI processing results
    const mockResults = {
      status: ResumeStatus.DONE,
      score: Math.floor(Math.random() * 40) + 60, // Score between 60-100
      extractedSkills: [
        'JavaScript',
        'React',
        'Node.js',
        'TypeScript',
        'Python',
        'SQL',
        'Git',
        'Agile',
      ],
      ranking: JSON.stringify({
        position: Math.floor(Math.random() * 50) + 1,
        totalCandidates: 100,
      }),
      processedAt: new Date(),
    };

    await this.prisma.resume.update({
      where: { id: resumeId },
      data: mockResults,
    });
  }
}
