import { apiSlice } from "../apiSlice";
import { API_CONFIG } from "../../config/api.config";

/**
 * Resume processing status types
 */
export type ResumeStatus = 'UPLOADED' | 'PROCESSING' | 'DONE' | 'ERROR';

/**
 * Resume upload response
 */
export interface ResumeUploadResponse {
    status: string;
    statusCode: number;
    message: string;
    data: {
        resumeId: string;
        filename: string;
        status: ResumeStatus;
    };
}

/**
 * Resume status response
 */
export interface ResumeStatusResponse {
    status: string;
    statusCode: number;
    message: string;
    data: {
        resumeId: string;
        filename: string;
        status: ResumeStatus;
        score?: number;
        extractedSkills?: string[];
        ranking?: {
            position: number;
            totalCandidates: number;
        };
        processedAt?: string;
        errorMessage?: string;
    };
}

/**
 * Resume list item
 */
export interface Resume {
    id: string;
    filename: string;
    status: ResumeStatus;
    score?: number;
    uploadedAt: string;
    processedAt?: string;
}

/**
 * Resume list response
 */
export interface ResumeListResponse {
    status: string;
    statusCode: number;
    message: string;
    data: {
        resumes: Resume[];
        total: number;
        page: number;
        limit: number;
    };
}

/**
 * Resume API endpoints
 */
export const resumeApi = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        /**
         * Upload a resume file
         */
        uploadResume: builder.mutation<ResumeUploadResponse, FormData>({
            query: (formData) => ({
                url: API_CONFIG.ENDPOINTS.RESUMES.UPLOAD,
                method: 'POST',
                body: formData,
                // Don't set Content-Type header, let browser set it with boundary for multipart
            }),
        }),

        /**
         * Get resume processing status
         */
        getResumeStatus: builder.query<ResumeStatusResponse, string>({
            query: (resumeId) => API_CONFIG.ENDPOINTS.RESUMES.STATUS(resumeId),
        }),

        /**
         * Get resume details
         */
        getResumeDetails: builder.query<ResumeStatusResponse, string>({
            query: (resumeId) => API_CONFIG.ENDPOINTS.RESUMES.DETAILS(resumeId),
        }),

        /**
         * List all resumes for the current user
         */
        listResumes: builder.query<ResumeListResponse, { page?: number; limit?: number }>({
            query: ({ page = 1, limit = 10 } = {}) => ({
                url: `${API_CONFIG.ENDPOINTS.RESUMES.LIST}?page=${page}&limit=${limit}`,
            }),
        }),
    }),
});

export const {
    useUploadResumeMutation,
    useGetResumeStatusQuery,
    useGetResumeDetailsQuery,
    useListResumesQuery,
} = resumeApi;
