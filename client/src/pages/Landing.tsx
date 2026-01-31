import { Link } from "react-router-dom";
import Logo from "../components/Logo.tsx";

const Landing = () => {
  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Logo />
          <div className="flex items-center space-x-4">
            <Link
              to="/signin"
              className="text-gray-300 hover:text-white transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 pt-20 pb-32">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            AI-Powered{" "}
            <span className="text-transparent bg-clip-text bg-linear-to-r from-purple-400 to-pink-400">
              CV Analysis
            </span>
          </h1>
          <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
            Transform your resume with intelligent insights. Our AI analyzes
            your CV, identifies gaps, and provides actionable recommendations
            to help you land your dream job.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/signin"
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg font-medium text-lg transition-colors w-full sm:w-auto"
            >
              Analyze Your CV Now
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-32 grid md:grid-cols-3 gap-8">
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
            <div className="w-14 h-14 bg-purple-500/20 rounded-xl flex items-center justify-center mb-6">
              <svg
                className="w-7 h-7 text-purple-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              Smart Analysis
            </h3>
            <p className="text-gray-400">
              Our AI deeply analyzes your CV structure, content, and formatting
              to provide comprehensive insights.
            </p>
          </div>

          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
            <div className="w-14 h-14 bg-pink-500/20 rounded-xl flex items-center justify-center mb-6">
              <svg
                className="w-7 h-7 text-pink-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              Instant Feedback
            </h3>
            <p className="text-gray-400">
              Get immediate, actionable recommendations to improve your CV and
              stand out from the competition.
            </p>
          </div>

          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
            <div className="w-14 h-14 bg-blue-500/20 rounded-xl flex items-center justify-center mb-6">
              <svg
                className="w-7 h-7 text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              Industry Benchmarks
            </h3>
            <p className="text-gray-400">
              Compare your CV against industry standards and see how you stack
              up in your target field.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8">
        <div className="container mx-auto px-6 text-center text-gray-400">
          <p>&copy; 2026 CVision. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;

