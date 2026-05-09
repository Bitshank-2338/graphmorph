export default function InsightCards({ insights }) {
  if (!insights?.length) return null;
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
      {insights.map((t, i) => (
        <div
          key={i}
          className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-3 text-sm text-zinc-200"
        >
          <span className="text-accent mr-2">●</span>
          {t}
        </div>
      ))}
    </div>
  );
}
