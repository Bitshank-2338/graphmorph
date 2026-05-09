import { useEffect, useRef, useState, useCallback } from "react";
import { createAgentSocket } from "../services/socket";
import { askAgent } from "../services/api";

/**
 * useAgent — manages the live agent session.
 * Tries WebSocket first, falls back to plain HTTP POST.
 */
export function useAgent({ onSchema, onReasoning } = {}) {
  const sockRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const sock = createAgentSocket({
      onOpen: () => setConnected(true),
      onClose: () => setConnected(false),
      onReasoning: (text) => onReasoning?.(text),
      onUiChunk: () => {},
      onComplete: (result) => {
        setBusy(false);
        if (result?.ui_schema) onSchema?.(result.ui_schema);
      },
      onError: (e) => {
        setBusy(false);
        console.warn("[useAgent] socket error:", e);
      },
    });
    sockRef.current = sock;
    return () => sock.close();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const ask = useCallback(
    async (query) => {
      if (!query?.trim()) return;
      setBusy(true);
      onReasoning?.(`> ${query}`);
      const sent = sockRef.current?.send(query);
      if (sent) return;

      // Fallback: HTTP
      try {
        const result = await askAgent(query);
        result.reasoning?.forEach((r) => onReasoning?.(r));
        if (result.ui_schema) onSchema?.(result.ui_schema);
      } catch (e) {
        onReasoning?.(`Error: ${e.message}`);
      } finally {
        setBusy(false);
      }
    },
    [onReasoning, onSchema]
  );

  return { ask, connected, busy };
}
