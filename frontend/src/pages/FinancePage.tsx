import React, { useState, useEffect } from 'react';
import ChatInterface from '../components/ChatInterface';
import { apiService } from '../services/api';
import { ChatResponse } from '../types/api';
import '../components/LoadingError.css';

const FinancePage: React.FC = () => {
  const [initialResponse, setInitialResponse] = useState<ChatResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInitialSummary = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiService.getFinanceSummary();
        setInitialResponse(response);
      } catch (err) {
        console.error('Error fetching finance summary:', err);
        setError('Failed to load finance summary. Please refresh the page.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchInitialSummary();
  }, []);

  if (isLoading) {
    return (
      <div className="loading-page">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <p>Loading finance summary...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-page">
        <div className="error-content">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <ChatInterface
      agentType="finance"
      welcomeMessage="Finance Hub - Market Insights"
      initialResponse={initialResponse}
    />
  );
};

export default FinancePage; 