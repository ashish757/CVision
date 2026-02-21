/**
 * API Configuration
 * Centralized configuration for API endpoints and base URLs
 */


// Base URL logic: use localhost for development, env variable for production
const getBaseUrl = (): string => {
        return import.meta.env.VITE_API_BASE_URL;
};

export const API_CONFIG = {
    // Base URL for the API server
    BASE_URL: getBaseUrl(),

    // API endpoints
    ENDPOINTS: {
        AUTH: {
            LOGIN: '/auth/login',
            REGISTER: '/auth/register',
            LOGOUT: '/auth/logout',
            SEND_OTP: '/auth/send-otp',
            REFRESH_TOKEN: '/auth/refresh-token',
        },
        RESUMES: {
            UPLOAD: '/resumes/upload',
            STATUS: (id: string) => `/resumes/${id}/status`,
            DETAILS: (id: string) => `/resumes/${id}`,
            LIST: '/resumes',
        }
    },

    // Request settings
    TIMEOUT: 30000, // 30 seconds

    // Retry settings
    MAX_RETRIES: 3,
} as const;


