import React from 'react';
import { Loader2, CheckCircle, AlertCircle, Clock } from 'lucide-react';
import type { ResumeStatus } from '../redux/resume/resumeApi';

interface UploadProgressProps {
  status: 'uploading' | ResumeStatus;
  filename?: string;
  progress?: number;
  error?: string;
}

const UploadProgress: React.FC<UploadProgressProps> = ({
  status,
  filename,
  progress = 0,
  error
}) => {
  console.log('UploadProgress render:', { status, filename, progress, error });

  const getStatusConfig = () => {
    switch (status) {
      case 'uploading':
        return {
          icon: <Loader2 className="w-6 h-6 animate-spin text-primary" />,
          title: 'Uploading',
          description: 'Sending your resume to the server...',
          bgColor: 'bg-primary/10',
          borderColor: 'border-primary/20',
          showProgress: true,
        };
      case 'UPLOADED':
        return {
          icon: <Clock className="w-6 h-6 text-warning" />,
          title: 'Queued',
          description: 'Your resume is in the processing queue...',
          bgColor: 'bg-warning/10',
          borderColor: 'border-warning/20',
          showProgress: false,
        };
      case 'PROCESSING':
        return {
          icon: <Loader2 className="w-6 h-6 animate-spin text-info" />,
          title: 'Processing',
          description: 'AI is analyzing your resume...',
          bgColor: 'bg-info/10',
          borderColor: 'border-info/20',
          showProgress: false,
        };
      case 'DONE':
        return {
          icon: <CheckCircle className="w-6 h-6 text-success" />,
          title: 'Complete',
          description: 'Analysis completed successfully!',
          bgColor: 'bg-success/10',
          borderColor: 'border-success/20',
          showProgress: false,
        };
      case 'ERROR':
        return {
          icon: <AlertCircle className="w-6 h-6 text-error" />,
          title: 'Error',
          description: error || 'An error occurred during processing',
          bgColor: 'bg-error/10',
          borderColor: 'border-error/20',
          showProgress: false,
        };
      default:
        return {
          icon: <Clock className="w-6 h-6 text-muted" />,
          title: 'Unknown',
          description: 'Status unknown',
          bgColor: 'bg-muted/10',
          borderColor: 'border-muted/20',
          showProgress: false,
        };
    }
  };

  const config = getStatusConfig();

  return (
    <div className={`${config.bgColor} border ${config.borderColor} rounded-lg p-6`}>
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          {config.icon}
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-medium text-text mb-1">
            {config.title}
          </h3>

          {filename && (
            <p className="text-sm text-muted mb-2 truncate">
              {filename}
            </p>
          )}

          <p className="text-sm text-muted">
            {config.description}
          </p>

          {config.showProgress && (
            <div className="mt-4">
              <div className="flex items-center justify-between text-xs text-muted mb-2">
                <span>Progress</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}

          {status === 'PROCESSING' && (
            <div className="mt-4">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-info rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-info rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-info rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadProgress;
