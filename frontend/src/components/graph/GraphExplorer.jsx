import { useMemo } from "react";
import ReactFlow, { Background, Controls, MiniMap } from "reactflow";
import "reactflow/dist/style.css";

const TYPE_COLOR = {
  Person: "#7c5cff",
  Department: "#5cb1ff",
  Skill: "#5cffae",
  Customer: "#ff5ca8",
  Product: "#ffb05c",
  Category: "#fff15c",
  Region: "#5cfff1",
  Entity: "#bbb",
};

export default function GraphExplorer({ nodes = [], edges = [], height = 520 }) {
  const styledNodes = useMemo(
    () =>
      nodes.map((n) => ({
        ...n,
        style: {
          background: "#101012",
          border: `1.5px solid ${TYPE_COLOR[n.data?.type] || "#2a2a30"}`,
          color: "#fff",
          borderRadius: 10,
          padding: "6px 10px",
          fontSize: 11,
          minWidth: 60,
        },
      })),
    [nodes]
  );

  return (
    <div
      style={{ height }}
      className="rounded-2xl border border-zinc-800 bg-bg overflow-hidden"
    >
      <ReactFlow
        nodes={styledNodes}
        edges={edges}
        fitView
        fitViewOptions={{ padding: 0.25 }}
        nodesDraggable
        nodesConnectable={false}
        proOptions={{ hideAttribution: true }}
      >
        <Background gap={24} size={1} color="#1c1c20" />
        <Controls showInteractive={false} />
        <MiniMap
          nodeColor={(n) => TYPE_COLOR[n.data?.type] || "#444"}
          maskColor="rgba(10,10,11,0.8)"
          style={{ background: "#101012", border: "1px solid #1c1c20" }}
        />
      </ReactFlow>
    </div>
  );
}
