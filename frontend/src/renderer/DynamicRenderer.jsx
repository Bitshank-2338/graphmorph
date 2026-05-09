/**
 * DynamicRenderer — the HEART of GraphMorph.
 *
 * Hybrid mode:
 *   1) If ui_type matches a known template, render the typed component.
 *   2) If ui_type === "generative", hand off to GenerativeRenderer to interpret
 *      the LLM's primitive tree.
 *   3) Otherwise, render a graceful empty state.
 *
 * This file is intentionally thin — all UI lives in the components it routes to.
 */
import { motion, AnimatePresence } from "framer-motion";

import RiskMatrix from "../components/ui/RiskMatrix";
import SkillGapGrid from "../components/ui/SkillGapGrid";
import SimulationPanel from "../components/ui/SimulationPanel";
import RelationshipExplorer from "../components/graph/RelationshipExplorer";
import ClusterGraph from "../components/graph/ClusterGraph";
import PathExplorer from "../components/graph/PathExplorer";
import GenerativeRenderer from "./GenerativeRenderer";

const REGISTRY = {
  risk_matrix: RiskMatrix,
  skill_gap_grid: SkillGapGrid,
  simulation_workspace: SimulationPanel,
  relationship_explorer: RelationshipExplorer,
  cluster_explorer: ClusterGraph,
  path_explorer: PathExplorer,
  generative: GenerativeRenderer,
};

export default function DynamicRenderer({ schema }) {
  if (!schema) {
    return (
      <div className="rounded-2xl border border-dashed border-zinc-800 p-10 text-center text-zinc-500">
        No interface generated yet. Upload a dataset or ask the agent a question.
      </div>
    );
  }

  const Comp = REGISTRY[schema.ui_type];

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={schema.ui_type + (schema.title || "") + Date.now()}
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.25 }}
      >
        {Comp ? (
          <Comp data={schema} />
        ) : (
          <div className="text-zinc-500 text-sm">
            Unknown ui_type:{" "}
            <code className="text-accent">{schema.ui_type}</code>
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
