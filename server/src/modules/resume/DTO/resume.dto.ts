import { IsString, IsOptional, IsNumber, IsArray } from 'class-validator';

export class UploadResumeDto {
  @IsString()
  filename: string;
}

export class ResumeStatusQueryDto {
  @IsOptional()
  @IsString()
  page?: string;

  @IsOptional()
  @IsString()
  limit?: string;
}

export class ResumeAnalysisDto {
  @IsString()
  resumeId: string;

  @IsString()
  filename: string;

  @IsString()
  status: string;

  @IsOptional()
  @IsNumber()
  score?: number;

  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  extractedSkills?: string[];

  @IsOptional()
  ranking?: {
    position: number;
    totalCandidates: number;
    percentile: number;
  };

  @IsOptional()
  @IsString()
  errorMessage?: string;
}

export class AiHealthDto {
  @IsString()
  status: string;

  @IsString()
  service: string;

  @IsString()
  version: string;
}

