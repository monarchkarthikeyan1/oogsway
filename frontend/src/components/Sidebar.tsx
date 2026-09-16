import React from 'react';
import { MessageSquare, Trash2, BookOpen, Sparkles, Layers, FileText, ChevronRight } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const Sidebar: React.FC = () => {
  const { 
    sessions, 
    currentSessionId, 
    selectSession, 
    deleteSession, 
    sendMessage,
    setActiveMode 
  } = useChatStore();

  const handleQuickPrompt = (prompt: string, mode: 'chat' | 'ship30' | 'artifact') => {
    setActiveMode(mode);
    sendMessage(prompt, mode);
  };

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col justify-between h-full select-none">
      {/* Top Session List */}
      <div className="p-4 flex-1 overflow-y-auto">
        <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 px-2 flex items-center justify-between">
          <span>Chat History</span>
          <span className="text-[10px] text-sky-400 bg-sky-500/10 px-1.5 py-0.5 rounded font-mono">
            {sessions.length} sessions
          </span>
        </div>

        <div className="space-y-1">
          {sessions.map((s) => {
            const isSelected = s.id === currentSessionId;
            return (
              <div
                key={s.id}
                onClick={() => selectSession(s.id)}
                className={`group flex items-center justify-between px-3 py-2.5 rounded-lg cursor-pointer text-xs transition-all ${
                  isSelected
                    ? 'bg-sky-500/10 text-sky-300 border border-sky-500/20 font-medium'
                    : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <MessageSquare className={`w-3.5 h-3.5 flex-shrink-0 ${isSelected ? 'text-sky-400' : 'text-slate-500'}`} />
                  <span className="truncate">{s.title}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteSession(s.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 text-slate-500 hover:text-rose-400 transition-opacity p-1"
                  title="Delete Chat"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })}
        </div>

        {/* Quick Skill Templates */}
        <div className="mt-8">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 px-2">
            Growth Skills
          </div>
          <div className="space-y-2">
            <button
              onClick={() => handleQuickPrompt("Write a Ship 30 for 30 essay on Shreyas Doshi's LNO framework and how to avoid PM burnout.", "ship30")}
              className="w-full text-left p-2.5 rounded-lg glass-card hover:border-sky-500/40 transition-all text-xs text-slate-300 flex items-start gap-2.5 group"
            >
              <FileText className="w-4 h-4 text-sky-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-semibold text-slate-200 group-hover:text-sky-300 flex items-center gap-1">
                  Ship 30 Essay <ChevronRight className="w-3 h-3 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
                </div>
                <div className="text-[11px] text-slate-400 mt-0.5">Generate 1,250w grounded essay on LNO Framework</div>
              </div>
            </button>

            <button
              onClick={() => handleQuickPrompt("Create an interactive Product Strategy Canvas artifact based on Marty Cagan's product discovery framework.", "artifact")}
              className="w-full text-left p-2.5 rounded-lg glass-card hover:border-emerald-500/40 transition-all text-xs text-slate-300 flex items-start gap-2.5 group"
            >
              <Layers className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-semibold text-slate-200 group-hover:text-emerald-300 flex items-center gap-1">
                  HTML Artifact <ChevronRight className="w-3 h-3 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
                </div>
                <div className="text-[11px] text-slate-400 mt-0.5">Render interactive HTML Product Canvas in viewer</div>
              </div>
            </button>

            <button
              onClick={() => handleQuickPrompt("How does Elena Verna explain Growth Loops vs Marketing Funnels for B2B SaaS?", "chat")}
              className="w-full text-left p-2.5 rounded-lg glass-card hover:border-purple-500/40 transition-all text-xs text-slate-300 flex items-start gap-2.5 group"
            >
              <Sparkles className="w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-semibold text-slate-200 group-hover:text-purple-300 flex items-center gap-1">
                  Growth Loops <ChevronRight className="w-3 h-3 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
                </div>
                <div className="text-[11px] text-slate-400 mt-0.5">PLG Insights from Elena Verna & Lenny</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Knowledge Base Info Card */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/40">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-300 mb-1">
          <BookOpen className="w-3.5 h-3.5 text-sky-400" />
          <span>Lenny Transcript Index</span>
        </div>
        <div className="text-[11px] text-slate-400">
          Loaded: Shreyas Doshi, Brian Chesky, Elena Verna, Marty Cagan, Gokul Rajaram & Claire Vo.
        </div>
      </div>
    </aside>
  );
};
