'use client';
import { useState } from 'react';


export default function Chat() {
  const [messages, setMessages] = useState<Array<{ role: string, content: string }>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = '';

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
              const parsed = JSON.parse(data);
              assistantMessage += parsed.content;
              setMessages([...newMessages, { role: 'assistant', content: assistantMessage }]);
            } catch (e) { }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="border rounded-lg h-96 overflow-y-auto mb-4 p-4">
        { messages.map((msg, idx) => (
          <div key={ idx } className={ `mb-2 ${msg.role === 'user' ? 'text-right' : ''}` }>
            <span className={ `inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}` }>
              { msg.content }
            </span>
          </div>
        )) }
        { loading && <div>Assistant is typing...</div> }
      </div>
      <div className="flex gap-2">
        <input
          value={ input }
          onChange={ (e) => setInput(e.target.value) }
          onKeyPress={ (e) => e.key === 'Enter' && sendMessage() }
          className="flex-1 p-2 border rounded"
          placeholder="Type your message..."
        />
        <button onClick={ sendMessage } className="px-4 py-2 bg-blue-500 text-white rounded">
          Send
        </button>
      </div>
    </div>
  );
}