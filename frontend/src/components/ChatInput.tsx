import React, { useState } from 'react';
import { Send, FileText, Layout, MessageSquare, Sparkles } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const ChatInput: React.FC = () => {
  const [text, setText] = useState('');
  const { sendMessage, isLoading, activeMode, setActiveMode } = useChatStore();

  const handleSend = () => {
    if (!text.trim() || isLoading) return;
    sendMessage(text, activeMode);
    setText('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 border-t border-slate-800 bg-slate-950/90 backdrop-blur-md">
      <div className="max-w-4xl mx-auto space-y-3">
        {/* Mode Selector Badges */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveMode('chat')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all ${
              activeMode === 'chat'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 border border-transparent'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Grounded Q&A</span>
          </button>

          <button
            onClick={() => setActiveMode('ship30')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all ${
              activeMode === 'ship30'
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 border border-transparent'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Ship 30 Essay</span>
          </button>

          <button
            onClick={() => setActiveMode('artifact')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all ${
              activeMode === 'artifact'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 border border-transparent'
            }`}
          >
            <Layout className="w-3.5 h-3.5" />
            <span>HTML Artifact</span>
          </button>
        </div>

        {/* Input Box */}
        <div className="relative glass-panel rounded-xl border border-slate-700/80 focus-within:border-sky-500/80 transition-colors">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              activeMode === 'ship30'
                ? "Ask to generate a ~1,250 word Ship 30 essay (e.g. 'Write a Ship 30 essay on Elena Verna PLG loops')..."
                : activeMode === 'artifact'
                ? "Ask to generate a rendered HTML/CSS artifact (e.g. 'Create an interactive ROI calculator component')..."
                : "Ask anything about product strategy, growth loops, or team empowerment..."
            }
            rows={2}
            className="w-full bg-transparent p-3.5 pr-12 text-xs text-slate-100 placeholder-slate-500 focus:outline-none resize-none"
          />

          <button
            onClick={handleSend}
            disabled={!text.trim() || isLoading}
            className="absolute right-3 bottom-3 p-2 rounded-lg bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white shadow-md transition-all"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
