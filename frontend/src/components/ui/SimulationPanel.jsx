import { useState } from "react";
import { motion } from "framer-motion";
import DependencyMap from "./DependencyMap";

export default function SimulationPanel({ data }) {
  const nodes = data.nodes || [];
  const [removed, setRemoved] = useState(new Set());

  const toggle = (id) => {
    setRemoved((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const totalImpact = nodes
    .filter((n) => removed.has(n.id))
    .reduce((sum, n) => sum + (n.impact || 0), 0);

  return (
    <div>
      <div className="mb-4">
        <div className="text-xl font-semibold">{data.title}</div>
        {data.subtitle && (
          <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="text-[11px] uppercase tracking-widest text-zinc-500 mb-2">
            Toggle removal to simulate
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {nodes.map((n) => {
              const isOut = removed.has(n.id);
              return (
                <motion.button
                  key={n.id}
                  onClick={() => toggle(n.id)}
                  whileTap={{ scale: 0.97 }}
                  className={`text-left p-3 rounded-xl border transition ${
                    isOut
                      ? "bg-red-900/40 border-red-700/60 opacity-60 line-through"
                      : "bg-zinc-900/60 border-zinc-800 hover:border-accent/40"
                  }`}
                >
                  <div className="text-sm font-medium">{n.id}</div>
                  <div className="text-[11px] text-zinc-400">
                    impact: {(n.impact * 100).toFixed(0)}%
                  </div>
                </motion.button>
              );
            })}
          </div>
        </div>

        <div>
          <div className="bg-gradient-to-br from-accent/20 to-zinc-900/40 border border-accent/30 rounded-2xl p-4 mb-4">
            <div className="text-[11px] uppercase tracking-widest text-zinc-400">
              Cumulative disruption
            </div>
            <div className="text-3xl font-semibold mt-2">
              {(totalImpact * 100).toFixed(0)}%
            </div>
            <div className="text-[11px] text-zinc-500 mt-1">
              {removed.size} node(s) removed
            </div>
          </div>
          <DependencyMap nodes={nodes} />
        </div>
      </div>
    </div>
  );
}
