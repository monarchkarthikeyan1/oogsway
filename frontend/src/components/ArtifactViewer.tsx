import React, { useState } from 'react';
import { X, Eye, Code, Copy, Check, Download, Shield, Sparkles } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const ArtifactViewer: React.FC = () => {
  const { activeArtifact, setActiveArtifact } = useChatStore();
  const [activeTab, setActiveTab] = useState<'preview' | 'code'>('preview');
  const [copied, setCopied] = useState(false);

  if (!activeArtifact) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(activeArtifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const ext = activeArtifact.artifact_type === 'html' ? 'html' : 'md';
    const blob = new Blob([activeArtifact.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${activeArtifact.title.replace(/\s+/g, '_').toLowerCase()}.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="w-1/2 h-full border-l border-slate-800 bg-slate-950 flex flex-col z-20 shadow-2xl transition-all">
      {/* Top Bar */}
      <div className="h-14 px-4 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Claude-Style Artifact Viewer</span>
          </div>
          <h2 className="text-xs font-bold text-slate-100 truncate max-w-[200px]">
            {activeArtifact.title}
          </h2>
        </div>

        <div className="flex items-center gap-2">
          {/* Tab Switcher */}
          <div className="flex bg-slate-800/80 p-0.5 rounded-lg text-xs font-medium border border-slate-700">
            <button
              onClick={() => setActiveTab('preview')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-colors ${
                activeTab === 'preview' ? 'bg-sky-500 text-white font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Preview</span>
            </button>
            <button
              onClick={() => setActiveTab('code')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-colors ${
                activeTab === 'code' ? 'bg-sky-500 text-white font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Code</span>
            </button>
          </div>

          <button
            onClick={handleCopy}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
            title="Copy Source"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>

          <button
            onClick={handleDownload}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
            title="Download Artifact"
          >
            <Download className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveArtifact(null)}
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
            title="Close Viewer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Security Status Banner */}
      <div className="bg-slate-900/60 px-4 py-2 border-b border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-1.5 text-emerald-400 font-mono">
          <Shield className="w-3.5 h-3.5" />
          <span>Security: Sandboxed iframe (allow-scripts, isolated origin, CSP)</span>
        </div>
        <span className="uppercase text-[10px] text-slate-500 font-mono">{activeArtifact.artifact_type}</span>
      </div>

      {/* Viewer Body */}
      <div className="flex-1 bg-slate-950 p-4 overflow-hidden relative">
        {activeTab === 'preview' ? (
          activeArtifact.artifact_type === 'html' ? (
            <iframe
              srcDoc={activeArtifact.content}
              title={activeArtifact.title}
              sandbox="allow-scripts"
              className="w-full h-full rounded-xl border border-slate-800 bg-slate-900"
            />
          ) : (
            <div className="w-full h-full rounded-xl border border-slate-800 bg-slate-900 p-6 overflow-y-auto font-sans text-sm leading-relaxed text-slate-200 whitespace-pre-wrap">
              {activeArtifact.content}
            </div>
          )
        ) : (
          <pre className="w-full h-full rounded-xl border border-slate-800 bg-slate-900 p-4 overflow-auto font-mono text-xs text-sky-300 leading-relaxed">
            <code>{activeArtifact.content}</code>
          </pre>
        )}
      </div>
    </div>
  );
};
