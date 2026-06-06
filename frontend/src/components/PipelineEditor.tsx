"use client";

import Editor from "@monaco-editor/react";

type Props = {
  value: string;
  onChange: (value: string) => void;
};

export default function PipelineEditor({
  value,
  onChange,
}: Props) {
  return (
    <div className="h-[500px] border rounded">
      <Editor
        height="500px"
        defaultLanguage="json"
        value={value}
        onChange={(v) => onChange(v || "")}
        theme="vs-dark"
      />
    </div>
  );
}