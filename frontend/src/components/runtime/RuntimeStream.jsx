import { useEffect, useRef } from "react";
import AgentThoughts from "./AgentThoughts";
import StreamingStatus from "./StreamingStatus";

export default function RuntimeStream({ messages, busy }) {
  const endRef = useRef(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="h-full flex flex-col">
      <StreamingStatus busy={busy} />
      <div className="flex-1 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <div className="text-[11px] text-zinc-600 italic">
            Awaiting input. Upload a dataset or ask the agent a question.
          </div>
        )}
        {messages.map((m, i) => (
          <AgentThoughts key={i} text={m} idx={i} />
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}
