import { motion } from "framer-motion";

export default function ClusterGraph({ data }) {
  const clusters = data.nodes || [];
  return (
    <div>
      <div className="mb-4">
        <div className="text-xl font-semibold">{data.title}</div>
        {data.subtitle && (
          <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
        )}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {clusters.map((c, i) => (
          <motion.div
            key={c.id}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-4"
          >
            <div className="flex justify-between items-baseline">
              <div className="font-semibold text-base">{c.label}</div>
              <div className="text-[11px] text-zinc-500">{c.size} members</div>
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {(c.members || []).slice(0, 12).map((m) => (
                <span
                  key={m}
                  className="text-[11px] bg-zinc-800/80 text-zinc-200 px-2 py-0.5 rounded-md"
                >
                  {m}
                </span>
              ))}
              {(c.members || []).length > 12 && (
                <span className="text-[11px] text-zinc-500">
                  +{c.members.length - 12} more
                </span>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
