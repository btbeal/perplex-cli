import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/api';
import { AgentType, ChatResponse } from '../types/api';
import ResponseDisplay from './ResponseDisplay';
import './ChatInterface.css';

interface ChatInterfaceProps {
  agentType: AgentType;
  welcomeMessage: string;
  initialResponse?: ChatResponse | null;
}

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  response?: ChatResponse;
  timestamp: Date;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  agentType, 
  welcomeMessage, 
  initialResponse 
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Add initial response if provided
  useEffect(() => {
    if (initialResponse) {
      const initialMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: initialResponse.response.summary,
        response: initialResponse,
        timestamp: new Date(),
      };
      setMessages([initialMessage]);
      setThreadId(initialResponse.thread_id);
    } else {
      setMessages([]);
      setThreadId(undefined);
    }
  }, [initialResponse, agentType]);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await apiService.chat(agentType, {
        message: input.trim(),
        thread_id: threadId,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.response.summary,
        response: response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setThreadId(response.thread_id);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <div className="chat-interface">
      <div className="welcome-message">
        <h1>{welcomeMessage}</h1>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            {message.type === 'user' ? (
              <div className="user-message">
                <span className="message-content">{message.content}</span>
              </div>
            ) : (
              <div className="assistant-message">
                {message.response ? (
                  <ResponseDisplay response={message.response.response} />
                ) : (
                  <span className="message-content">{message.content}</span>
                )}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="assistant-message">
              <div className="loading-indicator">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Ask me anything about ${agentType === 'general' ? 'any topic' : agentType}...`}
            disabled={isLoading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="send-button"
          >
            <span className="send-icon">→</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface; 