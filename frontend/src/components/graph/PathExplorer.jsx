import GraphExplorer from "./GraphExplorer";

/** Path-focused view (used when query type is shortest path). */
export default function PathExplorer({ data }) {
  return (
    <div>
      <div className="mb-4">
        <div className="text-xl font-semibold">{data.title}</div>
        {data.subtitle && (
          <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
        )}
      </div>
      <GraphExplorer nodes={data.nodes} edges={data.edges} height={460} />
    </div>
  );
}
