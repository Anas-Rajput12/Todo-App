import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  centered?: boolean;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  centered = false,
  text
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  const spinnerClass = `${sizeClasses[size]} animate-spin rounded-full border-2 border-current border-t-transparent text-indigo-600`;

  const containerClass = centered
    ? 'flex flex-col items-center justify-center'
    : 'inline-block';

  return (
    <div className={containerClass}>
      <div className={spinnerClass} role="status">
        <span className="sr-only">Loading...</span>
      </div>
      {text && (
        <p className="mt-2 text-sm text-gray-500">{text}</p>
      )}
    </div>
  );
};

export default LoadingSpinner;