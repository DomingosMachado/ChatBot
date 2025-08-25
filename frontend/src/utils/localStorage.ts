import { Conversation, Message } from '../types/chat';

const CONVERSATIONS_KEY = 'cloudwalk_conversations';
const USER_ID_KEY = 'cloudwalk_user_id';

export const generateId = (): string => {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
};

export const getUserId = (): string => {
  let userId = localStorage.getItem(USER_ID_KEY);
  if (!userId) {
    userId = generateId();
    localStorage.setItem(USER_ID_KEY, userId);
  }
  return userId;
};

export const getConversations = (): Conversation[] => {
  try {
    const stored = localStorage.getItem(CONVERSATIONS_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

export const saveConversation = (conversation: Conversation): void => {
  const conversations = getConversations();
  const existingIndex = conversations.findIndex(c => c.conversation_id === conversation.conversation_id);
  
  if (existingIndex >= 0) {
    conversations[existingIndex] = conversation;
  } else {
    conversations.unshift(conversation);
  }
  
  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(conversations));
};

export const getConversation = (conversationId: string): Conversation | null => {
  const conversations = getConversations();
  return conversations.find(c => c.conversation_id === conversationId) || null;
};

export const deleteConversation = (conversationId: string): void => {
  const conversations = getConversations();
  const filtered = conversations.filter(c => c.conversation_id !== conversationId);
  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(filtered));
};

export const createNewConversation = (): Conversation => {
  return {
    conversation_id: generateId(),
    title: 'New Conversation',
    messages: [],
    lastUpdated: Date.now()
  };
};

export const updateConversationTitle = (conversationId: string, firstMessage: string): void => {
  const conversations = getConversations();
  const conversation = conversations.find(c => c.conversation_id === conversationId);
  
  if (conversation && conversation.title === 'New Conversation') {
    conversation.title = firstMessage.slice(0, 50) + (firstMessage.length > 50 ? '...' : '');
    localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(conversations));
  }
};