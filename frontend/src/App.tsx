import React, { useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import { ArtifactViewer } from './components/ArtifactViewer';
import { CitationDrawer } from './components/CitationDrawer';
import { ModelSelectorModal } from './components/ModelSelectorModal';
import { useChatStore } from './store/useChatStore';

export const App: React.FC = () => {
  const { fetchSessions, fetchProviderStatus } = useChatStore();

  useEffect(() => {
    fetchSessions();
    fetchProviderStatus();
  }, [fetchSessions, fetchProviderStatus]);

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Navigation Header */}
      <Header />

      {/* Main Workspace Layout */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Left Sidebar */}
        <Sidebar />

        {/* Center Chat View */}
        <main className="flex-1 flex flex-col overflow-hidden relative">
          <ChatWindow />
          <ChatInput />
        </main>

        {/* Right Split-Pane Claude-Style Native Artifact Viewer */}
        <ArtifactViewer />
      </div>

      {/* Modals & Overlay Drawers */}
      <CitationDrawer />
      <ModelSelectorModal />
    </div>
  );
};

export default App;
