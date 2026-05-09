/**
 * GenerativeRenderer — interprets a recursive primitive tree emitted by the LLM.
 *
 * Whitelists the `kind` field. Any unknown kind renders as a small placeholder
 * so a malicious or malformed schema cannot inject arbitrary HTML.
 *
 * This is the piece that makes the "AI generates the UI" claim literally true:
 * the agent decides which primitives to nest, with what props, in what order.
 */
import { motion } from "framer-motion";
import GraphExplorer from "../components/graph/GraphExplorer";

const TONE_BG = {
  neutral: "bg-zinc-900/60 border-zinc-800",
  info:    "bg-blue-900/30 border-blue-800/60",
  success: "bg-emerald-900/30 border-emerald-800/60",
  warning: "bg-amber-900/30 border-amber-800/60",
  danger:  "bg-red-900/30 border-red-800/60",
};

function renderChildren(children) {
  if (!children) return null;
  return children.map((c, i) => <Node key={i} node={c} />);
}

function Node({ node }) {
  if (!node || typeof node !== "object") return null;
  const { kind, props = {}, children } = node;

  switch (kind) {
    case "container":
      return (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className={`flex ${
            props.direction === "row" ? "flex-row" : "flex-col"
          }`}
          style={{
            gap: props.gap ?? 12,
            padding: props.padding ?? 0,
          }}
        >
          {renderChildren(children)}
        </motion.div>
      );

    case "grid":
      return (
        <div
          className="grid"
          style={{
            gridTemplateColumns: `repeat(${props.cols || 3}, minmax(0, 1fr))`,
            gap: props.gap ?? 12,
          }}
        >
          {renderChildren(children)}
        </div>
      );

    case "card":
      return (
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`border rounded-2xl p-4 ${
            TONE_BG[props.tone] || TONE_BG.neutral
          }`}
        >
          {props.title && (
            <div className="text-sm font-semibold mb-1.5">{props.title}</div>
          )}
          {renderChildren(children)}
        </motion.div>
      );

    case "heading": {
      const Tag = `h${Math.min(Math.max(props.level || 2, 1), 4)}`;
      const cls = {
        h1: "text-2xl font-semibold",
        h2: "text-xl font-semibold",
        h3: "text-lg font-medium",
        h4: "text-sm font-medium uppercase tracking-widest text-zinc-400",
      }[Tag];
      return <Tag className={cls}>{props.text}</Tag>;
    }

    case "text":
      return (
        <p className={`text-sm ${props.muted ? "text-zinc-500" : "text-zinc-200"}`}>
          {props.text}
        </p>
      );

    case "metric":
      return (
        <div>
          <div className="text-[11px] uppercase tracking-widest text-zinc-500">
            {props.label}
          </div>
          <div className="text-2xl font-semibold mt-0.5">
            {props.value}
            {props.suffix && (
              <span className="text-sm text-zinc-400 ml-1">{props.suffix}</span>
            )}
          </div>
        </div>
      );

    case "badge":
      return (
        <span
          className={`text-[11px] px-2 py-0.5 rounded-full border ${
            TONE_BG[props.tone] || TONE_BG.neutral
          }`}
        >
          {props.text}
        </span>
      );

    case "heatmap_cell": {
      const v = Math.max(0, Math.min(1, props.value ?? 0));
      const bg = `rgba(124, 92, 255, ${0.15 + v * 0.65})`;
      return (
        <div
          className="rounded-lg p-3 border border-accent/20 text-center"
          style={{ background: bg }}
        >
          <div className="text-[11px] text-zinc-300">{props.label}</div>
          <div className="text-sm font-semibold">{Math.round(v * 100)}%</div>
        </div>
      );
    }

    case "list":
      return (
        <ul className="space-y-1 text-sm text-zinc-200">
          {(props.items || []).map((it, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-accent">›</span>
              <span>{it}</span>
            </li>
          ))}
        </ul>
      );

    case "divider":
      return <div className="h-px bg-zinc-800 my-2" />;

    case "slider":
      return (
        <div>
          <div className="flex justify-between text-[11px] text-zinc-400 mb-1">
            <span>{props.label}</span>
            <span>{props.value}</span>
          </div>
          <input
            type="range"
            min={props.min ?? 0}
            max={props.max ?? 100}
            defaultValue={props.value ?? 50}
            className="w-full accent-[#7c5cff]"
          />
        </div>
      );

    case "graph":
      return (
        <GraphExplorer
          nodes={props.nodes || []}
          edges={props.edges || []}
          height={props.height || 360}
        />
      );

    case "button":
      return (
        <button className="bg-accent hover:bg-accent/90 text-white text-sm px-3 py-1.5 rounded-lg">
          {props.label}
        </button>
      );

    default:
      return (
        <div className="text-[11px] text-zinc-600 italic border border-zinc-900 rounded-md px-2 py-1 inline-block">
          unknown:{kind}
        </div>
      );
  }
}

export default function GenerativeRenderer({ data }) {
  return (
    <div>
      <div className="mb-4">
        <div className="text-xl font-semibold">{data.title}</div>
        {data.subtitle && (
          <div className="text-xs text-zinc-500 mt-1">{data.subtitle}</div>
        )}
      </div>
      <Node node={data.tree} />
    </div>
  );
}
