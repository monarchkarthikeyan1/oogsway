import React from 'react';
import { X, Cpu, Cloud, Check, AlertCircle } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const ModelSelectorModal: React.FC = () => {
  const { isModelModalOpen, setModelModalOpen, providerStatus, toggleProvider } = useChatStore();

  if (!isModelModalOpen) return null;

  const currentProvider = providerStatus?.current_provider || 'ollama';

  const providers = [
    {
      id: 'ollama',
      name: 'Ollama (Local LLM)',
      tag: 'Mandatory Demo Target',
      model: providerStatus?.ollama_model || 'llama3.2',
      available: providerStatus?.ollama_available,
      desc: 'Zero-cloud local inference running via Ollama daemon at http://localhost:11434.'
    },
    {
      id: 'anthropic',
      name: 'Anthropic Claude',
      tag: 'Cloud LLM',
      model: providerStatus?.active_models['anthropic'] || 'claude-3-5-sonnet',
      available: providerStatus?.anthropic_available,
      desc: 'Requires ANTHROPIC_API_KEY set in .env'
    },
    {
      id: 'openai',
      name: 'OpenAI GPT-4o',
      tag: 'Cloud LLM',
      model: providerStatus?.active_models['openai'] || 'gpt-4o-mini',
      available: providerStatus?.openai_available,
      desc: 'Requires OPENAI_API_KEY set in .env'
    }
  ];

  return (
    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 space-y-5 shadow-2xl relative">
        <button
          onClick={() => setModelModalOpen(false)}
          className="absolute right-4 top-4 text-slate-400 hover:text-slate-200 p-1 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-100">LLM Provider Configuration</h3>
            <p className="text-xs text-slate-400">Switch between local Ollama and cloud LLMs seamlessly</p>
          </div>
        </div>

        <div className="space-y-3">
          {providers.map((p) => {
            const isSelected = currentProvider === p.id;
            return (
              <div
                key={p.id}
                onClick={() => toggleProvider(p.id)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  isSelected
                    ? 'bg-sky-500/10 border-sky-500/50 shadow-lg shadow-sky-500/10'
                    : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-slate-200">{p.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                      {p.tag}
                    </span>
                  </div>

                  {isSelected && (
                    <div className="w-5 h-5 rounded-full bg-sky-500 text-white flex items-center justify-center">
                      <Check className="w-3.5 h-3.5" />
                    </div>
                  )}
                </div>

                <p className="text-xs text-slate-400 mt-2">{p.desc}</p>

                <div className="mt-3 flex items-center justify-between text-[11px]">
                  <span className="font-mono text-slate-300">Model: {p.model}</span>
                  <div className="flex items-center gap-1.5">
                    {p.available ? (
                      <span className="text-emerald-400 flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#34d399]" />
                        Ready
                      </span>
                    ) : (
                      <span className="text-amber-400 flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" />
                        Key/Server Missing
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="pt-2 text-[11px] text-slate-400 border-t border-slate-800">
          <span className="font-semibold text-slate-300">Fallback Behavior:</span> If the selected provider is unavailable, the assistant automatically falls back to Ollama or displays an actionable diagnostic setup message.
        </div>
      </div>
    </div>
  );
};
