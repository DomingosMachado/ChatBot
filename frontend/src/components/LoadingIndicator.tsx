interface LoadingIndicatorProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingIndicator({ 
  message = "Typing...", 
  size = 'md' 
}: LoadingIndicatorProps) {
  const sizeClasses = {
    sm: 'text-xs sm:text-sm p-2 sm:p-3',
    md: 'text-sm sm:text-base p-3 sm:p-4',
    lg: 'text-base sm:text-lg p-4 sm:p-5'
  };

  return (
    <div className="mb-3 sm:mb-4 flex justify-start" role="status" aria-live="polite">
      <div className={`
        ${sizeClasses[size]}
        rounded-2xl sm:rounded-3xl max-w-[85%] sm:max-w-[80%]
        bg-gray-100 dark:bg-gray-800 
        text-gray-600 dark:text-gray-400
        shadow-sm animate-pulse
        flex items-center gap-2 sm:gap-3
      `}>
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
        <span className="hidden sm:inline">{message}</span>
      </div>
    </div>
  );
}