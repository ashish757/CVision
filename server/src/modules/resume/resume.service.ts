import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

export enum ResumeStatus {
  UPLOADED = 'UPLOADED',
  PROCESSING = 'PROCESSING',
  DONE = 'DONE',
  ERROR = 'ERROR'
}

@Injectable()
export class ResumeService {
  private readonly logger = new Logger(ResumeService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

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

    this.logger.log(`Resume uploaded: ${resume.id} - ${filename}`);

    // Start AI processing asynchronously
    this.processResumeWithAI(resume.id, filePath);

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

    // Parse ranking data if available
    let parsedRanking = null;
    if (resume.ranking) {
      try {
        parsedRanking = JSON.parse(resume.ranking);
      } catch (error) {
        this.logger.warn(`Failed to parse ranking data for resume ${resumeId}`, error.message);
      }
    }

    return {
      resumeId: resume.id,
      filename: resume.filename,
      status: resume.status,
      score: resume.score,
      extractedSkills: resume.extractedSkills || [],
      education: resume.education,
      ranking: parsedRanking,
      uploadedAt: resume.uploadedAt,
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

  async getAiServiceHealth() {
    try {
      const health = await this.aiService.checkHealth();
      this.logger.log('AI service health check passed');
      return health;
    } catch (error) {
      this.logger.error('AI service health check failed', error.message);
      throw error;
    }
  }

  private async updateResumeStatus(resumeId: string, status: ResumeStatus, errorMessage?: string) {
    await this.prisma.resume.update({
      where: { id: resumeId },
      data: {
        status,
        ...(errorMessage && { errorMessage }),
      },
    });
  }

  private async processResumeWithAI(resumeId: string, filePath: string) {
    try {
      this.logger.log(`Starting AI processing for resume: ${resumeId}`);

      // Update status to processing
      await this.updateResumeStatus(resumeId, ResumeStatus.PROCESSING);

      // Call AI service for analysis
      const analysisResult = await this.aiService.analyzeResume(filePath);

      this.logger.log(`AI analysis completed for resume: ${resumeId}, Score: ${analysisResult.score}`);

      // Calculate ranking (mock for now, but based on real AI score)
      const ranking = {
        position: Math.floor(Math.random() * 50) + 1, // This could be improved with actual ranking logic
        totalCandidates: 100,
        percentile: Math.floor((100 - analysisResult.score) + Math.random() * 20),
      };

      // Update resume with AI results
      await this.prisma.resume.update({
        where: { id: resumeId },
        data: {
          status: ResumeStatus.DONE,
          score: analysisResult.score,
          extractedSkills: analysisResult.skills,
          education: analysisResult.education,
          ranking: JSON.stringify(ranking),
          processedAt: new Date(),
        },
      });

      this.logger.log(`Resume processing completed successfully: ${resumeId}`);

    } catch (error) {
      this.logger.error(`AI processing failed for resume: ${resumeId}`, error.stack);

      // Update status to error
      await this.updateResumeStatus(
        resumeId,
        ResumeStatus.ERROR,
        error.message || 'AI processing failed'
      );
    }
  }
}
