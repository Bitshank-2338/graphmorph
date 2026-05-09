/** Compact list of high-dependency nodes — used inside simulations. */
export default function DependencyMap({ nodes = [] }) {
  return (
    <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4">
      <div className="text-[11px] uppercase tracking-widest text-zinc-500 mb-2">
        Top dependencies
      </div>
      <div className="space-y-1.5">
        {nodes.slice(0, 8).map((n) => (
          <div
            key={n.id}
            className="flex justify-between items-center text-sm text-zinc-200"
          >
            <span>{n.label || n.id}</span>
            <span className="text-xs text-accent">
              {n.connections ?? n.impact}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
