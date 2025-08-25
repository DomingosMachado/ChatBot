import { Conversation } from '../types/chat';

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onClick: () => void;
  onDelete: () => void;
}

export default function ConversationItem({ conversation, isActive, onClick, onDelete }: ConversationItemProps) {
  const lastMessage = conversation.messages[conversation.messages.length - 1];
  const lastMessagePreview = lastMessage ?
    (lastMessage.content.slice(0, 60) + (lastMessage.content.length > 60 ? '...' : '')) :
    'Nenhuma mensagem ainda';

  const formatTimestamp = (timestamp: number): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString([], { weekday: 'short' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Excluir esta conversa?')) {
      onDelete();
    }
  };

  return (
    <div
      onClick={ onClick }
      className={ `
        group p-3 rounded-lg cursor-pointer transition-colors relative
        ${isActive
          ? 'bg-blue-100 dark:bg-blue-900/30 border-l-2 border-blue-500'
          : 'hover:bg-gray-100 dark:hover:bg-gray-800'
        }
      `}
    >
      <div className="flex justify-between items-start mb-1">
        <h3 className={ `
          font-medium text-sm truncate pr-2
          ${isActive ? 'text-blue-700 dark:text-blue-300' : 'text-gray-800 dark:text-gray-200'}
        `}>
          { conversation.title }
        </h3>
        <button
          onClick={ handleDelete }
          className="opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-red-500 text-xs p-1"
          aria-label="Excluir conversa"
        >
          ✕
        </button>
      </div>

      <p className="text-xs text-gray-600 dark:text-gray-400 mb-2 line-clamp-2">
        { lastMessagePreview }
      </p>

      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500 dark:text-gray-500">
          { formatTimestamp(conversation.lastUpdated) }
        </span>
        { conversation.messages.length > 0 && (
          <span className="text-xs bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 px-2 py-1 rounded-full">
            { conversation.messages.length }
          </span>
        ) }
      </div>
    </div>
  );
}