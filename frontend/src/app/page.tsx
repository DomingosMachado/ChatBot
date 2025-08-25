'use client';
import { useState, useEffect, useRef } from 'react';
import ChatMessage from '../components/ChatMessage';
import MessageInput from '../components/MessageInput';
import LoadingIndicator from '../components/LoadingIndicator';
import { Message } from '../types/chat';

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sessionId) {
      setSessionId(Math.random().toString(36).substring(2) + Date.now().toString(36));
    }
  }, [sessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || !sessionId || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages, session_id: sessionId }),
      });

      if (!response.body) throw new Error("Response body is null");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;

            try {
              const parsed = JSON.parse(data);
              if (parsed.content) {
                setMessages(prev => {
                  const updatedMessages = [...prev];
                  const lastMessage = updatedMessages[updatedMessages.length - 1];
                  if (lastMessage && lastMessage.role === 'assistant') {
                    lastMessage.content = parsed.content;
                  }
                  return updatedMessages;
                });
              }
            } catch {
              // Ignore JSON parse errors
            }
          }
        }
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setMessages(prev => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last && last.role === 'assistant' && last.content === '') {
          last.content = 'Sorry, I encountered an error. Please try again.';
        }
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto font-sans">
      <header className="p-4 sm:p-6 text-center border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-800 dark:text-gray-200">
          CloudWalk Chat Assistant
        </h1>
        <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 mt-1">
          How can I help you today?
        </p>
      </header>
      
      <main 
        className="flex-1 overflow-y-auto p-3 sm:p-4 bg-white/30 dark:bg-black/30"
        role="main"
        aria-label="Chat conversation"
      >
        <div className="max-w-3xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center py-12 sm:py-20">
              <div className="text-4xl sm:text-6xl mb-4">💬</div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-600 dark:text-gray-400 mb-2">
                Start a conversation
              </h2>
              <p className="text-sm sm:text-base text-gray-500 dark:text-gray-500">
                Ask me anything and I&apos;ll be happy to help!
              </p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <ChatMessage 
              key={idx} 
              message={msg} 
              isLast={idx === messages.length - 1 && loading}
            />
          ))}
          
          {loading && messages[messages.length - 1]?.role === 'user' && (
            <LoadingIndicator message="Thinking..." />
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </main>

      <MessageInput
        value={input}
        onChange={setInput}
        onSend={sendMessage}
        loading={loading}
        placeholder="Ask me anything..."
      />
    </div>
  );
}