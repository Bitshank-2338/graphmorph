import { motion } from "framer-motion";

export default function Header({ connected }) {
  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-border bg-panel/60 backdrop-blur">
      <div className="flex items-center gap-3">
        <motion.div
          initial={{ rotate: 0 }}
          animate={{ rotate: 360 }}
          transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
          className="w-7 h-7 rounded-md border border-accent/40"
          style={{
            background:
              "conic-gradient(from 0deg, #7c5cff, #2d2256, #7c5cff)",
          }}
        />
        <div>
          <div className="text-sm font-semibold tracking-wide">GraphMorph</div>
          <div className="text-[11px] text-zinc-500">
            Runtime graph-native interfaces
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2 text-xs text-zinc-400">
        <span
          className={`w-2 h-2 rounded-full ${
            connected ? "bg-emerald-400" : "bg-zinc-600"
          } animate-pulse-slow`}
        />
        {connected ? "Agent stream live" : "Agent: HTTP fallback"}
      </div>
    </header>
  );
}
