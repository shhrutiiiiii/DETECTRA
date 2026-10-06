"use client";

import React, { useCallback, useRef, useState } from "react";
import { Upload, X, AlertCircle, FileText, FileType2 } from "lucide-react";

interface FileUploadZoneProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClear: () => void;
  disabled?: boolean;
}

const ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"];
const MAX_SIZE_MB = 10;

const EXT_CONFIG: Record<string, { icon: React.ReactNode; color: string; bg: string; label: string }> = {
  pdf: {
    icon: <FileType2 size={26} />,
    color: "#EF4444",
    bg: "rgba(239, 68, 68, 0.12)",
    label: "PDF Document",
  },
  docx: {
    icon: <FileText size={26} />,
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.12)",
    label: "Word Document",
  },
  txt: {
    icon: <FileText size={26} />,
    color: "#0E7490",
    bg: "rgba(14, 116, 144, 0.12)",
    label: "Text File",
  },
};

export default function FileUploadZone({
  onFileSelect,
  selectedFile,
  onClear,
  disabled,
}: FileUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    const ext = file.name.split(".").pop()?.toLowerCase() ?? "";
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      return `Unsupported format. Please upload .pdf, .docx, or .txt files.`;
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      return `File too large. Maximum size is ${MAX_SIZE_MB}MB.`;
    }
    return null;
  };

  const handleFile = (file: File) => {
    const err = validateFile(file);
    if (err) {
      setError(err);
      return;
    }
    setError(null);
    onFileSelect(file);
  };

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback(() => setIsDragging(false), []);

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  };

  if (selectedFile) {
    const ext = selectedFile.name.split(".").pop()?.toLowerCase() ?? "txt";
    const config = EXT_CONFIG[ext] ?? EXT_CONFIG.txt;
    return (
      <div
        className="glass-card p-6 md:p-8 animate-fade-in-up my-auto"
        style={{ borderColor: "var(--accent-primary)" }}
      >
        <div className="flex items-center gap-5">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-sm"
            style={{ background: config.bg, color: config.color }}
          >
            {config.icon}
          </div>
          <div className="flex-1 min-w-0 space-y-1">
            <p
              className="font-bold truncate text-base md:text-lg"
              style={{ color: "var(--text-primary)" }}
            >
              {selectedFile.name}
            </p>
            <div className="flex items-center gap-3 text-xs">
              <span
                className="font-bold px-3 py-0.5 rounded-full uppercase tracking-wider text-[11px]"
                style={{ background: config.bg, color: config.color }}
              >
                .{ext}
              </span>
              <span style={{ color: "var(--text-secondary)" }}>
                {formatSize(selectedFile.size)}
              </span>
              <span style={{ color: "var(--text-muted)" }}>
                • {config.label}
              </span>
            </div>
          </div>
          <button
            onClick={onClear}
            disabled={disabled}
            className="p-3 rounded-2xl transition-all hover:scale-110 cursor-pointer"
            style={{
              background: "rgba(239, 68, 68, 0.12)",
              color: "var(--red-ai)",
              border: "1px solid rgba(239, 68, 68, 0.25)",
            }}
          >
            <X size={18} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div
        className={`upload-zone p-14 md:p-20 text-center cursor-pointer transition-all duration-300 min-h-[340px] flex flex-col items-center justify-center ${
          isDragging ? "dragover" : ""
        }`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept=".pdf,.docx,.txt"
          onChange={onInputChange}
          disabled={disabled}
          id="file-upload-input"
        />

        <div className="flex flex-col items-center gap-6 my-auto">
          <div
            className="w-20 h-20 rounded-3xl flex items-center justify-center transition-transform hover:scale-105 shadow-lg"
            style={{
              background: "var(--subtle-bg)",
              border: "1px solid var(--border-primary)",
            }}
          >
            <Upload
              size={34}
              style={{
                color: isDragging ? "var(--accent-secondary)" : "var(--accent-primary)",
                transition: "color 0.2s ease",
              }}
            />
          </div>

          <div className="space-y-2">
            <p className="font-extrabold text-lg sm:text-xl" style={{ color: "var(--text-primary)" }}>
              {isDragging ? "Release file to upload" : "Drop your document here"}
            </p>
            <p className="text-sm font-normal" style={{ color: "var(--text-secondary)" }}>
              or{" "}
              <span
                className="font-bold underline underline-offset-4"
                style={{ color: "var(--accent-primary)" }}
              >
                browse local files from your device
              </span>
            </p>
          </div>

          <div className="flex items-center gap-2.5 flex-wrap justify-center pt-2">
            {ALLOWED_EXTENSIONS.map((ext) => {
              const cfg = EXT_CONFIG[ext];
              return (
                <span
                  key={ext}
                  className="px-3.5 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider flex items-center gap-1.5"
                  style={{
                    background: cfg.bg,
                    border: `1px solid ${cfg.color}35`,
                    color: cfg.color,
                  }}
                >
                  .{ext}
                </span>
              );
            })}
            <span className="text-xs font-semibold ml-2" style={{ color: "var(--text-muted)" }}>
              Max {MAX_SIZE_MB}MB per file
            </span>
          </div>
        </div>
      </div>

      {error && (
        <div
          className="flex items-center gap-3 mt-4 p-4.5 rounded-2xl text-sm animate-fade-in-up"
          style={{
            background: "rgba(239, 68, 68, 0.08)",
            border: "1px solid rgba(239, 68, 68, 0.25)",
            color: "var(--red-ai)",
          }}
        >
          <AlertCircle size={18} className="flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  );
}
