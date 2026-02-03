/**
 * Validation utility functions for form inputs
 */

/**
 * Validation result type
 */
export interface ValidationResult {
    isValid: boolean;
    error?: string;
}

/**
 * Password validation result with strength indicator
 */
export interface PasswordValidationResult {
    isValid: boolean;
    errors: string[];
    strength: 'weak' | 'medium' | 'strong';
}

/**
 * Validate email format
 */
export const validateEmail = (email: string): ValidationResult => {
    if (!email || email.trim().length === 0) {
        return { isValid: false, error: 'Email is required' };
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return { isValid: false, error: 'Please enter a valid email address' };
    }

    return { isValid: true };
};

/**
 * Validate password with strength calculation
 */
export const validatePassword = (password: string): PasswordValidationResult => {
    const errors: string[] = [];
    let strength: 'weak' | 'medium' | 'strong' = 'weak';

    if (!password || password.length === 0) {
        errors.push('Password is required');
        return { isValid: false, errors, strength };
    }

    // Only requirement: minimum 6 characters
    if (password.length < 6) {
        errors.push('Password must be at least 6 characters long');
    }

    // Calculate strength for indicator (but don't enforce)
    let strengthScore = 0;
    if (password.length >= 6) strengthScore++;
    if (password.length >= 8) strengthScore++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strengthScore++;
    if (/[0-9]/.test(password)) strengthScore++;
    if (/[^a-zA-Z0-9]/.test(password)) strengthScore++;

    if (strengthScore <= 2) strength = 'weak';
    else if (strengthScore <= 4) strength = 'medium';
    else strength = 'strong';

    return {
        isValid: errors.length === 0,
        errors,
        strength
    };
};

/**
 * Validate name
 */
export const validateName = (name: string): ValidationResult => {
    if (!name || name.trim().length === 0) {
        return { isValid: false, error: 'Name is required' };
    }

    if (name.trim().length < 2) {
        return { isValid: false, error: 'Name must be at least 2 characters long' };
    }

    if (name.trim().length > 50) {
        return { isValid: false, error: 'Name must not exceed 50 characters' };
    }

    const nameRegex = /^[a-zA-Z\s'-]+$/;
    if (!nameRegex.test(name)) {
        return { isValid: false, error: 'Name can only contain letters, spaces, hyphens, and apostrophes' };
    }

    return { isValid: true };
};

/**
 * Validate password confirmation matches
 */
export const validatePasswordMatch = (password: string, confirmPassword: string): ValidationResult => {
    if (!confirmPassword || confirmPassword.length === 0) {
        return { isValid: false, error: 'Please confirm your password' };
    }

    if (password !== confirmPassword) {
        return { isValid: false, error: 'Passwords do not match' };
    }

    return { isValid: true };
};

/**
 * Validate OTP (6 digits)
 */
export const validateOTP = (otp: string): ValidationResult => {
    if (!otp || otp.trim().length === 0) {
        return { isValid: false, error: 'OTP is required' };
    }

    if (otp.length !== 6) {
        return { isValid: false, error: 'OTP must be 6 digits' };
    }

    const otpRegex = /^\d{6}$/;
    if (!otpRegex.test(otp)) {
        return { isValid: false, error: 'OTP must contain only numbers' };
    }

    return { isValid: true };
};

/**
 * Get password strength color for UI
 */
export const getPasswordStrengthColor = (strength: 'weak' | 'medium' | 'strong'): string => {
    switch (strength) {
        case 'weak':
            return 'text-error';
        case 'medium':
            return 'text-warning';
        case 'strong':
            return 'text-success';
    }
};

/**
 * Get password strength bar width
 */
export const getPasswordStrengthWidth = (strength: 'weak' | 'medium' | 'strong'): string => {
    switch (strength) {
        case 'weak':
            return 'w-1/3';
        case 'medium':
            return 'w-2/3';
        case 'strong':
            return 'w-full';
    }
};

/**
 * Get password strength background color
 */
export const getPasswordStrengthBgColor = (strength: 'weak' | 'medium' | 'strong'): string => {
    switch (strength) {
        case 'weak':
            return 'bg-error';
        case 'medium':
            return 'bg-warning';
        case 'strong':
            return 'bg-success';
    }
};
