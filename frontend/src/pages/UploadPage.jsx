import { useState } from "react";

import UploadBox from "../components/upload/UploadBox";
import DynamicRenderer from "../renderer/DynamicRenderer";

export default function UploadPage() {
  const [messages, setMessages] = useState([]);
  const [schema, setSchema] = useState(null);

  return (
    <div className="min-h-screen bg-bg px-6 py-10 text-zinc-100">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8">
          <div className="text-[11px] uppercase tracking-[0.28em] text-accent/80">
            GraphMorph
          </div>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight text-white">
            Upload a dataset and generate a graph-native workspace.
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-zinc-400">
            Load a CSV or spreadsheet, transform it into a graph, and hand the result
            to the runtime UI renderer.
          </p>
        </div>

        <UploadBox
          onSchema={setSchema}
          onReasoning={(text) => setMessages((prev) => [...prev, text])}
        />

        {messages.length > 0 && (
          <div className="mb-5 rounded-2xl border border-zinc-800 bg-panel/40 p-4">
            <div className="mb-2 text-[11px] uppercase tracking-widest text-zinc-500">
              Upload log
            </div>
            <div className="space-y-1 text-sm text-zinc-300">
              {messages.map((message, index) => (
                <div key={`${message}-${index}`}>{message}</div>
              ))}
            </div>
          </div>
        )}

        <DynamicRenderer schema={schema} />
      </div>
    </div>
  );
}
