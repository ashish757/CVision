import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useLoginMutation } from "../redux/auth/authApi";
import Logo from "../components/Logo.tsx";
import type { ApiError } from "../utils/Types";
import { validateEmail, validatePassword } from "../utils/validation";
import { Chrome, Loader2 } from "lucide-react";

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({
    email: "",
    password: "",
  });
  const navigate = useNavigate();

  // RTK Query mutation
  const [login, { isLoading }] = useLoginMutation();

  // Validate email field on blur
  const handleEmailBlur = () => {
    const result = validateEmail(email);
    setFieldErrors((prev) => ({
      ...prev,
      email: result.error || "",
    }));
  };

  // Validate password field on blur
  const handlePasswordBlur = () => {
    const result = validatePassword(password);
    setFieldErrors((prev) => ({
      ...prev,
      password: result.errors[0] || "",
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({ email: "", password: "" });

    // Validate all fields
    const emailValidation = validateEmail(email);
    const passwordValidation = validatePassword(password);

    // Check for validation errors
    if (!emailValidation.isValid || !passwordValidation.isValid) {
      setFieldErrors({
        email: emailValidation.error || "",
        password: passwordValidation.errors[0] || "",
      });
      return;
    }

    try {
      await login({ email, password }).unwrap();
      // Login successful, navigate to dashboard
      navigate("/dashboard");
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError?.data?.message || "Invalid email or password");
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

        {/* Sign In Card */}
        <div className="bg-card/90 backdrop-blur-lg rounded-2xl p-8 border border-primary/20 shadow-2xl shadow-primary/5">
          <h2 className="text-2xl font-bold text-text text-center mb-2">
            Welcome Back
          </h2>
          <p className="text-muted text-center mb-8">
            Sign in to continue to CVision
          </p>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-error/10 border border-error/30 rounded-lg">
              <p className="text-error text-sm text-center">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
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
                  // Clear field error on change
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
                <p className="mt-2 text-sm text-error">{fieldErrors.email}</p>
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
                onChange={(e) => {
                  setPassword(e.target.value);
                  // Clear field error on change
                  if (fieldErrors.password) {
                    setFieldErrors((prev) => ({ ...prev, password: "" }));
                  }
                }}
                onBlur={handlePasswordBlur}
                className={`w-full px-4 py-3 bg-card/20 border ${
                  fieldErrors.password ? "border-error" : "border-border"
                } rounded-lg text-text placeholder-text-muted focus:outline-none focus:ring-2 ${
                  fieldErrors.password ? "focus:ring-error" : "focus:ring-primary"
                } focus:border-transparent transition-all`}
                placeholder="••••••••"
                required
              />
              {fieldErrors.password && (
                <p className="mt-2 text-sm text-error">{fieldErrors.password}</p>
              )}
            </div>

            <div className="flex items-center justify-end">
              <a
                href="#"
                className="text-sm text-primary hover:text-primary/80 transition-colors"
              >
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary hover:bg-primary/90 disabled:bg-primary/50 text-background py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
            >
              {isLoading ? (
                <Loader2 className="animate-spin h-5 w-5" />
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border/20"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-transparent text-muted">
                  Or continue with
                </span>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-4">
              <button className="flex items-center justify-center px-4 py-3 border border-border/20 rounded-lg hover:bg-card/10 transition-colors">
                <Chrome className="w-5 h-5 mr-2" />
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

          <p className="mt-8 text-center text-muted text-sm">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="text-primary hover:text-primary/80 transition-colors"
            >
              Sign up for free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignIn;

