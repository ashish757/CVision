import { FileText, Upload, TrendingUp, Check, LucideScanEye, Clock, CheckCircle2} from "lucide-react";
import { Link } from "react-router-dom";
import StatCard from "../components/StatCard.tsx";
import {useSelector} from "react-redux";
import type {RootState} from "../redux/store.ts";
import SideBar from "../components/SideBar.tsx";
import { useListResumesQuery } from "../redux/resume/resumeApi.ts";


const Dashboard = () => {

  const user = useSelector((state: RootState) => state.auth.user);

  // Fetch recent resumes
  const { data: resumesData, isLoading: isLoadingResumes } = useListResumesQuery({ page: 1, limit: 5 });
  const recentResumes = resumesData?.data?.resumes || [];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'DONE': return 'text-success';
      case 'PROCESSING': return 'text-warning';
      case 'ERROR': return 'text-error';
      default: return 'text-muted';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'DONE': return <CheckCircle2 className="w-4 h-4" />;
      case 'PROCESSING': return <Clock className="w-4 h-4" />;
      case 'ERROR': return <LucideScanEye className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <SideBar />

      {/* Main Content */}
      <main className="ml-64 p-8">
        <h1 className="text-3xl font-bold text-text mb-4">Dashboard</h1>

        {/* Header */}
        <div className="flex items-center justify-between mb-8 bg-linear-to-r from-primary to-accent rounded-lg p-5">
          <div>
            <h1 className="text-3xl font-bold text-white">Good Morning,  {user?.name || "User"}!</h1>
            <p className="text-gray-100 mt-1">
              Welcome back,  What would you like to do today?
            </p>
          </div>

        </div>


        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title={"Total Analysis"} num={"4"} Icon={Check} />
          <StatCard title={"CVs  Analysed"} num={"56"} Icon={FileText} />
          <StatCard title="Improvement" num="+12%" Icon={TrendingUp} />
        </div>


        {/* Action buttons*/}
        <h1 className="text-2xl text-text mb-4">Quick Actions</h1>
        <div className="flex items-center space-x-4 mb-8">
          <Link
            to="/analyse"
            className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center space-x-2"
          >
            <Upload className="w-5 h-5" />
            <span>Start New Analysis</span>
          </Link>

          <Link
            to="/analytics"
            className="bg-secondary hover:bg-secondary/90 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center space-x-2"
          >
            <LucideScanEye className="w-5 h-5" />
            <span>View Analytics</span>
          </Link>
        </div>

        {/* Recent Analyses */}
        <div className="mb-8">
          <h2 className="text-2xl text-text mb-4">Recent Analyses</h2>

          {isLoadingResumes ? (
            <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20">
              <div className="animate-pulse">
                <div className="h-4 bg-muted/20 rounded w-1/4 mb-4"></div>
                <div className="space-y-3">
                  <div className="h-3 bg-muted/20 rounded w-full"></div>
                  <div className="h-3 bg-muted/20 rounded w-3/4"></div>
                  <div className="h-3 bg-muted/20 rounded w-1/2"></div>
                </div>
              </div>
            </div>
          ) : recentResumes.length > 0 ? (
            <div className="bg-card/80 backdrop-blur-lg rounded-2xl border border-primary/20 overflow-hidden">
              <div className="p-6">
                <div className="space-y-4">
                  {recentResumes.map((resume) => (
                    <div
                      key={resume.id}
                      className="flex items-center justify-between p-4 bg-card/50 rounded-lg border border-primary/10 hover:border-primary/20 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                          <FileText className="w-5 h-5 text-primary" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-text truncate">
                            {resume.filename}
                          </p>
                          <p className="text-xs text-muted">
                            Uploaded {formatDate(resume.uploadedAt)}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        {resume.score && (
                          <div className="text-right">
                            <div className="text-sm font-medium text-text">
                              {resume.score}/100
                            </div>
                            <div className="text-xs text-muted">Score</div>
                          </div>
                        )}

                        <div className={`flex items-center space-x-1 text-xs ${getStatusColor(resume.status)}`}>
                          {getStatusIcon(resume.status)}
                          <span className="capitalize">{resume.status.toLowerCase()}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="px-6 py-3 bg-primary/5 border-t border-primary/10">
                <Link
                  to="/analytics"
                  className="text-primary hover:text-primary/80 text-sm font-medium"
                >
                  View all analyses →
                </Link>
              </div>
            </div>
          ) : (
            <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20 text-center">
              <div className="w-16 h-16 bg-muted/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-muted" />
              </div>
              <h3 className="text-lg font-medium text-text mb-2">No analyses yet</h3>
              <p className="text-muted mb-6">Start your first CV analysis to see results here.</p>
              <Link
                to="/analyse"
                className="inline-flex items-center space-x-2 bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg font-medium transition-colors"
              >
                <Upload className="w-5 h-5" />
                <span>Start Analysis</span>
              </Link>
            </div>
          )}
        </div>

      </main>

    </div>
  );

};

export default Dashboard;

