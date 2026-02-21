import { FileText, TrendingUp, Clock, CheckCircle2, AlertCircle } from "lucide-react";
import SideBar from "../components/SideBar.tsx";
import { useListResumesQuery } from "../redux/resume/resumeApi.ts";
import StatCard from "../components/StatCard.tsx";

const Analytics = () => {
    const { data: resumesData, isLoading } = useListResumesQuery({ page: 1, limit: 50 });
    const resumes = resumesData?.data?.resumes || [];

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
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
            case 'ERROR': return <AlertCircle className="w-4 h-4" />;
            default: return <Clock className="w-4 h-4" />;
        }
    };

    // Calculate analytics
    const totalAnalyses = resumes.length;
    const completedAnalyses = resumes.filter(r => r.status === 'DONE').length;
    const averageScore = completedAnalyses > 0
        ? Math.round(resumes.filter(r => r.score).reduce((acc, r) => acc + (r.score || 0), 0) / completedAnalyses)
        : 0;
    const improvementRate = "+12%"; // Placeholder for improvement calculation

    return (
        <div className="min-h-screen bg-background">
            {/* Sidebar */}
            <SideBar />

            {/* Main Content */}
            <main className="ml-64 p-8">
                <h1 className="text-3xl font-bold text-text mb-4">Analytics</h1>
                <p className="text-muted mb-8">Detailed analytics of your CV analyses and performance insights.</p>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <StatCard title="Total Analyses" num={totalAnalyses.toString()} Icon={FileText} />
                    <StatCard title="Completed" num={completedAnalyses.toString()} Icon={CheckCircle2} />
                    <StatCard title="Average Score" num={`${averageScore}/100`} Icon={TrendingUp} />
                    <StatCard title="Improvement" num={improvementRate} Icon={TrendingUp} />
                </div>

                {/* Recent Analyses Table */}
                <div className="bg-card/80 backdrop-blur-lg rounded-2xl border border-primary/20 overflow-hidden">
                    <div className="p-6">
                        <h2 className="text-xl font-semibold text-text mb-6">All Analyses</h2>

                        {isLoading ? (
                            <div className="animate-pulse space-y-4">
                                {[...Array(5)].map((_, i) => (
                                    <div key={i} className="flex items-center space-x-4 p-4 border border-border rounded-lg">
                                        <div className="w-10 h-10 bg-muted/20 rounded-lg"></div>
                                        <div className="flex-1 space-y-2">
                                            <div className="h-4 bg-muted/20 rounded w-3/4"></div>
                                            <div className="h-3 bg-muted/20 rounded w-1/2"></div>
                                        </div>
                                        <div className="w-16 h-8 bg-muted/20 rounded"></div>
                                    </div>
                                ))}
                            </div>
                        ) : resumes.length > 0 ? (
                            <div className="space-y-3">
                                {resumes.map((resume) => (
                                    <div
                                        key={resume.id}
                                        className="flex items-center justify-between p-4 bg-card/50 rounded-lg border border-primary/10 hover:border-primary/20 transition-colors"
                                    >
                                        <div className="flex items-center space-x-4">
                                            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                                                <FileText className="w-5 h-5 text-primary" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-text">
                                                    {resume.filename}
                                                </p>
                                                <p className="text-xs text-muted">
                                                    Uploaded: {formatDate(resume.uploadedAt)}
                                                </p>
                                                {resume.processedAt && (
                                                    <p className="text-xs text-muted">
                                                        Processed: {formatDate(resume.processedAt)}
                                                    </p>
                                                )}
                                            </div>
                                        </div>

                                        <div className="flex items-center space-x-4">
                                            {resume.score && (
                                                <div className="text-center">
                                                    <div className="text-lg font-bold text-text">
                                                        {resume.score}
                                                    </div>
                                                    <div className="text-xs text-muted">Score</div>
                                                </div>
                                            )}

                                            <div className={`flex items-center space-x-1 text-sm ${getStatusColor(resume.status)}`}>
                                                {getStatusIcon(resume.status)}
                                                <span className="capitalize">{resume.status.toLowerCase()}</span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-12">
                                <div className="w-16 h-16 bg-muted/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                                    <FileText className="w-8 h-8 text-muted" />
                                </div>
                                <h3 className="text-lg font-medium text-text mb-2">No analyses yet</h3>
                                <p className="text-muted">Start your first CV analysis to see analytics here.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Analytics;