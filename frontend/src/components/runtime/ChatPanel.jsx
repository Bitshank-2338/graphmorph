import { useState } from "react";

const SUGGESTIONS = [
  "Who are the organizational bottlenecks?",
  "What skills are missing across the org?",
  "Show shortest path between Sales and Engineering",
  "Cluster the org by department",
  "What happens if Alice leaves?",
  "Build me a custom dashboard for Engineering risk", // generative
];

export default function ChatPanel({ onAsk, busy }) {
  const [query, setQuery] = useState("");

  const submit = (q) => {
    const text = (q ?? query).trim();
    if (!text) return;
    onAsk(text);
    setQuery("");
  };

  return (
    <div className="h-full flex flex-col">
      <div className="text-[11px] uppercase tracking-widest text-zinc-500 mb-2">
        Ask the agent
      </div>

      <textarea
        className="w-full bg-zinc-900/70 border border-zinc-800 rounded-lg p-3 text-sm
                   focus:outline-none focus:border-accent/60 resize-none"
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submit();
        }}
        placeholder="e.g. Who are the bottlenecks?"
      />

      <button
        className="mt-2 w-full bg-accent hover:bg-accent/90 disabled:opacity-50
                   text-white font-medium px-3 py-2 rounded-lg text-sm transition"
        onClick={() => submit()}
        disabled={busy}
      >
        {busy ? "Generating..." : "Ask agent"}
      </button>

      <div className="mt-4 text-[11px] uppercase tracking-widest text-zinc-500 mb-2">
        Try
      </div>
      <div className="space-y-1.5 overflow-y-auto pr-1">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => submit(s)}
            disabled={busy}
            className="w-full text-left text-[12px] bg-zinc-900/40 hover:bg-zinc-900/80
                       border border-zinc-800 hover:border-accent/40 transition
                       rounded-md px-2.5 py-2 text-zinc-300"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
