export interface Source {
  title: string;
  url: string;
}

export interface PerplexityResponse {
  summary: string;
  explore_more: Source[];
}

export interface ChatResponse {
  response: PerplexityResponse;
  thread_id: string;
}

export interface ChatRequest {
  message: string;
  thread_id?: string;
}

export interface HealthResponse {
  status: string;
  message: string;
}

export type AgentType = 'general' | 'sports' | 'finance'; 