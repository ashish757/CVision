import React, { useCallback, useState } from 'react';
import { Upload, X, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { validateResumeFile, formatFileSize } from '../utils/validation';

interface FileUploadProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
  error?: string;
  disabled?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  selectedFile,
  error,
  disabled = false
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [validationError, setValidationError] = useState<string>('');

  const handleFile = useCallback((file: File) => {
    const validation = validateResumeFile(file);

    if (!validation.isValid) {
      setValidationError(validation.error || 'Invalid file');
      onFileSelect(null);
      return;
    }

    setValidationError('');
    onFileSelect(file);
  }, [onFileSelect]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  }, [handleFile, disabled]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      setDragActive(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();

    if (disabled) return;

    const files = e.target.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  }, [handleFile, disabled]);

  const removeFile = useCallback(() => {
    onFileSelect(null);
    setValidationError('');
  }, [onFileSelect]);

  const displayError = error || validationError;

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      {!selectedFile && (
        <div
          className={`
            file-upload-container
            relative border-2 border-dashed rounded-lg p-8 text-center transition-all
            ${dragActive && !disabled ? 'file-upload-drag-active' : ''}
            ${displayError ? 'file-upload-error' : ''}
            ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-primary/50'}
          `}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <input
            type="file"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
            onChange={handleFileInput}
            accept=".pdf,.doc,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword"
            disabled={disabled}
          />

          <div className="space-y-4">
            <div className={`mx-auto w-12 h-12 rounded-lg flex items-center justify-center ${
              displayError ? 'bg-error/10' : 'bg-primary/10'
            }`}>
              {displayError ? (
                <AlertCircle className={`w-6 h-6 ${displayError ? 'text-error' : 'text-primary'}`} />
              ) : (
                <Upload className="w-6 h-6 text-primary" />
              )}
            </div>

            <div>
              <p className="text-lg font-medium text-text">
                {displayError ? 'Upload Error' : 'Upload your resume'}
              </p>
              <p className="text-sm text-muted mt-1">
                {displayError ? displayError : 'Drag and drop your file here, or click to browse'}
              </p>
              <p className="text-xs text-muted mt-2">
                Supports PDF and DOCX files up to 5MB
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Selected File Display */}
      {selectedFile && (
        <div className="bg-card border border-border rounded-lg p-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-success" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-text truncate">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-muted">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>

            <button
              onClick={removeFile}
              disabled={disabled}
              className="p-1 text-muted hover:text-error transition-colors disabled:opacity-50"
              aria-label="Remove file"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="mt-3 flex items-center space-x-2 text-xs text-success">
            <CheckCircle className="w-3 h-3" />
            <span>File selected successfully</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
