import { motion } from "framer-motion";
import InsightCards from "./InsightCards";

const TONE = {
  critical: "from-red-600/40 to-red-900/20 border-red-700/60 text-red-100",
  high:     "from-orange-600/30 to-orange-900/10 border-orange-700/50 text-orange-100",
  medium:   "from-amber-500/20 to-amber-900/10 border-amber-700/40 text-amber-100",
  low:      "from-emerald-500/15 to-emerald-900/10 border-emerald-700/40 text-emerald-100",
};

export default function RiskMatrix({ data }) {
  const nodes = data.nodes || [];
  return (
    <div>
      <Header data={data} />
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {nodes.map((n, i) => (
          <motion.div
            key={n.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
            className={`bg-gradient-to-br ${TONE[n.risk] || TONE.medium}
                        border rounded-2xl p-4 relative overflow-hidden`}
          >
            <div className="text-xs uppercase tracking-widest opacity-70">
              {n.risk}
            </div>
            <div className="text-lg font-semibold mt-1">{n.label || n.id}</div>
            <div className="text-xs opacity-80 mt-2">
              {n.connections} connections
            </div>
            <div className="mt-3 h-1.5 bg-black/30 rounded-full overflow-hidden">
              <div
                className="h-full bg-white/70"
                style={{ width: `${Math.round((n.metric || 0) * 100)}%` }}
              />
            </div>
          </motion.div>
        ))}
      </div>
      <InsightCards insights={data.insights} />
    </div>
  );
}

function Header({ data }) {
  return (
    <div className="mb-4">
      <div className="text-xl font-semibold">{data.title}</div>
      {data.subtitle && (
        <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
      )}
    </div>
  );
}
