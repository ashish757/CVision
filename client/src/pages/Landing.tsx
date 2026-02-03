import { Link } from "react-router-dom";
import Logo from "../components/Logo.tsx";
import ThemeToggle from "../components/ThemeToggle.tsx";
import { Lightbulb, Zap, BarChart3 } from "lucide-react";

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/10 to-background">
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
              className="bg-primary hover:bg-primary/90 text-background px-8 py-4 rounded-lg font-medium text-lg transition-all transform hover:scale-105 hover:shadow-lg w-full sm:w-auto shadow-primary/25"
            >
              Analyze Your CV Now
            </Link>
            <Link
              to="/signin"
              className="border-2 border-primary text-primary hover:bg-primary hover:text-background px-8 py-4 rounded-lg font-medium text-lg transition-all w-full sm:w-auto"
            >
              Watch Demo
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-32 grid md:grid-cols-3 gap-8">
          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20 hover:border-primary/50 transition-all group hover:shadow-2xl hover:shadow-primary/10">
            <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-all">
              <Lightbulb className="w-7 h-7 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              Smart Analysis
            </h3>
            <p className="text-muted leading-relaxed">
              Our AI deeply analyzes your CV structure, content, and formatting
              to provide comprehensive insights.
            </p>
          </div>

          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-secondary/20 hover:border-secondary/50 transition-all group hover:shadow-2xl hover:shadow-secondary/10">
            <div className="w-14 h-14 bg-secondary/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-secondary/20 transition-all">
              <Zap className="w-7 h-7 text-secondary" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              Instant Feedback
            </h3>
            <p className="text-muted leading-relaxed">
              Get immediate, actionable recommendations to improve your CV and
              stand out from the competition.
            </p>
          </div>

          <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-accent/20 hover:border-accent/50 transition-all group hover:shadow-2xl hover:shadow-accent/10">
            <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-accent/20 transition-all">
              <BarChart3 className="w-7 h-7 text-accent" />
            </div>
            <h3 className="text-xl font-semibold text-text mb-3">
              Industry Benchmarks
            </h3>
            <p className="text-muted leading-relaxed">
              Compare your CV against industry standards and see how you stack
              up in your target field.
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

