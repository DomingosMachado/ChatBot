export interface AgentWorkflow {
  agent: string;
  decision: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  agent_workflow?: AgentWorkflow[];
}

export interface Conversation {
  conversation_id: string;
  title: string;
  messages: Message[];
  lastUpdated: number;
}