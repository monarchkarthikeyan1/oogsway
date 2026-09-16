import React from 'react';
import { X, BookOpen, ExternalLink, Quote } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const CitationDrawer: React.FC = () => {
  const { activeCitation, setActiveCitation } = useChatStore();

  if (!activeCitation) return null;

  return (
    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-xl w-full p-6 space-y-4 shadow-2xl relative">
        <button
          onClick={() => setActiveCitation(null)}
          className="absolute right-4 top-4 text-slate-400 hover:text-slate-200 p-1 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 text-xs font-semibold text-sky-400 uppercase tracking-wider">
          <BookOpen className="w-4 h-4" />
          <span>Grounded Source Citation {activeCitation.id}</span>
        </div>

        <div>
          <h3 className="text-base font-bold text-slate-100">{activeCitation.guest}</h3>
          <p className="text-xs text-slate-400 mt-0.5">{activeCitation.episode_title}</p>
          {activeCitation.timestamp && (
            <span className="inline-block mt-2 px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono text-slate-300">
              Timestamp: {activeCitation.timestamp}
            </span>
          )}
        </div>

        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans relative">
          <Quote className="w-6 h-6 text-sky-500/20 absolute right-3 top-3" />
          <p className="italic relative z-10">"{activeCitation.quote}"</p>
        </div>

        {activeCitation.source_url && (
          <a
            href={activeCitation.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs text-sky-400 hover:underline pt-2"
          >
            <span>View Full Transcript on Lenny's Newsletter</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}
      </div>
    </div>
  );
};
