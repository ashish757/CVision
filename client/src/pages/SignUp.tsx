import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useRegisterMutation, useRequestOtpMutation } from "../redux/auth/authApi";
import Logo from "../components/Logo";
import type { ApiError } from "../utils/Types";
import {
  validateEmail,
  validateName,
  validatePassword,
  validatePasswordMatch,
  validateOTP,
  getPasswordStrengthColor,
  getPasswordStrengthBgColor,
  getPasswordStrengthWidth,
} from "../utils/validation";

const SignUp = () => {
  // Form state
  const [step, setStep] = useState<"info" | "otp">("info");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [passwordStrength, setPasswordStrength] = useState<"weak" | "medium" | "strong">("weak");
  const [fieldErrors, setFieldErrors] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    otp: "",
  });

  const navigate = useNavigate();

  // RTK Query mutations
  const [requestOtp, { isLoading: isRequestingOtp }] = useRequestOtpMutation();
  const [register, { isLoading: isRegistering }] = useRegisterMutation();

  // Field validation handlers
  const handleNameBlur = () => {
    const result = validateName(name);
    setFieldErrors((prev) => ({
      ...prev,
      name: result.error || "",
    }));
  };

  const handleEmailBlur = () => {
    const result = validateEmail(email);
    setFieldErrors((prev) => ({
      ...prev,
      email: result.error || "",
    }));
  };

  const handlePasswordChange = (value: string) => {
    setPassword(value);
    const result = validatePassword(value);
    setPasswordStrength(result.strength);

    // Clear error on change
    if (fieldErrors.password) {
      setFieldErrors((prev) => ({ ...prev, password: "" }));
    }
  };

  const handlePasswordBlur = () => {
    const result = validatePassword(password);
    setFieldErrors((prev) => ({
      ...prev,
      password: result.errors[0] || "",
    }));
  };

  const handleConfirmPasswordBlur = () => {
    const result = validatePasswordMatch(password, confirmPassword);
    setFieldErrors((prev) => ({
      ...prev,
      confirmPassword: result.error || "",
    }));
  };

  const handleOtpBlur = () => {
    const result = validateOTP(otp);
    setFieldErrors((prev) => ({
      ...prev,
      otp: result.error || "",
    }));
  };

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({ name: "", email: "", password: "", confirmPassword: "", otp: "" });

    // Validate all fields
    const nameValidation = validateName(name);
    const emailValidation = validateEmail(email);
    const passwordValidation = validatePassword(password);
    const passwordMatchValidation = validatePasswordMatch(password, confirmPassword);

    // Check for validation errors
    const hasErrors =
      !nameValidation.isValid ||
      !emailValidation.isValid ||
      !passwordValidation.isValid ||
      !passwordMatchValidation.isValid;

    if (hasErrors) {
      setFieldErrors({
        name: nameValidation.error || "",
        email: emailValidation.error || "",
        password: passwordValidation.errors[0] || "",
        confirmPassword: passwordMatchValidation.error || "",
        otp: "",
      });
      return;
    }

    try {
      await requestOtp({ name, email }).unwrap();
      setStep("otp");
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError?.data?.message || "Failed to send OTP. Please try again.");
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors((prev) => ({ ...prev, otp: "" }));

    // Validate OTP
    const otpValidation = validateOTP(otp);
    if (!otpValidation.isValid) {
      setFieldErrors((prev) => ({ ...prev, otp: otpValidation.error || "" }));
      return;
    }

    try {
      await register({
        otp,
        user: {
          name,
          email,
          password,
        },
      }).unwrap();

      // Registration successful, navigate to dashboard
      navigate("/dashboard");
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError?.data?.message || "Registration failed. Please try again.");
    }
  };

  const handleBackToInfo = () => {
    setStep("info");
    setOtp("");
    setError("");
    setFieldErrors({ name: "", email: "", password: "", confirmPassword: "", otp: "" });
  };

  const handleResendOtp = async () => {
    setError("");
    try {
      await requestOtp({ name, email }).unwrap();
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError?.data?.message || "Failed to resend OTP. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-2">
            <Logo />
          </Link>
        </div>

        {/* Sign Up Card */}
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
          <h2 className="text-2xl font-bold text-white text-center mb-2">
            {step === "info" ? "Create Account" : "Verify Your Email"}
          </h2>
          <p className="text-gray-400 text-center mb-8">
            {step === "info"
              ? "Sign up to get started with CVision"
              : `Enter the OTP sent to ${email}`}
          </p>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
              <p className="text-red-400 text-sm text-center">{error}</p>
            </div>
          )}

          {/* Step 1: User Info */}
          {step === "info" && (
            <form onSubmit={handleSendOtp} className="space-y-6">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-300 mb-2"
                >
                  Full Name
                </label>
                <input
                  type="text"
                  id="name"
                  value={name}
                  onChange={(e) => {
                    setName(e.target.value);
                    if (fieldErrors.name) {
                      setFieldErrors((prev) => ({ ...prev, name: "" }));
                    }
                  }}
                  onBlur={handleNameBlur}
                  className={`w-full px-4 py-3 bg-white/5 border ${
                    fieldErrors.name ? "border-red-500" : "border-white/10"
                  } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 ${
                    fieldErrors.name ? "focus:ring-red-500" : "focus:ring-purple-500"
                  } focus:border-transparent transition-all`}
                  placeholder="John Doe"
                  required
                />
                {fieldErrors.name && (
                  <p className="mt-2 text-sm text-red-400">{fieldErrors.name}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-300 mb-2"
                >
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (fieldErrors.email) {
                      setFieldErrors((prev) => ({ ...prev, email: "" }));
                    }
                  }}
                  onBlur={handleEmailBlur}
                  className={`w-full px-4 py-3 bg-white/5 border ${
                    fieldErrors.email ? "border-red-500" : "border-white/10"
                  } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 ${
                    fieldErrors.email ? "focus:ring-red-500" : "focus:ring-purple-500"
                  } focus:border-transparent transition-all`}
                  placeholder="you@example.com"
                  required
                />
                {fieldErrors.email && (
                  <p className="mt-2 text-sm text-red-400">{fieldErrors.email}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-300 mb-2"
                >
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => handlePasswordChange(e.target.value)}
                  onBlur={handlePasswordBlur}
                  className={`w-full px-4 py-3 bg-white/5 border ${
                    fieldErrors.password ? "border-red-500" : "border-white/10"
                  } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 ${
                    fieldErrors.password ? "focus:ring-red-500" : "focus:ring-purple-500"
                  } focus:border-transparent transition-all`}
                  placeholder="••••••••"
                  required
                />
                {/* Password Strength Indicator */}
                {password && !fieldErrors.password && (
                  <div className="mt-2">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-gray-400">Password strength:</span>
                      <span className={`text-xs font-medium ${getPasswordStrengthColor(passwordStrength)}`}>
                        {passwordStrength.charAt(0).toUpperCase() + passwordStrength.slice(1)}
                      </span>
                    </div>
                    <div className="w-full bg-white/10 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-300 ${getPasswordStrengthBgColor(
                          passwordStrength
                        )} ${getPasswordStrengthWidth(passwordStrength)}`}
                      ></div>
                    </div>
                  </div>
                )}
                {fieldErrors.password && (
                  <p className="mt-2 text-sm text-red-400">{fieldErrors.password}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="confirmPassword"
                  className="block text-sm font-medium text-gray-300 mb-2"
                >
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    if (fieldErrors.confirmPassword) {
                      setFieldErrors((prev) => ({ ...prev, confirmPassword: "" }));
                    }
                  }}
                  onBlur={handleConfirmPasswordBlur}
                  className={`w-full px-4 py-3 bg-white/5 border ${
                    fieldErrors.confirmPassword ? "border-red-500" : "border-white/10"
                  } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 ${
                    fieldErrors.confirmPassword ? "focus:ring-red-500" : "focus:ring-purple-500"
                  } focus:border-transparent transition-all`}
                  placeholder="••••••••"
                  required
                />
                {fieldErrors.confirmPassword && (
                  <p className="mt-2 text-sm text-red-400">{fieldErrors.confirmPassword}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isRequestingOtp}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                {isRequestingOtp ? (
                  <svg
                    className="animate-spin h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  "Send OTP"
                )}
              </button>
            </form>
          )}

          {/* Step 2: OTP Verification */}
          {step === "otp" && (
            <form onSubmit={handleRegister} className="space-y-6">
              <div>
                <label
                  htmlFor="otp"
                  className="block text-sm font-medium text-gray-300 mb-2"
                >
                  Enter OTP
                </label>
                <input
                  type="text"
                  id="otp"
                  value={otp}
                  onChange={(e) => {
                    const value = e.target.value.replace(/\D/g, "").slice(0, 6);
                    setOtp(value);
                    if (fieldErrors.otp) {
                      setFieldErrors((prev) => ({ ...prev, otp: "" }));
                    }
                  }}
                  onBlur={handleOtpBlur}
                  className={`w-full px-4 py-3 bg-white/5 border ${
                    fieldErrors.otp ? "border-red-500" : "border-white/10"
                  } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 ${
                    fieldErrors.otp ? "focus:ring-red-500" : "focus:ring-purple-500"
                  } focus:border-transparent transition-all text-center text-2xl tracking-widest`}
                  placeholder="000000"
                  required
                  maxLength={6}
                />
                {fieldErrors.otp && (
                  <p className="mt-2 text-sm text-red-400 text-center">{fieldErrors.otp}</p>
                )}
                <p className="mt-2 text-sm text-gray-400 text-center">
                  Didn't receive the code?{" "}
                  <button
                    type="button"
                    onClick={handleResendOtp}
                    disabled={isRequestingOtp}
                    className="text-purple-400 hover:text-purple-300 transition-colors disabled:opacity-50"
                  >
                    Resend
                  </button>
                </p>
              </div>

              <button
                type="submit"
                disabled={isRegistering}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                {isRegistering ? (
                  <svg
                    className="animate-spin h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  "Create Account"
                )}
              </button>

              <button
                type="button"
                onClick={handleBackToInfo}
                className="w-full text-gray-400 hover:text-gray-300 py-2 text-sm transition-colors"
              >
                ← Back to edit details
              </button>
            </form>
          )}

          {/* Social Sign Up */}
          {step === "info" && (
            <>
              <div className="mt-6">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-white/10"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-transparent text-gray-400">
                      Or continue with
                    </span>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-2 gap-4">
                  <button className="flex items-center justify-center px-4 py-3 border border-white/10 rounded-lg hover:bg-white/5 transition-colors">
                    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                      <path
                        fill="#fff"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="#fff"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="#fff"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="#fff"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                    <span className="text-white text-sm">Google</span>
                  </button>
                  <button className="flex items-center justify-center px-4 py-3 border border-white/10 rounded-lg hover:bg-white/5 transition-colors">
                    <svg className="w-5 h-5 mr-2" fill="#fff" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                    </svg>
                    <span className="text-white text-sm">GitHub</span>
                  </button>
                </div>
              </div>
            </>
          )}

          <p className="mt-8 text-center text-gray-400 text-sm">
            Already have an account?{" "}
            <Link
              to="/signin"
              className="text-purple-400 hover:text-purple-300 transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
