/**
 * Tiny WebSocket client for the AG-UI streaming endpoint.
 * Usage:
 *   const sock = createAgentSocket({
 *     onReasoning: (text) => ...,
 *     onUiChunk: (data) => ...,
 *     onComplete: (result) => ...,
 *     onError: (err) => ...,
 *   });
 *   sock.send("Who are the bottlenecks?");
 */
const WS_BASE =
  import.meta.env.VITE_WS_BASE ||
  (typeof window !== "undefined" && window.location.origin.startsWith("https")
    ? "wss://localhost:8001"
    : "ws://localhost:8001");

export function createAgentSocket({
  onReasoning,
  onUiChunk,
  onComplete,
  onError,
  onOpen,
  onClose,
} = {}) {
  let ws = new WebSocket(`${WS_BASE}/ws/stream`);

  ws.onopen = () => onOpen?.();
  ws.onclose = () => onClose?.();
  ws.onerror = (e) => onError?.(e);
  ws.onmessage = (msg) => {
    try {
      const evt = JSON.parse(msg.data);
      switch (evt.event) {
        case "reasoning":
          onReasoning?.(evt.data);
          break;
        case "ui_chunk":
          onUiChunk?.(evt.data);
          break;
        case "complete":
          onComplete?.(evt.data);
          break;
        case "error":
          onError?.(evt.data);
          break;
        default:
          break;
      }
    } catch (e) {
      onError?.(e);
    }
  };

  return {
    send: (query) => {
      if (ws.readyState !== WebSocket.OPEN) return false;
      ws.send(JSON.stringify({ query }));
      return true;
    },
    close: () => ws.close(),
    raw: () => ws,
  };
}
