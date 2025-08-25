import { KeyboardEvent, FormEvent } from 'react';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  loading: boolean;
  placeholder?: string;
}

export default function MessageInput({ 
  value, 
  onChange, 
  onSend, 
  loading, 
  placeholder = "Type your message..." 
}: MessageInputProps) {
  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSend();
  };

  return (
    <form 
      onSubmit={handleSubmit}
      className="flex gap-2 sm:gap-3 p-3 sm:p-4 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-t border-gray-200 dark:border-gray-700"
      role="search"
      aria-label="Message input"
    >
      <label htmlFor="message-input" className="sr-only">
        Message input
      </label>
      <input
        id="message-input"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={handleKeyPress}
        className="
          flex-1 p-3 sm:p-4 rounded-2xl text-sm sm:text-base
          border-2 border-gray-200 dark:border-gray-600
          bg-white dark:bg-gray-800 
          text-gray-800 dark:text-gray-200
          placeholder-gray-500 dark:placeholder-gray-400
          focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20
          disabled:opacity-60 disabled:cursor-not-allowed
          transition-colors duration-200
        "
        placeholder={placeholder}
        disabled={loading}
        autoComplete="off"
        aria-describedby="send-button"
      />
      <button 
        id="send-button"
        type="submit"
        className="
          px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-sm sm:text-base font-medium
          bg-blue-500 hover:bg-blue-600 active:bg-blue-700
          text-white shadow-lg hover:shadow-xl
          disabled:bg-blue-300 disabled:cursor-not-allowed disabled:shadow-none
          transform hover:scale-105 active:scale-95
          transition-all duration-200
          focus:outline-none focus:ring-2 focus:ring-blue-500/50
        " 
        disabled={loading || !value.trim()}
        aria-label={loading ? "Sending message..." : "Send message"}
      >
        {loading ? (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            <span className="hidden sm:inline">Sending...</span>
          </div>
        ) : (
          <span>Send</span>
        )}
      </button>
    </form>
  );
}