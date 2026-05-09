import { useRef, useState } from "react";
import { uploadDataset } from "../../services/api";

export default function UploadBox({ onSchema, onReasoning }) {
  const inputRef = useRef(null);
  const [busy, setBusy] = useState(false);
  const [filename, setFilename] = useState(null);

  const handleFile = async (file) => {
    if (!file) return;
    setFilename(file.name);
    setBusy(true);
    onReasoning?.(`Uploading ${file.name}...`);
    try {
      const res = await uploadDataset(file);
      res.reasoning?.forEach((r) => onReasoning?.(r));
      onSchema?.(res.ui_schema);
    } catch (e) {
      onReasoning?.(`Upload failed: ${e.message}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        handleFile(e.dataTransfer.files?.[0]);
      }}
      onClick={() => inputRef.current?.click()}
      className="border border-dashed border-zinc-700 hover:border-accent/60 transition
                 rounded-2xl p-6 mb-5 cursor-pointer bg-panel/40"
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv,.xlsx,.xls"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm font-medium">
            {busy ? "Transforming dataset..." : filename || "Drop a CSV / XLSX to begin"}
          </div>
          <div className="text-[11px] text-zinc-500 mt-0.5">
            We'll detect entities, build a graph, and load Neo4j automatically.
          </div>
        </div>
        <div className="text-xs text-accent font-medium">
          {busy ? "..." : "Choose file"}
        </div>
      </div>
    </div>
  );
}
