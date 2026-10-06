"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/Header";
import DocumentTypeSelector from "@/components/DocumentTypeSelector";
import FileUploadZone from "@/components/FileUploadZone";
import ResultsDashboard from "@/components/ResultsDashboard";
import { fetchDocumentTypes, analyzeFile, analyzeText } from "@/lib/api";
import { AnalysisResult, DocumentType } from "@/types";
import {
  Sparkles,
  Upload,
  AlignLeft,
  Loader2,
  AlertCircle,
  FileCheck,
  ShieldCheck,
  Brain,
  GraduationCap,
  Sliders,
} from "lucide-react";

type UploadMode = "file" | "text";

const PROFILE_WEIGHTS: Record<string, { perplexity: number; burstiness: number; vocabulary: number; focus: string }> = {
  essay: { perplexity: 45, burstiness: 30, vocabulary: 25, focus: "Academic Tone & Structure" },
  resume: { perplexity: 30, burstiness: 40, vocabulary: 30, focus: "Work History & Skill Bullets" },
  research: { perplexity: 50, burstiness: 25, vocabulary: 25, focus: "Citations & Formal Rigor" },
  cover_letter: { perplexity: 35, burstiness: 35, vocabulary: 30, focus: "Personal Narrative Voice" },
};

const HERO_FEATURES = [
  {
    icon: <Brain size={18} />,
    title: "Category NLP Profiles",
    desc: "Tuned perplexity & burstiness weights",
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.12)",
  },
  {
    icon: <ShieldCheck size={18} />,
    title: "Sentence Inspector",
    desc: "Color highlights with AI probability",
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.12)",
  },
  {
    icon: <FileCheck size={18} />,
    title: "Readability Suite",
    desc: "Flesch-Kincaid & Fog index scoring",
    color: "#0E7490",
    bg: "rgba(14, 116, 144, 0.12)",
  },
];

export default function Home() {
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [selectedType, setSelectedType] = useState<string>("essay");
  const [uploadMode, setUploadMode] = useState<UploadMode>("file");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pastedText, setPastedText] = useState<string>("");
  const [status, setStatus] = useState<"idle" | "uploading" | "analyzing" | "done" | "error">("idle");
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDocumentTypes()
      .then((types) => {
        if (types && types.length > 0) {
          setDocumentTypes(types);
          setSelectedType(types[0].id);
        }
      })
      .catch(() => {
        setDocumentTypes([
          {
            id: "essay",
            name: "Homework / Assignment Essay",
            description: "Optimized for academic tone & structure",
          },
          {
            id: "resume",
            name: "Resume / CV",
            description: "Optimized for work history & skill bullets",
          },
          {
            id: "research",
            name: "Research Paper / Thesis",
            description: "Optimized for citations & academic rigor",
          },
          {
            id: "cover_letter",
            name: "Cover Letter / SOP",
            description: "Optimized for personal narrative voice",
          },
        ]);
      });
  }, []);

  const wordCount = pastedText
    .trim()
    .split(/\s+/)
    .filter((w) => w.length > 0).length;

  const canAnalyze =
    uploadMode === "file" ? selectedFile !== null : wordCount >= 20;

  const handleAnalyze = async () => {
    if (!canAnalyze) return;
    setError(null);

    try {
      if (uploadMode === "file" && selectedFile) {
        setStatus("uploading");
        setUploadProgress(10);
        const res = await analyzeFile(selectedFile, selectedType, (pct) => {
          setUploadProgress(pct);
          if (pct >= 95) setStatus("analyzing");
        });
        setStatus("analyzing");
        await new Promise((r) => setTimeout(r, 400));
        setResult(res);
        setStatus("done");
      } else if (uploadMode === "text" && pastedText) {
        setStatus("analyzing");
        const res = await analyzeText(pastedText, selectedType);
        setResult(res);
        setStatus("done");
      }
    } catch (err: unknown) {
      setStatus("error");
      if (err && typeof err === "object" && "response" in err) {
        const responseData = (err as { response?: { data?: { detail?: string } } }).response?.data;
        setError(responseData?.detail || "Failed to analyze document. Please check network connection.");
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred during analysis.");
      }
    }
  };

  const handleReset = () => {
    setResult(null);
    setStatus("idle");
    setSelectedFile(null);
    setPastedText("");
    setError(null);
  };

  const isLoading = status === "uploading" || status === "analyzing";
  const currentWeights = PROFILE_WEIGHTS[selectedType] ?? PROFILE_WEIGHTS.essay;

  return (
    <div className="bg-grid min-h-screen flex flex-col relative overflow-hidden transition-colors duration-300">
      {/* Background Ambient Orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      {/* Header */}
      <Header />

      <main className="relative z-10 max-w-[1700px] mx-auto px-6 sm:px-10 lg:px-12 py-10 md:py-12 flex-1 w-full flex flex-col justify-between">
        {result && status === "done" ? (
          /* ─── Results View (Full Screen Expansive View) ─── */
          <div className="w-full animate-fade-in-up">
            <ResultsDashboard result={result} onReset={handleReset} />
          </div>
        ) : (
          /* ─── Main Workspace ─── */
          <div className="space-y-12 my-auto">
            {/* Top Hero Banner */}
            <div className="flex flex-col lg:flex-row items-center justify-between gap-8 pb-8 border-b border-[#06B6D4]/15">
              {/* Top Left Title Area */}
              <div className="max-w-2xl text-left flex flex-col gap-[0.2mm] pt-1">
                <div
                  className="inline-flex items-center gap-2.5 px-4.5 py-2 rounded-full text-xs font-extrabold tracking-widest uppercase shadow-sm mb-[0.2mm] w-fit"
                  style={{
                    background: "var(--subtle-bg)",
                    border: "1px solid var(--border-primary)",
                    color: "var(--accent-primary)",
                  }}
                >
                  <GraduationCap size={16} />
                  DETECTRA INTEGRITY AI SUITE
                </div>

                <h1
                  className="text-4xl sm:text-5xl font-black tracking-tight leading-[1.08] mb-[0.2mm]"
                  style={{ fontFamily: "'Fira Code', monospace" }}
                >
                  Detect <span className="gradient-text">AI Generation</span>
                  <br className="hidden sm:inline" /> across any document.
                </h1>

                <p className="text-sm sm:text-base font-normal leading-relaxed max-w-xl mt-[0.2mm]" style={{ color: "var(--text-secondary)" }}>
                  Multi-signal statistical NLP engine tailored for student assignments, resumes, research papers, and SOPs.
                </p>
              </div>

              {/* Upper Right 3 Feature Boxes */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full lg:w-auto flex-shrink-0">
                {HERO_FEATURES.map((f) => (
                  <div
                    key={f.title}
                    className="flex items-start gap-4 p-4.5 rounded-2xl text-left shadow-sm min-w-[210px]"
                    style={{
                      background: "var(--bg-glass)",
                      border: "1px solid var(--border-primary)",
                    }}
                  >
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5" style={{ background: f.bg, color: f.color }}>
                      {f.icon}
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-extrabold truncate" style={{ color: "var(--text-primary)" }}>{f.title}</div>
                      <div className="text-[11px] leading-snug mt-1" style={{ color: "var(--text-secondary)" }}>{f.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ─── Centered Grid with 1 Block Margin on Left and Right (Cols 2–11) ─── */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 items-stretch">
              {/* STEP 1 (Box 1): Category Selection - Starts at Col 2 (Leaves 1 Block on Left) */}
              <div className="lg:col-span-5 lg:col-start-2 flex flex-col justify-between">
                <div className="glass-card p-7 sm:p-8 md:p-9 flex flex-col justify-between h-full space-y-7 shadow-xl">
                  <div className="space-y-6">
                    <div className="flex items-center justify-between border-b pb-5" style={{ borderColor: "var(--border-primary)" }}>
                      <div className="flex items-center gap-3">
                        <span
                          className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-extrabold"
                          style={{
                            background: "rgba(6, 182, 212, 0.15)",
                            color: "var(--accent-primary)",
                          }}
                        >
                          1
                        </span>
                        <span className="text-xs font-extrabold tracking-widest uppercase" style={{ color: "var(--text-secondary)" }}>
                          Select Document Category
                        </span>
                      </div>
                      <span className="text-xs font-semibold" style={{ color: "var(--text-muted)" }}>
                        Step 1 of 2
                      </span>
                    </div>

                    {/* Document Selector List */}
                    <DocumentTypeSelector
                      documentTypes={documentTypes}
                      selected={selectedType}
                      onChange={setSelectedType}
                      disabled={isLoading}
                    />
                  </div>

                  {/* Active Profile Parameter Card */}
                  <div className="rounded-2xl p-5 md:p-6 space-y-4" style={{ background: "var(--subtle-bg)", border: "1px solid var(--border-primary)" }}>
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-extrabold flex items-center gap-2" style={{ color: "var(--text-primary)" }}>
                        <Sliders size={15} style={{ color: "var(--accent-primary)" }} />
                        NLP Tuning Parameters
                      </span>
                      <span className="text-xs font-extrabold px-3 py-1 rounded-full" style={{ background: "rgba(6, 182, 212, 0.12)", color: "var(--accent-primary)" }}>
                        {currentWeights.focus}
                      </span>
                    </div>

                    <div className="grid grid-cols-3 gap-3.5 text-center">
                      <div className="p-3.5 rounded-xl" style={{ background: "var(--bg-glass)" }}>
                        <div className="text-base font-black tabular-nums" style={{ color: "var(--accent-primary)" }}>{currentWeights.perplexity}%</div>
                        <div className="text-[11px] mt-0.5 font-semibold" style={{ color: "var(--text-muted)" }}>Perplexity</div>
                      </div>
                      <div className="p-3.5 rounded-xl" style={{ background: "var(--bg-glass)" }}>
                        <div className="text-base font-black tabular-nums" style={{ color: "var(--accent-secondary)" }}>{currentWeights.burstiness}%</div>
                        <div className="text-[11px] mt-0.5 font-semibold" style={{ color: "var(--text-muted)" }}>Burstiness</div>
                      </div>
                      <div className="p-3.5 rounded-xl" style={{ background: "var(--bg-glass)" }}>
                        <div className="text-base font-black tabular-nums" style={{ color: "var(--accent-cyan)" }}>{currentWeights.vocabulary}%</div>
                        <div className="text-[11px] mt-0.5 font-semibold" style={{ color: "var(--text-muted)" }}>Vocabulary</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* STEP 2 (Box 2): Content Input Workspace (Spans 5 Cols, Leaves 1 Block on Right) */}
              <div className="lg:col-span-5 flex flex-col justify-between">
                <div className="glass-card p-7 sm:p-8 md:p-9 flex flex-col justify-between h-full space-y-7 shadow-xl">
                  <div className="space-y-6">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-5" style={{ borderColor: "var(--border-primary)" }}>
                      <div className="flex items-center gap-3">
                        <span
                          className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-extrabold"
                          style={{
                            background: "rgba(6, 182, 212, 0.15)",
                            color: "var(--accent-primary)",
                          }}
                        >
                          2
                        </span>
                        <span className="text-xs font-extrabold tracking-widest uppercase" style={{ color: "var(--text-secondary)" }}>
                          Provide Document Content
                        </span>
                      </div>

                      {/* Mode Toggle Switch - Perfectly Aligned Buttons with Generous Padding */}
                      <div
                        className="p-1.5 rounded-2xl flex items-center gap-1.5 border shadow-sm self-start sm:self-auto"
                        style={{
                          background: "var(--subtle-bg)",
                          borderColor: "var(--border-primary)",
                        }}
                      >
                        {[
                          { id: "file" as UploadMode, icon: <Upload size={15} />, label: "Upload File" },
                          { id: "text" as UploadMode, icon: <AlignLeft size={15} />, label: "Paste Text" },
                        ].map((m) => (
                          <button
                            key={m.id}
                            id={`mode-${m.id}`}
                            onClick={() => {
                              setUploadMode(m.id);
                              setError(null);
                            }}
                            disabled={isLoading}
                            className="flex items-center justify-center gap-2.5 px-4.5 py-2.5 rounded-xl text-xs font-extrabold transition-all duration-200 cursor-pointer text-center min-w-[125px]"
                            style={{
                              background: uploadMode === m.id ? "var(--accent-primary)" : "transparent",
                              color: uploadMode === m.id ? "#ffffff" : "var(--text-secondary)",
                              boxShadow: uploadMode === m.id ? "0 4px 14px rgba(6, 182, 212, 0.35)" : "none",
                            }}
                          >
                            <span className="flex-shrink-0 flex items-center justify-center">{m.icon}</span>
                            <span className="leading-none">{m.label}</span>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Content Input Workspace */}
                    <div className="min-h-[280px] flex flex-col justify-center">
                      {uploadMode === "file" && (
                        <FileUploadZone
                          onFileSelect={setSelectedFile}
                          selectedFile={selectedFile}
                          onClear={() => setSelectedFile(null)}
                          disabled={isLoading}
                        />
                      )}

                      {uploadMode === "text" && (
                        <div className="space-y-4">
                          <textarea
                            id="text-input-area"
                            value={pastedText}
                            onChange={(e) => setPastedText(e.target.value)}
                            disabled={isLoading}
                            placeholder="Paste document text here… (minimum 20 words required for confidence scoring)"
                            rows={12}
                            className="w-full rounded-2xl px-6 py-5 text-sm sm:text-base transition-all leading-relaxed outline-none"
                            style={{
                              background: "var(--input-bg)",
                              border: "1px solid var(--border-primary)",
                              color: "var(--text-primary)",
                              boxShadow: "inset 0 2px 4px rgba(0,0,0,0.05)",
                              lineHeight: "1.75",
                            }}
                          />
                          <div className="flex items-center justify-between px-1">
                            <span className="text-xs font-semibold" style={{ color: "var(--text-muted)" }}>
                              Supports PDF, DOCX, and TXT plain text
                            </span>
                            <span
                              className="text-xs font-extrabold tabular-nums px-3.5 py-1 rounded-full"
                              style={{
                                background: wordCount >= 20 ? "rgba(16, 185, 129, 0.12)" : "var(--subtle-bg)",
                                color: wordCount >= 20 ? "var(--green-human)" : wordCount > 0 ? "var(--orange-ai)" : "var(--text-muted)",
                              }}
                            >
                              {wordCount} / 20 words {wordCount >= 20 ? "✓ Ready" : "minimum"}
                            </span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Status / Error Alerts */}
                  {status === "uploading" && (
                    <div className="animate-fade-in-up space-y-2">
                      <div className="flex justify-between text-xs font-semibold" style={{ color: "var(--text-secondary)" }}>
                        <span>Uploading document…</span>
                        <span className="tabular-nums">{uploadProgress}%</span>
                      </div>
                      <div className="progress-bar-track" style={{ height: 6 }}>
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${uploadProgress}%`,
                            background: "linear-gradient(90deg, #A5F3FC, #06B6D4, #0E7490)",
                          }}
                        />
                      </div>
                    </div>
                  )}

                  {status === "analyzing" && (
                    <div
                      className="flex items-center gap-4 p-4.5 rounded-2xl animate-fade-in-up"
                      style={{
                        background: "rgba(6, 182, 212, 0.08)",
                        border: "1px solid var(--border-glow)",
                      }}
                    >
                      <Loader2 size={20} className="animate-spin-slow flex-shrink-0" style={{ color: "var(--accent-primary)" }} />
                      <div>
                        <div className="font-bold text-xs sm:text-sm" style={{ color: "var(--text-primary)" }}>
                          Running Detection Engine…
                        </div>
                        <div className="text-xs mt-0.5" style={{ color: "var(--text-secondary)" }}>
                          Evaluating sentence perplexity, burstiness variation, and phrase density
                        </div>
                      </div>
                    </div>
                  )}

                  {error && (
                    <div
                      className="flex items-start gap-3.5 p-4.5 rounded-2xl text-xs sm:text-sm animate-fade-in-up"
                      style={{
                        background: "rgba(239, 68, 68, 0.09)",
                        border: "1px solid rgba(239, 68, 68, 0.3)",
                        color: "var(--red-ai)",
                      }}
                    >
                      <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                      <div>
                        <div className="font-bold">Analysis Error</div>
                        <div className="mt-0.5 opacity-90">{error}</div>
                      </div>
                    </div>
                  )}

                  {/* Primary Action Button */}
                  <button
                    id="analyze-btn"
                    onClick={handleAnalyze}
                    disabled={!canAnalyze || isLoading}
                    className="btn-glow w-full py-4.5 text-base sm:text-lg font-black flex items-center justify-center gap-3 rounded-2xl cursor-pointer shadow-xl"
                    style={{
                      opacity: !canAnalyze || isLoading ? 0.45 : 1,
                      cursor: !canAnalyze || isLoading ? "not-allowed" : "pointer",
                    }}
                  >
                    {isLoading ? (
                      <span className="flex items-center gap-2.5">
                        <Loader2 size={22} className="animate-spin-slow" />
                        <span>Analyzing Document…</span>
                      </span>
                    ) : (
                      <span className="flex items-center gap-2.5">
                        <Sparkles size={20} />
                        Run AI Detection Analysis
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Bottom Trust Badges */}
            <div className="flex items-center justify-center gap-8 sm:gap-12 pt-4 text-xs font-extrabold tracking-wide" style={{ color: "var(--text-muted)" }}>
              <span>🔒 100% Confidential Parsing</span>
              <span>⚡ Sub-Second Statistical Analysis</span>
              <span>📄 PDF · DOCX · TXT Files Supported</span>
              <span>🎯 4 Category Specific NLP Engines</span>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer
        className="relative z-10 text-center py-6 text-xs border-t transition-colors duration-300"
        style={{
          color: "var(--text-muted)",
          borderColor: "var(--border-primary)",
        }}
      >
        <span className="gradient-text font-bold">Detectra</span> AI Integrity Suite v1.0 — Powered by FastAPI & Next.js
      </footer>
    </div>
  );
}
