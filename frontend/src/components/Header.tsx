import React, { useEffect } from 'react';
import { Cpu, Plus, Settings, Sparkles, BookOpen, ShieldCheck } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const Header: React.FC = () => {
  const { 
    providerStatus, 
    fetchProviderStatus, 
    setModelModalOpen, 
    createNewSession, 
    sessions, 
    currentSessionId 
  } = useChatStore();

  useEffect(() => {
    fetchProviderStatus();
  }, [fetchProviderStatus]);

  const currentSession = sessions.find(s => s.id === currentSessionId);
  const currentProvider = providerStatus?.current_provider || 'ollama';

  const isOllamaActive = currentProvider === 'ollama';
  const isAvailable = isOllamaActive 
    ? providerStatus?.ollama_available 
    : (currentProvider === 'anthropic' ? providerStatus?.anthropic_available : providerStatus?.openai_available);

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-6 flex items-center justify-between z-10">
      {/* Brand & Logo */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-400 to-emerald-400 p-[1px] shadow-lg shadow-sky-500/20">
          <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-sky-400" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-slate-100 tracking-tight text-base">The Lenny Growth Assistant</h1>
            <span className="px-2 py-0.5 text-[10px] font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-full">
              FDE Edition
            </span>
          </div>
          <p className="text-xs text-slate-400">
            {currentSession ? currentSession.title : "Grounded Product & Growth Intelligence"}
          </p>
        </div>
      </div>

      {/* Action Controls & Provider Selector */}
      <div className="flex items-center gap-3">
        {/* Model Switcher Pill */}
        <button
          onClick={() => setModelModalOpen(true)}
          className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 transition-all text-xs font-medium text-slate-200"
          title="Click to change LLM provider"
        >
          <Cpu className="w-4 h-4 text-sky-400" />
          <span className="capitalize">{currentProvider}</span>
          <span className="text-slate-500 text-[10px]">
            ({providerStatus?.active_models[currentProvider] || 'llama3.2'})
          </span>
          <span className={`w-2 h-2 rounded-full ${isAvailable ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-amber-400'}`} />
        </button>

        {/* Security Shield Indicator */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <ShieldCheck className="w-4 h-4" />
          <span>Iframe Sandbox Active</span>
        </div>

        {/* Settings button */}
        <button
          onClick={() => setModelModalOpen(true)}
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
          title="Model Configuration Settings"
        >
          <Settings className="w-4 h-4" />
        </button>

        {/* New Session Button */}
        <button
          onClick={() => createNewSession("New Growth Chat")}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-medium text-xs shadow-md shadow-sky-500/20 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>
    </header>
  );
};
