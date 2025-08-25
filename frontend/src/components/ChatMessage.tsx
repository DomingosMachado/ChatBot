import { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
  isLast?: boolean;
}

export default function ChatMessage({ message, isLast }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div 
      className={`mb-3 sm:mb-4 flex ${isUser ? 'justify-end' : 'justify-start'}`}
      role="article"
      aria-label={`${isUser ? 'User' : 'Assistant'} message`}
    >
      <div 
        className={`
          p-3 sm:p-4 rounded-2xl sm:rounded-3xl max-w-[85%] sm:max-w-[80%] 
          whitespace-pre-wrap shadow-sm text-sm sm:text-base leading-relaxed
          ${isUser 
            ? 'bg-blue-500 text-white ml-auto' 
            : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100 mr-auto'
          }
          ${isLast && !isUser ? 'animate-pulse' : ''}
        `}
      >
        <p className="break-words">{message.content}</p>
      </div>
    </div>
  );
}