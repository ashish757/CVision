import {apiSlice} from "../apiSlice.ts";
import { API_CONFIG } from "../../config/api.config";

export const authApi = apiSlice.injectEndpoints({
    // reducerPath: 'userApi', // The name of the slice in the store

    // Define data types for cache invalidation
    // tagTypes: ['Auth'] ,

    endpoints: (builder) => ({
        login: builder.mutation({
            query: (credentials) => ({
                url: API_CONFIG.ENDPOINTS.AUTH.LOGIN,
                method: 'POST',
                body: credentials,
            }),
        }),

        requestOtp: builder.mutation({
            query: (otpData) => ({
                url: API_CONFIG.ENDPOINTS.AUTH.SEND_OTP,
                method: 'POST',
                body: otpData,
            }),
        }),

        register: builder.mutation({
            query: (registerData) => ({
                url: API_CONFIG.ENDPOINTS.AUTH.REGISTER,
                method: 'POST',
                body: registerData,
            }),
        }),

        logout: builder.mutation<void, void>({
            query: () => ({
                url: API_CONFIG.ENDPOINTS.AUTH.LOGOUT,
                method: 'POST',
            }),
        }),

        refreshToken: builder.mutation({
            query: () => ({
                url: API_CONFIG.ENDPOINTS.AUTH.REFRESH_TOKEN,
                method: 'POST',
            }),
        }),


    }),
});


export const { useLoginMutation, useRequestOtpMutation, useRegisterMutation, useLogoutMutation, useRefreshTokenMutation } = authApi;
