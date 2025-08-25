import { Conversation } from '../types/chat';
import ConversationItem from './ConversationItem';
import { createNewConversation, deleteConversation } from '../utils/localStorage';

interface ConversationListProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
  onNewConversation: () => void;
  onDeleteConversation: (conversationId: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export default function ConversationList({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  isOpen,
  onClose
}: ConversationListProps) {
  const handleNewConversation = () => {
    onNewConversation();
    onClose(); // Close mobile sidebar after creating new conversation
  };

  return (
    <>
      {/* Mobile overlay */ }
      { isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={ onClose }
        />
      ) }

      {/* Sidebar */ }
      <div className={ `
        fixed left-0 top-0 h-full w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 z-50
        transform transition-transform duration-300 ease-in-out
        lg:relative lg:translate-x-0 lg:z-auto
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Header */ }
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
              Conversations
            </h2>
            <button
              onClick={ onClose }
              className="lg:hidden text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              aria-label="Close sidebar"
            >
              ✕
            </button>
          </div>

          <button
            onClick={ handleNewConversation }
            className="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <span className="text-lg">+</span>
            New Conversation
          </button>
        </div>

        {/* Conversations List */ }
        <div className="flex-1 overflow-y-auto p-2">
          { conversations.length === 0 ? (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400">
              <div className="text-4xl mb-2">💬</div>
              <p className="text-sm">No conversations yet</p>
              <p className="text-xs mt-1">Start a new conversation to get started!</p>
            </div>
          ) : (
            <div className="space-y-1">
              { conversations.map((conversation) => (
                <ConversationItem
                  key={ conversation.conversation_id }
                  conversation={ conversation }
                  isActive={ conversation.conversation_id === activeConversationId }
                  onClick={ () => {
                    onSelectConversation(conversation.conversation_id);
                    onClose(); // Close mobile sidebar when selecting conversation
                  } }
                  onDelete={ () => onDeleteConversation(conversation.conversation_id) }
                />
              )) }
            </div>
          ) }
        </div>

        {/* Footer */ }
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
            CloudWalk AI Chat Assistant
          </div>
        </div>
      </div>
    </>
  );
}