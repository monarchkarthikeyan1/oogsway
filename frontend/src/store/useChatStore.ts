import { create } from 'zustand';
import { api, Session, Message, Artifact, Citation, ProviderStatus } from '../services/api';

interface ChatStore {
  sessions: Session[];
  currentSessionId: string | null;
  messages: Message[];
  activeArtifact: Artifact | null;
  activeCitation: Citation | null;
  providerStatus: ProviderStatus | null;
  isLoading: boolean;
  isModelModalOpen: boolean;
  activeMode: 'chat' | 'ship30' | 'artifact';

  // Actions
  fetchSessions: () => Promise<void>;
  selectSession: (sessionId: string) => Promise<void>;
  createNewSession: (title?: string) => Promise<string>;
  deleteSession: (sessionId: string) => Promise<void>;
  sendMessage: (content: string, mode?: 'chat' | 'ship30' | 'artifact') => Promise<void>;
  
  setActiveArtifact: (artifact: Artifact | null) => void;
  setActiveCitation: (citation: Citation | null) => void;
  setModelModalOpen: (isOpen: boolean) => void;
  toggleProvider: (provider: string) => Promise<void>;
  fetchProviderStatus: () => Promise<void>;
  setActiveMode: (mode: 'chat' | 'ship30' | 'artifact') => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  sessions: [],
  currentSessionId: null,
  messages: [],
  activeArtifact: null,
  activeCitation: null,
  providerStatus: null,
  isLoading: false,
  isModelModalOpen: false,
  activeMode: 'chat',

  fetchSessions: async () => {
    try {
      const sessions = await api.listSessions();
      set({ sessions });
      if (sessions.length > 0 && !get().currentSessionId) {
        await get().selectSession(sessions[0].id);
      } else if (sessions.length === 0) {
        await get().createNewSession("Welcome Growth Session");
      }
    } catch (err) {
      console.error("Error fetching sessions:", err);
    }
  },

  selectSession: async (sessionId: string) => {
    set({ isLoading: true, currentSessionId: sessionId });
    try {
      const session = await api.getSession(sessionId);
      set({ 
        messages: session.messages || [],
        isLoading: false 
      });
    } catch (err) {
      console.error("Error selecting session:", err);
      set({ isLoading: false });
    }
  },

  createNewSession: async (title = "New Growth Chat") => {
    set({ isLoading: true });
    try {
      const newSession = await api.createSession(title, get().providerStatus?.current_provider);
      set((state) => ({
        sessions: [newSession, ...state.sessions],
        currentSessionId: newSession.id,
        messages: [],
        activeArtifact: null,
        activeCitation: null,
        isLoading: false
      }));
      return newSession.id;
    } catch (err) {
      console.error("Error creating session:", err);
      set({ isLoading: false });
      return "";
    }
  },

  deleteSession: async (sessionId: string) => {
    try {
      await api.deleteSession(sessionId);
      const remaining = get().sessions.filter((s) => s.id !== sessionId);
      set({ sessions: remaining });
      if (get().currentSessionId === sessionId) {
        if (remaining.length > 0) {
          await get().selectSession(remaining[0].id);
        } else {
          await get().createNewSession();
        }
      }
    } catch (err) {
      console.error("Error deleting session:", err);
    }
  },

  sendMessage: async (content: string, modeOverride) => {
    const { currentSessionId, messages, providerStatus, activeMode } = get();
    if (!currentSessionId || !content.trim()) return;

    const mode = modeOverride || activeMode;

    // Optimistic user message update
    const tempUserMsg: Message = {
      id: `temp-${Date.now()}`,
      session_id: currentSessionId,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    };

    set({ 
      messages: [...messages, tempUserMsg],
      isLoading: true 
    });

    try {
      const res = await api.sendMessage(
        currentSessionId,
        content,
        providerStatus?.current_provider,
        mode
      );

      // Refresh session messages
      const session = await api.getSession(currentSessionId);
      set({
        messages: session.messages || [],
        isLoading: false
      });

      // If an artifact was generated in this turn, automatically pop open the Artifact Viewer!
      if (res.artifacts && res.artifacts.length > 0) {
        set({ activeArtifact: res.artifacts[0] });
      }
    } catch (err) {
      console.error("Error sending message:", err);
      set({ isLoading: false });
    }
  },

  setActiveArtifact: (artifact) => set({ activeArtifact: artifact }),
  setActiveCitation: (citation) => set({ activeCitation: citation }),
  setModelModalOpen: (isOpen) => set({ isModelModalOpen: isOpen }),
  setActiveMode: (mode) => set({ activeMode: mode }),

  fetchProviderStatus: async () => {
    try {
      const status = await api.getProviders();
      set({ providerStatus: status });
    } catch (err) {
      console.error("Error fetching provider status:", err);
    }
  },

  toggleProvider: async (providerName: string) => {
    try {
      const updated = await api.toggleProvider(providerName);
      set({ providerStatus: updated });
    } catch (err) {
      console.error("Error toggling provider:", err);
    }
  }
}));
