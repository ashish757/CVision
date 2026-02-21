import { useState, useCallback } from 'react';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import SideBar from "../components/SideBar.tsx";
import FileUpload from "../components/FileUpload.tsx";
import UploadProgress from "../components/UploadProgress.tsx";
import ResumeResults from "../components/ResumeResults.tsx";
import { useUploadResumeMutation } from "../redux/resume/resumeApi";
import { useResumePolling } from "../hooks/useResumePolling";
import type { ResumeStatus } from '../redux/resume/resumeApi';
import type { ApiError } from '../utils/Types';

const Analyse = () => {
    // State management
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadError, setUploadError] = useState<string>('');
    const [currentResumeId, setCurrentResumeId] = useState<string | null>(null);
    const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading'>('idle');
    const [uploadProgress, setUploadProgress] = useState<number>(0);

    // RTK Query mutation
    const [uploadResume, { isLoading: isUploadingMutation }] = useUploadResumeMutation();

    // Polling hook for status updates
    const {
        data: resumeData,
        status: resumeStatus,
        error: pollingError,
        refetch: refetchStatus,
    } = useResumePolling({
        resumeId: currentResumeId,
        enabled: !!currentResumeId,
        onStatusChange: (status) => {
            console.log('Resume status changed:', status);
        },
        onComplete: (data) => {
            console.log('Resume processing completed:', data);
        },
        onError: (error) => {
            console.error('Resume processing error:', error);
            setUploadError(typeof error === 'string' ? error : 'Processing failed');
        },
    });

    // Convert error to string for display
    const pollingErrorMessage = typeof pollingError === 'string'
        ? pollingError
        : pollingError && 'data' in pollingError && pollingError.data
          ? (pollingError.data as any)?.message || 'An error occurred'
          : 'An error occurred';

    // File selection handler
    const handleFileSelect = useCallback((file: File | null) => {
        setSelectedFile(file);
        setUploadError('');
    }, []);

    // Upload handler
    const handleUpload = useCallback(async () => {
        if (!selectedFile) {
            setUploadError('Please select a file first');
            return;
        }

        setUploadError('');
        setUploadStatus('uploading');
        setUploadProgress(0);

        try {
            // Create FormData
            const formData = new FormData();
            formData.append('file', selectedFile);

            console.log('Starting upload for file:', selectedFile.name);

            // Simulate upload progress
            const progressInterval = setInterval(() => {
                setUploadProgress((prev) => {
                    const newProgress = prev + 10;
                    if (newProgress >= 90) {
                        clearInterval(progressInterval);
                        return 90;
                    }
                    return newProgress;
                });
            }, 200);

            // Upload file
            const result = await uploadResume(formData).unwrap();
            console.log('Upload successful:', result);

            // Complete progress
            clearInterval(progressInterval);
            setUploadProgress(100);

            // Set resume ID to start polling
            if (result?.data?.resumeId) {
                setCurrentResumeId(result.data.resumeId);
                console.log('Starting polling for resume ID:', result.data.resumeId);
            } else {
                throw new Error('No resume ID returned from server');
            }

            setUploadStatus('idle');

        } catch (error) {
            console.error('Upload error:', error);
            setUploadStatus('idle');
            setUploadProgress(0);

            const apiError = error as ApiError;
            const errorMessage = apiError?.data?.message || 'Upload failed. Please try again.';
            setUploadError(errorMessage);
            console.error('Upload failed:', errorMessage);
        }
    }, [selectedFile, uploadResume]);

    // Reset handler
    const handleReset = useCallback(() => {
        setSelectedFile(null);
        setUploadError('');
        setCurrentResumeId(null);
        setUploadStatus('idle');
        setUploadProgress(0);
    }, []);

    // View details handler (placeholder)
    const handleViewDetails = useCallback(() => {
        // Navigate to detailed analysis page
        console.log('View details for resume:', currentResumeId);
    }, [currentResumeId]);

    // Download report handler (placeholder)
    const handleDownloadReport = useCallback(() => {
        // Download analysis report
        console.log('Download report for resume:', currentResumeId);
    }, [currentResumeId]);

    // Determine current view
    const isUploading = uploadStatus === 'uploading' || isUploadingMutation;
    const hasResumeId = !!currentResumeId;
    const isPolling = hasResumeId && ['UPLOADED', 'PROCESSING'].includes(resumeStatus || '');
    const isComplete = resumeStatus === 'DONE' && resumeData;
    const hasError = !!uploadError || !!pollingError || resumeStatus === 'ERROR';

    const showResults = isComplete;
    const showProgress = isUploading || isPolling;
    const showUpload = !showProgress && !showResults;

    console.log('Current state:', {
        uploadStatus,
        currentResumeId,
        resumeStatus,
        isUploading,
        hasResumeId,
        isPolling,
        isComplete,
        showResults,
        showProgress,
        showUpload,
        hasError
    });

    return (
        <div className="min-h-screen bg-background">
            {/* Sidebar */}
            <SideBar />

            {/* Main Content */}
            <main className="ml-64 p-8">
                <div className="max-w-4xl mx-auto">
                    {/* Header */}
                    <div className="mb-8">
                        <div className="flex items-center space-x-4 mb-4">
                            {(showProgress || showResults) && (
                                <button
                                    onClick={handleReset}
                                    className="p-2 text-muted hover:text-primary rounded-lg hover:bg-primary/10 transition-all"
                                    aria-label="Start new analysis"
                                >
                                    <ArrowLeft className="w-5 h-5" />
                                </button>
                            )}
                            <h1 className="text-3xl font-bold text-text">CV Analysis</h1>
                        </div>

                        <p className="text-muted">
                            {showUpload && "Upload your resume to get AI-powered insights and scoring"}
                            {showProgress && "Your resume is being analyzed..."}
                            {showResults && "Analysis complete! Review your results below."}
                        </p>
                    </div>

                    {/* Upload Section */}
                    {showUpload && (
                        <div className="space-y-6">
                            {/* File Upload */}
                            <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20">
                                <h2 className="text-xl font-semibold text-text mb-6">
                                    Upload Resume
                                </h2>

                                <FileUpload
                                    onFileSelect={handleFileSelect}
                                    selectedFile={selectedFile}
                                    error={uploadError}
                                    disabled={isUploadingMutation}
                                />

                                {selectedFile && !uploadError && (
                                    <div className="mt-6 pt-6 border-t border-border">
                                        <button
                                            onClick={handleUpload}
                                            disabled={isUploading || !selectedFile}
                                            className="w-full bg-primary hover:bg-primary/90 disabled:bg-primary/50 disabled:cursor-not-allowed text-background py-3 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                                        >
                                            {isUploading ? (
                                                <>
                                                    <RefreshCw className="w-5 h-5 animate-spin" />
                                                    <span>Uploading...</span>
                                                </>
                                            ) : (
                                                <span>Start Analysis</span>
                                            )}
                                        </button>
                                    </div>
                                )}
                            </div>

                            {/* Info Cards */}
                            <div className="grid md:grid-cols-3 gap-6">
                                <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 border border-primary/10">
                                    <h3 className="font-medium text-text mb-2">Fast Processing</h3>
                                    <p className="text-sm text-muted">Get results in under 2 minutes</p>
                                </div>

                                <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 border border-primary/10">
                                    <h3 className="font-medium text-text mb-2">AI-Powered</h3>
                                    <p className="text-sm text-muted">Advanced machine learning analysis</p>
                                </div>

                                <div className="bg-card/50 backdrop-blur-sm rounded-xl p-6 border border-primary/10">
                                    <h3 className="font-medium text-text mb-2">Detailed Insights</h3>
                                    <p className="text-sm text-muted">Score, skills, and recommendations</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Progress Section */}
                    {showProgress && (
                        <div className="space-y-6">
                            <UploadProgress
                                status={uploadStatus === 'uploading' ? 'uploading' : (resumeStatus as ResumeStatus)}
                                filename={selectedFile?.name}
                                progress={uploadProgress}
                                error={uploadError || pollingErrorMessage}
                            />

                            {pollingError && (
                                <div className="bg-error/10 border border-error/30 rounded-lg p-4">
                                    <p className="text-error text-sm mb-3">
                                        {pollingErrorMessage}
                                    </p>
                                    <button
                                        onClick={refetchStatus}
                                        className="text-primary hover:text-primary/80 text-sm font-medium"
                                    >
                                        Retry
                                    </button>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Results Section */}
                    {showResults && resumeData && (
                        <div className="space-y-6">
                            <ResumeResults
                                filename={selectedFile?.name || 'Unknown file'}
                                score={resumeData.score || 0}
                                extractedSkills={resumeData.extractedSkills}
                                ranking={resumeData.ranking}
                                processedAt={resumeData.processedAt || new Date().toISOString()}
                                onViewDetails={handleViewDetails}
                                onDownloadReport={handleDownloadReport}
                            />
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default Analyse;