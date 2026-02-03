import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/10 to-background flex items-center justify-center px-6">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
            404
          </h1>
        </div>
        <h2 className="text-3xl md:text-4xl font-bold text-text mb-4">
          Page Not Found
        </h2>
        <p className="text-muted text-lg mb-8 max-w-md mx-auto">
          Oops! The page you're looking for doesn't exist or has been moved to
          another location.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/"
            className="bg-primary hover:bg-primary/90 text-background px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Back to Home
          </Link>
          <Link
            to="/dashboard"
            className="border border-border hover:border-primary text-text hover:text-primary px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Go to Dashboard
          </Link>
        </div>

        {/* Decorative elements */}
        <div className="mt-16 flex justify-center space-x-4">
          <div className="w-3 h-3 bg-primary rounded-full animate-bounce"></div>
          <div
            className="w-3 h-3 bg-secondary rounded-full animate-bounce"
            style={{ animationDelay: "0.1s" }}
          ></div>
          <div
            className="w-3 h-3 bg-accent rounded-full animate-bounce"
            style={{ animationDelay: "0.2s" }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;

