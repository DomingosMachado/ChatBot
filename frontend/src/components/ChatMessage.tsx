import { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
  isLast?: boolean;
}

const AgentIcon = ({ agent }: { agent: string }) => {
  const icons = {
    'RouterAgent': '🎯',
    'KnowledgeAgent': '📚',
    'MathAgent': '🔢'
  };
  return <span className="text-xs">{ icons[agent as keyof typeof icons] || '🤖' }</span>;
};

export default function ChatMessage({ message, isLast }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={ `mb-3 sm:mb-4 flex flex-col ${isUser ? 'items-end' : 'items-start'}` }
      role="article"
      aria-label={ `${isUser ? 'User' : 'Assistant'} message` }
    >
      <div
        className={ `
          p-3 sm:p-4 rounded-2xl sm:rounded-3xl max-w-[85%] sm:max-w-[80%] 
          whitespace-pre-wrap shadow-sm text-sm sm:text-base leading-relaxed
          ${isUser
            ? 'bg-blue-500 text-white ml-auto'
            : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100 mr-auto'
          }
          ${isLast && !isUser ? 'animate-pulse' : ''}
        `}
      >
        <p className="break-words">{ message.content }</p>
      </div>

      { !isUser && message.agent_workflow && message.agent_workflow.length > 0 && (
        <div className={ `mt-1 flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400 ${isUser ? 'mr-4' : 'ml-4'}` }>
          { message.agent_workflow.map((workflow, index) => (
            <div key={ index } className="flex items-center gap-1">
              { index > 0 && <span className="mx-1">→</span> }
              <div className="flex items-center gap-1 bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded-full">
                <AgentIcon agent={ workflow.agent } />
                <span className="font-medium">{ workflow.agent.replace('Agent', '') }</span>
              </div>
            </div>
          )) }
        </div>
      ) }
    </div>
  );
}