import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";
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
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/10 to-background flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-2">
            <Logo />
          </Link>
        </div>

        {/* Sign Up Card */}
        <div className="bg-card/90 backdrop-blur-lg rounded-2xl p-8 border border-primary/20 shadow-2xl shadow-primary/5">
          <h2 className="text-2xl font-bold text-text text-center mb-2">
            {step === "info" ? "Create Account" : "Verify Your Email"}
          </h2>
          <p className="text-muted text-center mb-8">
            {step === "info"
              ? "Sign up to get started with CVision"
              : `Enter the OTP sent to ${email}`}
          </p>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-error/10 border border-error/30 rounded-lg">
              <p className="text-error text-sm text-center">{error}</p>
            </div>
          )}

          {/* Step 1: User Info */}
          {step === "info" && (
            <form onSubmit={handleSendOtp} className="space-y-6">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-muted mb-2"
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
                  className={`w-full px-4 py-3 bg-card/20 border ${
                    fieldErrors.name ? "border-error" : "border-border"
                  } rounded-lg text-text placeholder-muted focus:outline-none focus:ring-2 ${
                    fieldErrors.name ? "focus:ring-error" : "focus:ring-primary"
                  } focus:border-transparent transition-all`}
                  placeholder="John Doe"
                  required
                />
                {fieldErrors.name && (
                  <p className="text-sm text-error">{fieldErrors.name}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-muted mb-2"
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
                  className={`w-full px-4 py-3 bg-card/20 border ${
                    fieldErrors.email ? "border-error" : "border-border"
                  } rounded-lg text-text placeholder-muted focus:outline-none focus:ring-2 ${
                    fieldErrors.email ? "focus:ring-error" : "focus:ring-primary"
                  } focus:border-transparent transition-all`}
                  placeholder="you@example.com"
                  required
                />
                {fieldErrors.email && (
                  <p className="text-sm text-error">{fieldErrors.email}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-muted mb-2"
                >
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => handlePasswordChange(e.target.value)}
                  onBlur={handlePasswordBlur}
                  className={`w-full px-4 py-3 bg-card/20 border ${
                    fieldErrors.password ? "border-error" : "border-border"
                  } rounded-lg text-text placeholder-muted focus:outline-none focus:ring-2 ${
                    fieldErrors.password ? "focus:ring-error" : "focus:ring-primary"
                  } focus:border-transparent transition-all`}
                  placeholder="••••••••"
                  required
                />
                {/* Password Strength Indicator */}
                {password && !fieldErrors.password && (
                  <div className="mt-2">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-muted">Password strength:</span>
                      <span className={`text-xs font-medium ${getPasswordStrengthColor(passwordStrength)}`}>
                        {passwordStrength.charAt(0).toUpperCase() + passwordStrength.slice(1)}
                      </span>
                    </div>
                    <div className="w-full bg-muted/30 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-300 ${getPasswordStrengthBgColor(
                          passwordStrength
                        )} ${getPasswordStrengthWidth(passwordStrength)}`}
                      ></div>
                    </div>
                  </div>
                )}
                {fieldErrors.password && (
                  <p className="text-sm text-error">{fieldErrors.password}</p>
                )}
              </div>

              <div>
                <label
                  htmlFor="confirmPassword"
                  className="block text-sm font-medium text-muted mb-2"
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
                  className={`w-full px-4 py-3 bg-card/20 border ${
                    fieldErrors.confirmPassword ? "border-error" : "border-border"
                  } rounded-lg text-text placeholder-text-muted focus:outline-none focus:ring-2 ${
                    fieldErrors.confirmPassword ? "focus:ring-error" : "focus:ring-primary"
                  } focus:border-transparent transition-all`}
                  placeholder="••••••••"
                  required
                />
                {fieldErrors.confirmPassword && (
                  <p className="text-sm text-error">{fieldErrors.confirmPassword}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isRequestingOtp}
                className="w-full bg-primary hover:bg-primary/90 disabled:bg-primary/50 text-background py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                {isRequestingOtp ? (
                  <Loader2 className="animate-spin h-5 w-5" />
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
                  className="block text-sm font-medium text-muted mb-2"
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
                  className={`w-full px-4 py-3 bg-card/20 border ${
                    fieldErrors.otp ? "border-error" : "border-border"
                  } rounded-lg text-text placeholder-text-muted focus:outline-none focus:ring-2 ${
                    fieldErrors.otp ? "focus:ring-error" : "focus:ring-primary"
                  } focus:border-transparent transition-all text-center text-2xl tracking-widest`}
                  placeholder="000000"
                  required
                  maxLength={6}
                />
                {fieldErrors.otp && (
                  <p className="text-sm text-error text-center">{fieldErrors.otp}</p>
                )}
                <p className="mt-2 text-sm text-muted text-center">
                  Didn't receive the code?{" "}
                  <button
                    type="button"
                    onClick={handleResendOtp}
                    disabled={isRequestingOtp}
                    className="text-primary hover:text-primary/80 transition-colors disabled:opacity-50"
                  >
                    Resend
                  </button>
                </p>
              </div>

              <button
                type="submit"
                disabled={isRegistering}
                className="w-full bg-primary hover:bg-primary/90 disabled:bg-primary/50 text-background py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                {isRegistering ? (
                  <Loader2 className="animate-spin h-5 w-5" />
                ) : (
                  "Create Account"
                )}
              </button>

              <button
                type="button"
                onClick={handleBackToInfo}
                className="w-full text-muted hover:text-text py-2 text-sm transition-colors"
              >
                ← Back to edit details
              </button>
            </form>
          )}


          <p className="mt-8 text-center text-muted text-sm">
            Already have an account?{" "}
            <Link
              to="/signin"
              className="text-primary hover:text-primary/80 transition-colors"
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
