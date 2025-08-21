// domingosmachado/chatbot/ChatBot-c52a09916732c591151116fd44bf41bbdf5f54e5/frontend/src/app/page.tsx
'use client';
import { useState, useEffect, useRef } from 'react';

interface Message {
  role: string;
  content: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Create a unique session ID for the user's conversation history
    if (!sessionId) {
      setSessionId(crypto.randomUUID());
    }
  }, [sessionId]);

  useEffect(() => {
    // Automatically scroll to the latest message
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

      // Add a placeholder for the assistant's response
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
                // Update the last message (the placeholder) with new content
                setMessages(prev => {
                  const updatedMessages = [...prev];
                  const lastMessage = updatedMessages[updatedMessages.length - 1];
                  if (lastMessage && lastMessage.role === 'assistant') {
                    lastMessage.content += parsed.content;
                  }
                  return updatedMessages;
                });
              }
            } catch (error) {
              // This can happen with incomplete JSON chunks, safe to ignore
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // If an error occurs, update the placeholder with an error message
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
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 font-sans">
      <div className="flex-1 overflow-y-auto mb-4 p-4 border rounded-lg bg-white/50 dark:bg-black/50">
        { messages.map((msg, idx) => (
          <div key={ idx } className={ `mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}` }>
            <div className={ `p-3 rounded-lg max-w-[80%] whitespace-pre-wrap ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}` }>
              <p>{ msg.content }</p>
            </div>
          </div>
        )) }
        { loading && messages[messages.length - 1]?.role === 'user' && (
          <div className="mb-4 flex justify-start">
            <div className="p-3 rounded-lg bg-gray-200 text-gray-500 dark:bg-gray-700 dark:text-gray-400">
              Typing...
            </div>
          </div>
        ) }
        <div ref={ messagesEndRef } />
      </div>
      <div className="flex gap-2">
        <input
          value={ input }
          onChange={ (e) => setInput(e.target.value) }
          onKeyPress={ (e) => e.key === 'Enter' && sendMessage() }
          className="flex-1 p-2 border rounded text-gray-800 bg-white dark:bg-gray-900 dark:text-gray-200 dark:border-gray-600"
          placeholder="Type your message..."
          disabled={ loading }
        />
        <button onClick={ sendMessage } className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-blue-300" disabled={ loading }>
          Send
        </button>
      </div>
    </div>
  );
}