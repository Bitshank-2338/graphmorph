import { motion, AnimatePresence } from "framer-motion";

/** Single line in the reasoning stream. */
export default function AgentThoughts({ text, idx }) {
  const isUser = text?.startsWith?.("> ");
  const isError = text?.toLowerCase?.().includes("error") || text?.toLowerCase?.().includes("fail");
  return (
    <AnimatePresence>
      <motion.div
        key={idx}
        initial={{ opacity: 0, x: -6 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.18 }}
        className={`mb-2 text-[12px] leading-relaxed font-mono px-2 py-1.5 rounded-md border ${
          isUser
            ? "bg-accent/10 border-accent/30 text-accent"
            : isError
            ? "bg-red-950/40 border-red-900/60 text-red-300"
            : "bg-zinc-900/60 border-zinc-800 text-zinc-300"
        }`}
      >
        {text}
      </motion.div>
    </AnimatePresence>
  );
}
