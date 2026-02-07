import { Link } from "react-router-dom";
import Logo from "../components/Logo.tsx";
import ThemeToggle from "../components/ThemeToggle.tsx";
import { Lightbulb, Zap, BarChart3 } from "lucide-react";

const Landing = () => {
  return (
    <div className="min-h-screen landing-bg">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Logo />
          <div className="flex items-center space-x-4">
            <Link
              to="/signin"
              className="text-muted hover:text-primary transition-colors font-medium"
            >
              Sign In
            </Link>
            <ThemeToggle />
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 pt-20 pb-32">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold text-text mb-6">
            AI-Powered{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
              CV Analysis
            </span>
          </h1>
          <p className="text-xl text-muted mb-10 max-w-2xl mx-auto">
            Transform your resume with intelligent insights. Our AI analyzes
            your CV, identifies gaps, and provides actionable recommendations
            to help you land your dream job.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/signin"
              className="bg-primary text-white hover:bg-primary/90 px-8 py-4 rounded-lg font-medium text-lg transition-all transform hover:scale-105 hover:shadow-lg w-full sm:w-auto shadow-primary/25"
            >
              Analyze Your CV Now
            </Link>
            <Link
              to="/signin"
              className="border-2 border-primary text-primary hover:bg-primary hover:text-white px-8 py-4 rounded-lg font-medium text-lg transition-all w-full sm:w-auto"
            >
              Watch Demo
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-32 grid md:grid-cols-3 gap-8">
          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20 hover:border-primary/50 transition-all group hover:shadow-2xl hover:shadow-primary/10">
            <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-yellow-500/30 transition-all">
              <Lightbulb className="w-7 h-7 text-primary group-hover:text-yellow-700" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              <span className="text-yellow-500 ">Light</span> but Heavy Analysis
            </h3>
            <p className="text-muted leading-relaxed">
              Our AI Heavily analyzes CV structure, content, and formatting
              to provide comprehensive insights, intelligently, instantly.
            </p>
          </div>

          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-secondary/20 hover:border-secondary/50 transition-all group hover:shadow-2xl hover:shadow-secondary/10">
            <div className="w-14 h-14 bg-secondary/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-blue-500/30 transition-all">
              <Zap className="w-7 h-7 text-secondary group-hover:text-blue-700" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              <span className="text-blue-500">Thunder</span> But Transparent
            </h3>
            <p className="text-muted leading-relaxed">
              As powerful as a lightning strike, but with transparency and unbias at its core.
            </p>
          </div>

          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-accent/20 hover:border-accent/50 transition-all group hover:shadow-2xl hover:shadow-accent/10">
            <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-500/30 transition-all">
              <BarChart3 className="w-7 h-7 text-accent group-hover:text-green-700" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              <span className="text-green-500">Graphs</span> but Real Benchmarks
            </h3>
            <p className="text-muted leading-relaxed">
              Now Control the Analysis and Rankings based on customized and weighted parameters.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/30 py-8">
        <div className="container mx-auto px-6 text-center text-muted">
          <p>&copy; 2026 CVision. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;

