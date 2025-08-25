'use client';
import { useState, useEffect, useRef } from 'react';
import ChatMessage from '../components/ChatMessage';
import MessageInput from '../components/MessageInput';
import LoadingIndicator from '../components/LoadingIndicator';
import ConversationList from '../components/ConversationList';
import { Message, Conversation } from '../types/chat';
import {
  getUserId,
  getConversations,
  saveConversation,
  getConversation,
  deleteConversation,
  createNewConversation
} from '../utils/localStorage';

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [userId, setUserId] = useState<string>('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const id = getUserId();
    setUserId(id);
    const savedConversations = getConversations();
    setConversations(savedConversations);
    if (savedConversations.length === 0) {
      const newConv = createNewConversation();
      setConversations([newConv]);
      setActiveConversationId(newConv.conversation_id);
      saveConversation(newConv);
    } else {
      const mostRecent = savedConversations[0];
      setActiveConversationId(mostRecent.conversation_id);
      setMessages(mostRecent.messages);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSelectConversation = (conversationId: string) => {
    const conversation = getConversation(conversationId);
    if (conversation) {
      setActiveConversationId(conversationId);
      setMessages(conversation.messages);
    }
  };

  const handleNewConversation = () => {
    const newConv = createNewConversation();
    const updatedConversations = [newConv, ...conversations];
    setConversations(updatedConversations);
    setActiveConversationId(newConv.conversation_id);
    setMessages([]);
    saveConversation(newConv);
  };

  const handleDeleteConversation = (conversationId: string) => {
    deleteConversation(conversationId);
    const updatedConversations = conversations.filter(c => c.conversation_id !== conversationId);
    setConversations(updatedConversations);
    if (conversationId === activeConversationId) {
      if (updatedConversations.length > 0) {
        const nextConv = updatedConversations[0];
        setActiveConversationId(nextConv.conversation_id);
        setMessages(nextConv.messages);
      } else {
        handleNewConversation();
      }
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !activeConversationId || !userId || loading) return;
    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    const inputText = input;
    setMessages(newMessages);
    setInput('');
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputText,
          user_id: userId,
          conversation_id: activeConversationId
        }),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        agent_workflow: data.agent_workflow
      };
      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);
      const updatedConversation: Conversation = {
        conversation_id: activeConversationId,
        title: messages.length === 0 ? inputText.slice(0, 50) + (inputText.length > 50 ? '...' : '') :
          conversations.find(c => c.conversation_id === activeConversationId)?.title || 'Nova conversa',
        messages: finalMessages,
        lastUpdated: Date.now()
      };
      saveConversation(updatedConversation);
      const updatedConversations = conversations.map(c =>
        c.conversation_id === activeConversationId ? updatedConversation : c
      );
      setConversations(updatedConversations);
    } catch (err) {
      console.error('Error sending message:', err);
      setMessages(prev => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last && last.role === 'assistant' && last.content === '') {
          last.content = 'Desculpe, houve um erro. Tente novamente.';
        }
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[var(--infinite-neutral-900)] text-[var(--infinite-neutral-200)]">
      <ConversationList
        conversations={ conversations }
        activeConversationId={ activeConversationId }
        onSelectConversation={ handleSelectConversation }
        onNewConversation={ handleNewConversation }
        onDeleteConversation={ handleDeleteConversation }
        isOpen={ sidebarOpen }
        onClose={ () => setSidebarOpen(false) }
      />
      <div className="flex-1 flex flex-col lg:ml-0">
        <header className="p-4 sm:p-6 border-b border-[var(--infinite-purple-0)] bg-[var(--infinite-neutral-800)]">
          <div className="flex items-center justify-between">
            <button
              onClick={ () => setSidebarOpen(true) }
              className="lg:hidden p-2 rounded-md text-[var(--infinite-neutral-200)] hover:bg-[var(--infinite-neutral-900)]"
              aria-label="Abrir conversas"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={ 2 } d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div className="flex-1 text-center lg:text-left lg:ml-0">
              <h1 className="text-xl sm:text-2xl font-bold text-[var(--infinite-green-500)]">
                InfinitePay Chat Assistant
              </h1>
              <p className="text-sm sm:text-base text-[var(--infinite-neutral-400)] mt-1">
                Como posso ajudar você hoje?
              </p>
            </div>
          </div>
        </header>
        <main
          className="flex-1 overflow-y-auto p-3 sm:p-4 bg-[var(--infinite-neutral-900)]"
          role="main"
          aria-label="Chat conversation"
        >
          <div className="max-w-3xl mx-auto">
            { messages.length === 0 && (
              <div className="text-center py-12 sm:py-20">
                <div className="text-4xl sm:text-6xl mb-4">💬</div>
                <h2 className="text-lg sm:text-xl font-semibold text-[var(--infinite-purple-200)] mb-2">
                  Comece uma conversa
                </h2>
                <p className="text-sm sm:text-base text-[var(--infinite-neutral-400)]">
                  Pergunte qualquer coisa e eu vou ajudar!
                </p>
              </div>
            ) }
            { messages.map((msg, idx) => (
              <ChatMessage
                key={ idx }
                message={ msg }
                isLast={ idx === messages.length - 1 && loading }
              />
            )) }
            { loading && messages[messages.length - 1]?.role === 'user' && (
              <LoadingIndicator message="Pensando..." />
            ) }
            <div ref={ messagesEndRef } />
          </div>
        </main>
        <MessageInput
          value={ input }
          onChange={ setInput }
          onSend={ sendMessage }
          loading={ loading }
          placeholder="Digite sua mensagem..."
        />
      </div>
    </div>
  );
}
