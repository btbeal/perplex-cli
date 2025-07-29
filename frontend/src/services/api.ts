import axios from 'axios';
import { ChatRequest, ChatResponse, HealthResponse, AgentType } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async checkHealth(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
  },

  // General agent chat
  async chatGeneral(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat', request);
    return response.data;
  },

  // Sports agent chat
  async chatSports(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat/sports', request);
    return response.data;
  },

  // Finance agent chat
  async chatFinance(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat/finance', request);
    return response.data;
  },

  // Get sports summary
  async getSportsSummary(): Promise<ChatResponse> {
    const response = await api.get<ChatResponse>('/chat/sports/summary');
    return response.data;
  },

  // Get finance summary
  async getFinanceSummary(): Promise<ChatResponse> {
    const response = await api.get<ChatResponse>('/chat/finance/summary');
    return response.data;
  },

  // Generic chat method based on agent type
  async chat(agentType: AgentType, request: ChatRequest): Promise<ChatResponse> {
    switch (agentType) {
      case 'sports':
        return this.chatSports(request);
      case 'finance':
        return this.chatFinance(request);
      case 'general':
      default:
        return this.chatGeneral(request);
    }
  },

  // Get initial summary based on agent type
  async getInitialSummary(agentType: AgentType): Promise<ChatResponse | null> {
    switch (agentType) {
      case 'sports':
        return this.getSportsSummary();
      case 'finance':
        return this.getFinanceSummary();
      case 'general':
      default:
        return null; // General agent doesn't have an initial summary
    }
  },
}; 