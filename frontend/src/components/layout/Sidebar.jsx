/**
 * Generic sidebar wrapper used for left + right panels.
 */
import { cn } from "../../lib/cn";

export default function Sidebar({ side = "left", title, children, className }) {
  return (
    <aside
      className={cn(
        "flex flex-col bg-panel/40 backdrop-blur",
        side === "left" ? "border-r" : "border-l",
        "border-border",
        className
      )}
    >
      {title && (
        <div className="px-4 py-3 text-[11px] uppercase tracking-widest text-zinc-500 border-b border-border">
          {title}
        </div>
      )}
      <div className="flex-1 overflow-y-auto p-3">{children}</div>
    </aside>
  );
}
