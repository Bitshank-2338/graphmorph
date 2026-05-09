import { useState } from "react";

import WorkspaceLayout from "../components/layout/WorkspaceLayout";
import RuntimeStream from "../components/runtime/RuntimeStream";
import ChatPanel from "../components/runtime/ChatPanel";
import UploadBox from "../components/upload/UploadBox";
import DynamicRenderer from "../renderer/DynamicRenderer";
import { useAgent } from "../hooks/useAgent";

export default function WorkspacePage() {
  const [messages, setMessages] = useState([]);
  const [schema, setSchema] = useState(null);

  const pushReasoning = (text) => {
    if (!text) return;
    setMessages((prev) => [...prev, text]);
  };

  const { ask, connected, busy } = useAgent({
    onSchema: setSchema,
    onReasoning: pushReasoning,
  });

  return (
    <WorkspaceLayout
      connected={connected}
      left={<RuntimeStream messages={messages} busy={busy} />}
      center={
        <div className="space-y-5">
          <UploadBox onSchema={setSchema} onReasoning={pushReasoning} />
          <DynamicRenderer schema={schema} />
        </div>
      }
      right={<ChatPanel onAsk={ask} busy={busy} />}
    />
  );
}
