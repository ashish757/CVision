import React from 'react';
import { Trophy, Target, Tag, Download, Eye } from 'lucide-react';

interface ResumeResultsProps {
  filename: string;
  score: number;
  extractedSkills?: string[];
  ranking?: {
    position: number;
    totalCandidates: number;
  };
  processedAt: string;
  onViewDetails?: () => void;
  onDownloadReport?: () => void;
}

const ResumeResults: React.FC<ResumeResultsProps> = ({
  filename,
  score,
  extractedSkills = [],
  ranking,
  processedAt,
  onViewDetails,
  onDownloadReport,
}) => {
  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'text-success';
    if (score >= 60) return 'text-warning';
    return 'text-error';
  };

  const getScoreBgColor = (score: number): string => {
    if (score >= 80) return 'bg-success/10';
    if (score >= 60) return 'bg-warning/10';
    return 'bg-error/10';
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getRankingText = (position: number, total: number): string => {
    const percentage = ((total - position + 1) / total) * 100;
    return `Top ${Math.round(percentage)}%`;
  };

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-semibold text-text mb-1">Analysis Complete</h2>
            <p className="text-sm text-muted">{filename}</p>
            <p className="text-xs text-muted">Processed on {formatDate(processedAt)}</p>
          </div>

          <div className={`${getScoreBgColor(score)} px-4 py-2 rounded-lg text-center`}>
            <div className={`text-2xl font-bold ${getScoreColor(score)}`}>
              {score}
            </div>
            <div className="text-xs text-muted">Score</div>
          </div>
        </div>
      </div>

      {/* Score & Ranking Section */}
      <div className="p-6 space-y-6">
        {/* Score Breakdown */}
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-medium text-text">Overall Score</h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted">Resume Quality</span>
              <span className={`font-medium ${getScoreColor(score)}`}>{score}/100</span>
            </div>

            <div className="w-full bg-border rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ease-out ${
                  score >= 80 ? 'bg-success' : score >= 60 ? 'bg-warning' : 'bg-error'
                }`}
                style={{ width: `${score}%` }}
              />
            </div>

            <div className="text-xs text-muted">
              {score >= 80
                ? 'Excellent! Your resume stands out.'
                : score >= 60
                  ? 'Good! Some areas for improvement.'
                  : 'Needs improvement. Consider our recommendations.'
              }
            </div>
          </div>
        </div>

        {/* Ranking Section */}
        {ranking && (
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Trophy className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-medium text-text">Ranking</h3>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-primary/10 rounded-lg p-4">
                <div className="text-xl font-bold text-primary">#{ranking.position}</div>
                <div className="text-xs text-muted">Position</div>
              </div>

              <div className="bg-info/10 rounded-lg p-4">
                <div className="text-xl font-bold text-info">{getRankingText(ranking.position, ranking.totalCandidates)}</div>
                <div className="text-xs text-muted">Percentile</div>
              </div>

              <div className="bg-accent/10 rounded-lg p-4">
                <div className="text-xl font-bold text-accent">{ranking.totalCandidates}</div>
                <div className="text-xs text-muted">Total</div>
              </div>
            </div>
          </div>
        )}

        {/* Skills Section */}
        {extractedSkills.length > 0 && (
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Tag className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-medium text-text">Extracted Skills</h3>
              <span className="bg-primary/10 text-primary text-xs px-2 py-1 rounded-full">
                {extractedSkills.length} found
              </span>
            </div>

            <div className="flex flex-wrap gap-2">
              {extractedSkills.slice(0, 12).map((skill, index) => (
                <span
                  key={index}
                  className="bg-card border border-border px-3 py-1 rounded-full text-sm text-text hover:border-primary/50 transition-colors"
                >
                  {skill}
                </span>
              ))}

              {extractedSkills.length > 12 && (
                <span className="bg-muted/10 text-muted px-3 py-1 rounded-full text-sm">
                  +{extractedSkills.length - 12} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-3 pt-4 border-t border-border">
          {onViewDetails && (
            <button
              onClick={onViewDetails}
              className="flex-1 bg-primary hover:bg-primary/90 text-background px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
            >
              <Eye className="w-4 h-4" />
              <span>View Details</span>
            </button>
          )}

          {onDownloadReport && (
            <button
              onClick={onDownloadReport}
              className="flex-1 bg-card border border-border hover:border-primary/50 text-text px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeResults;
