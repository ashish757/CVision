import { Injectable, Logger, HttpException, HttpStatus } from '@nestjs/common';
import axios from 'axios';

export interface AIAnalysisRequest {
  file_path: string;
}

export interface AIAnalysisResponse {
  skills: string[];
  experience_years: number;
  education: string;
  score: number;
  processing_time_seconds: number;
}

export interface AIHealthResponse {
  status: string;
  service: string;
  version: string;
}

@Injectable()
export class AiService {
  private readonly logger = new Logger(AiService.name);
  private readonly httpClient: any;
  private readonly baseUrl: string;

  constructor() {
    this.baseUrl = process.env.AI_SERVER_URL || 'http://localhost:4000';

    this.httpClient = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000, // 30 seconds timeout for AI processing
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request/response interceptors for logging
    this.setupInterceptors();
  }

  /**
   * Analyze a resume file using the AI service
   */
  async analyzeResume(filePath: string): Promise<AIAnalysisResponse> {
    try {
      this.logger.log(`Starting resume analysis for file: ${filePath}`);

      // Check if file exists before sending to AI service
      const fs = require('fs');
      if (!fs.existsSync(filePath)) {
        throw new Error(`File does not exist: ${filePath}`);
      }

      // Get file stats for logging
      const stats = fs.statSync(filePath);
      this.logger.log(`File size: ${stats.size} bytes`);

      const request: AIAnalysisRequest = {
        file_path: filePath,
      };

      this.logger.log(`Sending request to AI service: ${JSON.stringify(request)}`);

      const response: any = await this.httpClient.post(
        '/api/v1/analyze',
        request,
      );

      this.logger.log(`AI analysis completed successfully. Score: ${response.data.score}`);

      return response.data;
    } catch (error) {
      this.logger.error(`Failed to analyze resume: ${error.message}`, error.stack);

      if (error.response) {
        const status = error.response?.status || 500;
        const message = error.response?.data?.detail || 'AI service analysis failed';

        this.logger.error(`AI service error response: ${JSON.stringify(error.response.data)}`);

        // Handle validation errors (422) as bad request
        const httpStatus = (status === 422 || (status >= 400 && status < 500))
          ? HttpStatus.BAD_REQUEST
          : HttpStatus.INTERNAL_SERVER_ERROR;

        throw new HttpException(
          {
            message: 'Resume analysis failed',
            details: message,
            aiServiceError: true,
          },
          httpStatus,
        );
      }

      throw new HttpException(
        'AI service is unavailable',
        HttpStatus.SERVICE_UNAVAILABLE,
      );
    }
  }

  /**
   * Check if the AI service is healthy and available
   */
  async checkHealth(): Promise<AIHealthResponse> {
    try {
      const response: any = await this.httpClient.get(
        '/api/v1/analyze/health',
      );

      this.logger.log('AI service health check passed');
      return response.data;
    } catch (error) {
      this.logger.error('AI service health check failed', error.message);

      throw new HttpException(
        'AI service is unavailable',
        HttpStatus.SERVICE_UNAVAILABLE,
      );
    }
  }

  /**
   * Get AI service information
   */
  async getServiceInfo(): Promise<any> {
    try {
      const response = await this.httpClient.get('/');
      return response.data;
    } catch (error) {
      this.logger.error('Failed to get AI service info', error.message);
      throw new HttpException(
        'AI service is unavailable',
        HttpStatus.SERVICE_UNAVAILABLE,
      );
    }
  }

  /**
   * Setup axios interceptors for logging and error handling
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.httpClient.interceptors.request.use(
      (config) => {
        this.logger.debug(`AI Service Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        this.logger.error('AI Service Request Error:', error);
        return Promise.reject(error);
      },
    );

    // Response interceptor
    this.httpClient.interceptors.response.use(
      (response) => {
        this.logger.debug(
          `AI Service Response: ${response.status} ${response.config.url} (${response.data?.processing_time_seconds || 0}s)`,
        );
        return response;
      },
      (error) => {
        const status = error.response?.status || 'Unknown';
        const url = error.config?.url || 'Unknown';
        this.logger.error(`AI Service Response Error: ${status} ${url}`, error.message);
        return Promise.reject(error);
      },
    );
  }
}


