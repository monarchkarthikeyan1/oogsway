import React, { useRef, useEffect } from 'react';
import { User, Bot, BookOpen, Layout, ExternalLink, Copy, Check, FileText } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';
import { Artifact, Citation } from '../services/api';

export const ChatWindow: React.FC = () => {
  const { messages, isLoading, setActiveArtifact, setActiveCitation } = useChatStore();
  const bottomRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = React.useState<string | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Simple renderer to turn [1], [2] citation markers into interactive buttons
  const renderFormattedContent = (content: string, citations?: Citation[]) => {
    const parts = content.split(/(\[\d+\])/g);
    return (
      <div className="prose prose-invert max-w-none text-sm leading-relaxed whitespace-pre-wrap">
        {parts.map((part, i) => {
          const match = part.match(/\[(\d+)\]/);
          if (match && citations) {
            const citIndex = parseInt(match[1], 10) - 1;
            const citation = citations[citIndex];
            return (
              <button
                key={i}
                onClick={() => citation && setActiveCitation(citation)}
                className="inline-flex items-center mx-1 px-1.5 py-0.5 text-[11px] font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30 rounded hover:bg-sky-500/30 transition-colors"
                title={citation ? `${citation.guest} in ${citation.episode_title}` : 'Source Quote'}
              >
                {part}
              </button>
            );
          }
          return <span key={i}>{part}</span>;
        })}
      </div>
    );
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-950/60">
      {messages.length === 0 && !isLoading && (
        <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-sky-500 to-emerald-400 p-[1px] mb-4">
            <div className="w-full h-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Bot className="w-6 h-6 text-sky-400" />
            </div>
          </div>
          <h2 className="text-lg font-bold text-slate-100 mb-2">Lenny Growth Assistant</h2>
          <p className="text-xs text-slate-400 leading-relaxed mb-6">
            Ask any question about Product Management, Growth Loops, PLG, or Founder Mode grounded strictly in Lenny’s Podcast transcripts.
          </p>
        </div>
      )}

      {messages.map((msg) => {
        const isUser = msg.role === 'user';
        return (
          <div
            key={msg.id}
            className={`flex gap-4 max-w-4xl mx-auto ${isUser ? 'justify-end' : 'justify-start'}`}
          >
            {!isUser && (
              <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                <Bot className="w-4 h-4 text-sky-400" />
              </div>
            )}

            <div className={`space-y-3 max-w-3xl ${isUser ? 'order-1' : 'order-2'}`}>
              <div
                className={`p-4 rounded-2xl ${
                  isUser
                    ? 'bg-sky-600/20 border border-sky-500/30 text-slate-100 rounded-tr-none'
                    : 'glass-panel text-slate-200 rounded-tl-none'
                }`}
              >
                {renderFormattedContent(msg.content, msg.citations)}

                {/* Copy response action */}
                {!isUser && (
                  <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <button
                      onClick={() => copyToClipboard(msg.content, msg.id)}
                      className="flex items-center gap-1 hover:text-slate-200 transition-colors"
                    >
                      {copiedId === msg.id ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                          <span className="text-emerald-400">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy Response</span>
                        </>
                      )}
                    </button>

                    {msg.citations && msg.citations.length > 0 && (
                      <span className="text-[11px] text-sky-400/80">
                        {msg.citations.length} grounded citation{msg.citations.length > 1 ? 's' : ''}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Citations Card Row */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-1">
                  {msg.citations.map((c) => (
                    <button
                      key={c.id}
                      onClick={() => setActiveCitation(c)}
                      className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-sky-500/40 text-xs text-slate-300 transition-all"
                    >
                      <BookOpen className="w-3.5 h-3.5 text-sky-400" />
                      <span className="font-semibold text-sky-300">{c.id}</span>
                      <span className="text-slate-400">{c.guest}</span>
                    </button>
                  ))}
                </div>
              )}

              {/* Generated Artifacts Trigger Card */}
              {msg.artifacts && msg.artifacts.length > 0 && (
                <div className="space-y-2 pt-2">
                  {msg.artifacts.map((art) => (
                    <div
                      key={art.id}
                      onClick={() => setActiveArtifact(art)}
                      className="p-3.5 rounded-xl bg-gradient-to-r from-slate-900 to-slate-800 border border-sky-500/30 hover:border-sky-400 cursor-pointer flex items-center justify-between group shadow-lg transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center">
                          {art.artifact_type === 'html' ? (
                            <Layout className="w-4 h-4 text-sky-400" />
                          ) : (
                            <FileText className="w-4 h-4 text-emerald-400" />
                          )}
                        </div>
                        <div>
                          <div className="text-xs font-semibold text-slate-200 group-hover:text-sky-300">
                            {art.title}
                          </div>
                          <div className="text-[11px] text-slate-400 uppercase tracking-wider font-mono">
                            {art.artifact_type} Artifact • Click to view in Side Panel
                          </div>
                        </div>
                      </div>
                      <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-sky-300 transition-colors" />
                    </div>
                  ))}
                </div>
              )}
            </div>

            {isUser && (
              <div className="w-8 h-8 rounded-lg bg-sky-600/20 border border-sky-500/30 flex items-center justify-center flex-shrink-0 mt-1">
                <User className="w-4 h-4 text-sky-300" />
              </div>
            )}
          </div>
        );
      })}

      {isLoading && (
        <div className="flex gap-4 max-w-4xl mx-auto items-center">
          <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center">
            <Bot className="w-4 h-4 text-sky-400 animate-pulse" />
          </div>
          <div className="p-4 rounded-2xl glass-panel text-slate-400 text-xs flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
            Searching transcripts and synthesizing grounded response...
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
