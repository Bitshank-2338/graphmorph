import { motion } from "framer-motion";
import InsightCards from "./InsightCards";

export default function SkillGapGrid({ data }) {
  const skills = data.skills || [];
  return (
    <div>
      <div className="mb-4">
        <div className="text-xl font-semibold">{data.title}</div>
        {data.subtitle && (
          <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
        )}
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {skills.map((s, i) => {
          const pct = Math.max(0, Math.min(100, s.coverage));
          const tone =
            pct < 25
              ? "bg-red-900/30 border-red-800"
              : pct < 60
              ? "bg-amber-900/20 border-amber-800"
              : "bg-emerald-900/20 border-emerald-800";
          return (
            <motion.div
              key={s.name}
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.03 }}
              className={`border rounded-2xl p-4 ${tone}`}
            >
              <div className="text-sm font-semibold">{s.name}</div>
              <div className="text-[11px] text-zinc-400 mt-0.5">
                {s.headcount} {s.headcount === 1 ? "person" : "people"}
              </div>
              <div className="mt-3 h-2 bg-black/40 rounded-full overflow-hidden">
                <div
                  className="h-full bg-accent"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <div className="text-[11px] text-zinc-300 mt-1">{pct}% coverage</div>
            </motion.div>
          );
        })}
      </div>
      <InsightCards insights={data.insights} />
    </div>
  );
}
