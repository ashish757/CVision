import { IsString, IsOptional } from 'class-validator';

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
