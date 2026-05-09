/** Reserved for runtime-generated filter chips — wired in by generative tree. */
export default function DynamicFilters({ filters = [], onChange }) {
  if (!filters.length) return null;
  return (
    <div className="flex flex-wrap gap-2 mb-3">
      {filters.map((f) => (
        <button
          key={f.id}
          onClick={() => onChange?.(f.id)}
          className="text-[11px] px-2.5 py-1 rounded-full border border-zinc-800
                     bg-zinc-900/60 hover:border-accent/40 text-zinc-300"
        >
          {f.label}
        </button>
      ))}
    </div>
  );
}
