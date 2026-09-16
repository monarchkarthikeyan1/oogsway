import axios from 'axios';

const API_BASE = '/api/v1';

export interface Citation {
  id: string;
  guest: string;
  episode_title: string;
  quote: string;
  source_url?: string;
  timestamp?: string;
}

export interface Artifact {
  id: string;
  session_id: string;
  message_id?: string;
  title: string;
  artifact_type: string;
  content: string;
  language?: string;
  created_at: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  citations?: Citation[];
  artifacts?: Artifact[];
  created_at: string;
}

export interface Session {
  id: string;
  title: string;
  provider: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface ProviderStatus {
  current_provider: string;
  ollama_available: boolean;
  ollama_model: string;
  anthropic_available: boolean;
  openai_available: boolean;
  active_models: Record<string, string>;
}

export const api = {
  // Sessions
  async listSessions(): Promise<Session[]> {
    const res = await axios.get(`${API_BASE}/sessions`);
    return res.data;
  },

  async createSession(title?: string, provider?: string): Promise<Session> {
    const res = await axios.post(`${API_BASE}/sessions`, { title, provider });
    return res.data;
  },

  async getSession(sessionId: string): Promise<Session> {
    const res = await axios.get(`${API_BASE}/sessions/${sessionId}`);
    return res.data;
  },

  async deleteSession(sessionId: string): Promise<void> {
    await axios.delete(`${API_BASE}/sessions/${sessionId}`);
  },

  // Chat
  async sendMessage(sessionId: string, message: string, provider?: string, mode: string = 'chat'): Promise<{
    response: string;
    citations: Citation[];
    artifacts: Artifact[];
  }> {
    const res = await axios.post(`${API_BASE}/chat/message`, {
      session_id: sessionId,
      message,
      provider,
      mode
    });
    return res.data;
  },

  // Artifacts
  async getArtifact(artifactId: string): Promise<Artifact> {
    const res = await axios.get(`${API_BASE}/artifacts/${artifactId}`);
    return res.data;
  },

  // Providers
  async getProviders(): Promise<ProviderStatus> {
    const res = await axios.get(`${API_BASE}/providers`);
    return res.data;
  },

  async toggleProvider(provider: string): Promise<ProviderStatus> {
    const res = await axios.post(`${API_BASE}/providers/toggle`, { provider });
    return res.data;
  },

  // Health
  async getHealth() {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  }
};
