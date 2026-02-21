import { useEffect, useRef } from 'react';
import { useGetResumeStatusQuery } from '../redux/resume/resumeApi';
import type { ResumeStatus } from '../redux/resume/resumeApi';

interface UseResumePollingOptions {
  resumeId: string | null;
  enabled?: boolean;
  pollingInterval?: number;
  onStatusChange?: (status: ResumeStatus) => void;
  onComplete?: (data: any) => void;
  onError?: (error: any) => void;
}

/**
 * Custom hook for polling resume processing status
 */
export const useResumePolling = ({
  resumeId,
  enabled = true,
  pollingInterval = 2000, // 2 seconds default
  onStatusChange,
  onComplete,
  onError,
}: UseResumePollingOptions) => {
  const prevStatusRef = useRef<ResumeStatus | null>(null);

  // Get current status first to determine if we should poll
  const statusQuery = useGetResumeStatusQuery(
    resumeId!,
    {
      skip: !resumeId || !enabled,
      refetchOnMountOrArgChange: true,
    }
  );

  const currentStatus = statusQuery.data?.data?.status;
  const shouldPoll = currentStatus && !['DONE', 'ERROR'].includes(currentStatus);

  const {
    data,
    error,
    isLoading,
    isError,
    refetch,
  } = useGetResumeStatusQuery(
    resumeId!,
    {
      skip: !resumeId || !enabled,
      pollingInterval: shouldPoll ? pollingInterval : 0,
      skipPollingIfUnfocused: true,
      refetchOnMountOrArgChange: true,
    }
  );

  const status = data?.data?.status;
  const isProcessing = status && !['DONE', 'ERROR'].includes(status);

  console.log('Polling status:', { resumeId, status, enabled, pollingInterval, isProcessing, shouldPoll });

  // Handle status changes
  useEffect(() => {
    if (status && status !== prevStatusRef.current) {
      console.log(`Status changed from ${prevStatusRef.current} to ${status}`);
      prevStatusRef.current = status;
      onStatusChange?.(status);

      if (status === 'DONE') {
        console.log('Processing completed:', data);
        onComplete?.(data);
      } else if (status === 'ERROR') {
        const errorMessage = data?.data?.errorMessage || 'Processing failed';
        console.log('Processing error:', errorMessage);
        onError?.(errorMessage);
      }
    }
  }, [status, data, onStatusChange, onComplete, onError]);

  // Handle API errors
  useEffect(() => {
    if (isError && error) {
      console.error('API error in polling:', error);
      onError?.(error);
    }
  }, [isError, error, onError]);


  return {
    data: data?.data,
    status,
    error: error || data?.data?.errorMessage,
    isLoading,
    isError,
    isProcessing,
    refetch,
  };
};
