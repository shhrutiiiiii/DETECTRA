"use client";

import React, { useState } from "react";
import { AnalysisResult } from "@/types";
import ScoreDial from "./ScoreDial";
import {
  FileText,
  BarChart2,
  AlignLeft,
  Hash,
  BookOpen,
  TrendingUp,
  Eye,
  Brain,
  Sparkles,
  ArrowLeft,
  Download,
  Activity,
  Layers,
  MessageSquare,
} from "lucide-react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

interface ResultsDashboardProps {
  result: AnalysisResult;
  onReset: () => void;
}

const VERDICT_CONFIG = {
  red: {
    bg: "rgba(239, 68, 68, 0.08)",
    border: "rgba(239, 68, 68, 0.3)",
    text: "#EF4444",
    glow: "rgba(239, 68, 68, 0.15)",
    dialColor: "#EF4444",
    label: "Highly AI-Generated",
    icon: "🤖",
    gradientFrom: "#EF4444",
    gradientTo: "#dc2626",
  },
  orange: {
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.3)",
    text: "#F59E0B",
    glow: "rgba(245, 158, 11, 0.15)",
    dialColor: "#F59E0B",
    label: "Likely AI-Assisted",
    icon: "⚠️",
    gradientFrom: "#F59E0B",
    gradientTo: "#d97706",
  },
  yellow: {
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.3)",
    text: "#F59E0B",
    glow: "rgba(245, 158, 11, 0.15)",
    dialColor: "#F59E0B",
    label: "Mixed Content",
    icon: "🔍",
    gradientFrom: "#F59E0B",
    gradientTo: "#b45309",
  },
  green: {
    bg: "rgba(16, 185, 129, 0.08)",
    border: "rgba(16, 185, 129, 0.3)",
    text: "#10B981",
    glow: "rgba(16, 185, 129, 0.15)",
    dialColor: "#10B981",
    label: "Likely Human-Written",
    icon: "✅",
    gradientFrom: "#10B981",
    gradientTo: "#059669",
  },
};

function MetricBar({
  label,
  value,
  color,
  tooltip,
  delay = 0,
}: {
  label: string;
  value: number;
  color: string;
  tooltip?: string;
  delay?: number;
}) {
  return (
    <div
      className="metric-card p-4 tooltip"
      data-tip={tooltip}
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex justify-between items-center mb-2.5">
        <span className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>
          {label}
        </span>
        <span
          className="text-sm font-bold tabular-nums px-2.5 py-0.5 rounded-full"
          style={{
            color,
            background: `${color}18`,
            fontFamily: "'Fira Code', monospace",
          }}
        >
          {value}%
        </span>
      </div>
      <div className="progress-bar-track" style={{ height: 7, borderRadius: 999 }}>
        <div
          className="progress-bar-fill"
          style={{
            width: `${value}%`,
            background: `linear-gradient(90deg, ${color}77, ${color})`,
            height: "100%",
            borderRadius: 999,
            boxShadow: `0 0 10px ${color}33`,
          }}
        />
      </div>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  sub,
  color,
  delay = 0,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
  delay?: number;
}) {
  return (
    <div
      className="metric-card p-4 flex items-center gap-3.5"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div
        className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm"
        style={{ background: color ? `${color}14` : "var(--subtle-bg)" }}
      >
        <span style={{ color: color ?? "var(--accent-primary)" }}>{icon}</span>
      </div>
      <div>
        <div
          className="font-bold tabular-nums"
          style={{
            color: color ?? "var(--text-primary)",
            fontFamily: "'Fira Code', monospace",
            fontSize: "1.1rem",
            lineHeight: 1.2,
          }}
        >
          {value}
        </div>
        <div className="text-xs mt-0.5" style={{ color: "var(--text-secondary)" }}>
          {label}
          {sub && <span style={{ color: "var(--text-muted)" }}> · {sub}</span>}
        </div>
      </div>
    </div>
  );
}

// Custom recharts tooltip
const CustomTooltip = ({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}) => {
  if (active && payload && payload.length) {
    return (
      <div
        style={{
          background: "#1E293B",
          border: "1px solid #334155",
          borderRadius: 10,
          padding: "8px 14px",
          fontSize: 12,
          color: "#F8FAFC",
        }}
      >
        {label && <div style={{ color: "#94A3B8", marginBottom: 4 }}>{label}</div>}
        {payload.map((p) => (
          <div key={p.name} style={{ color: p.color }}>
            {p.name}: <strong>{p.value}%</strong>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export default function ResultsDashboard({
  result,
  onReset,
}: ResultsDashboardProps) {
  const config = VERDICT_CONFIG[result.verdict_color];
  const [activeTab, setActiveTab] = useState<"breakdown" | "readability" | "sentences" | "charts">(
    "breakdown"
  );

  const getReadabilityLabel = (score: number) => {
    if (score >= 90) return "Very Easy";
    if (score >= 70) return "Easy";
    if (score >= 60) return "Standard";
    if (score >= 50) return "Fairly Difficult";
    if (score >= 30) return "Difficult";
    return "Very Confusing";
  };

  // Data for pie chart (sentence distribution)
  const pieData = [
    { name: "AI", value: result.document_stats.ai_sentences, color: "#EF4444" },
    { name: "Mixed", value: result.document_stats.mixed_sentences, color: "#F59E0B" },
    { name: "Human", value: result.document_stats.human_sentences, color: "#10B981" },
  ].filter((d) => d.value > 0);

  // Data for radar chart
  const radarData = [
    {
      subject: "Vocabulary",
      score: result.metrics.vocabulary_score,
      fullMark: 100,
    },
    {
      subject: "Uniformity",
      score: result.metrics.burstiness_score,
      fullMark: 100,
    },
    {
      subject: "Lexical",
      score: result.metrics.perplexity_score,
      fullMark: 100,
    },
    {
      subject: "Readability",
      score: Math.min(100, Math.max(0, result.readability.flesch_kincaid_grade * 5)),
      fullMark: 100,
    },
    {
      subject: "Avg Length",
      score: Math.min(100, result.document_stats.avg_sentence_length * 3),
      fullMark: 100,
    },
  ];

  // Bar chart data for readability
  const readabilityBarData = [
    {
      name: "FK Grade",
      value: Math.min(100, result.readability.flesch_kincaid_grade * 5),
      raw: result.readability.flesch_kincaid_grade,
    },
    {
      name: "Reading Ease",
      value: result.readability.flesch_reading_ease,
      raw: result.readability.flesch_reading_ease,
    },
    {
      name: "Fog Index",
      value: Math.min(100, result.readability.gunning_fog_index * 5),
      raw: result.readability.gunning_fog_index,
    },
  ];

  const TABS = [
    { id: "breakdown" as const, label: "AI Metrics Breakdown", icon: <Brain size={16} /> },
    { id: "charts" as const, label: "Visual Analytics", icon: <Activity size={16} /> },
    { id: "readability" as const, label: "Readability Suite", icon: <BookOpen size={16} /> },
    { id: "sentences" as const, label: "Sentence Inspector", icon: <Eye size={16} /> },
  ];

  return (
    <div className="animate-fade-in-up w-full max-w-[1650px] mx-auto flex flex-col" style={{ gap: "0.5cm" }}>
      {/* ─── Hero Summary Card (Full Screen Spacious Layout with 0.5cm Line Distance) ─── */}
      <div
        className="glass-card p-8 sm:p-10 md:p-12 shadow-2xl transition-all duration-300"
        style={{
          borderColor: config.border,
          boxShadow: `0 0 60px ${config.glow}`,
        }}
      >
        <div className="flex flex-col lg:flex-row items-center lg:items-start" style={{ gap: "0.5cm" }}>
          {/* Score Dial */}
          <div className="flex-shrink-0 py-2">
            <ScoreDial
              score={result.overall_ai_probability}
              color={config.dialColor}
              size={210}
            />
          </div>

          {/* Summary Info with 0.5cm distance between lines */}
          <div className="flex-1 w-full flex flex-col" style={{ gap: "0.5cm" }}>
            {/* Verdict Header Line - Perfectly Aligned */}
            <div className="flex items-center gap-3.5 flex-wrap">
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl sm:text-3xl flex-shrink-0 leading-none">{config.icon}</span>
                <h2
                  className="text-xl sm:text-2xl lg:text-3xl font-black tracking-tight leading-snug truncate"
                  style={{ color: "var(--text-primary)", fontFamily: "'Fira Code', monospace" }}
                >
                  {result.verdict}
                </h2>
              </div>
              <span
                className="verdict-badge text-xs sm:text-sm px-3.5 py-1.5 font-extrabold uppercase tracking-wider rounded-lg flex-shrink-0"
                style={{
                  background: config.bg,
                  border: `1px solid ${config.border}`,
                  color: config.text,
                }}
              >
                {result.document_type_name}
              </span>
            </div>

            <p className="text-base sm:text-lg leading-relaxed" style={{ color: "var(--text-secondary)" }}>
              Analyzed:{" "}
              <span className="font-extrabold text-[#06B6D4]" style={{ color: "var(--text-primary)" }}>{result.filename}</span> ·{" "}
              <span className="font-semibold">{result.file_size_kb} KB</span> ·{" "}
              <span className="font-bold">{result.document_stats.word_count.toLocaleString()} words</span>
            </p>

            {/* Sentence distribution pills - Properly Aligned */}
            <div className="flex items-center flex-wrap" style={{ gap: "0.5cm" }}>
              {[
                {
                  label: "AI Sentences",
                  count: result.document_stats.ai_sentences,
                  color: "var(--red-ai)",
                  bg: "var(--red-highlight)",
                },
                {
                  label: "Mixed Sentences",
                  count: result.document_stats.mixed_sentences,
                  color: "var(--orange-ai)",
                  bg: "var(--orange-highlight)",
                },
                {
                  label: "Human Sentences",
                  count: result.document_stats.human_sentences,
                  color: "var(--green-human)",
                  bg: "var(--green-highlight)",
                },
              ].map((s) => (
                <div
                  key={s.label}
                  className="px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center justify-center gap-2.5 shadow-sm"
                  style={{
                    background: s.bg,
                    border: `1px solid ${s.color}35`,
                    color: s.color,
                  }}
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                    style={{ background: s.color, display: "inline-block" }}
                  />
                  <span>{s.count} {s.label}</span>
                </div>
              ))}
            </div>

            {/* Mini metric indicators - Centered inside Boxes */}
            <div className="grid grid-cols-1 sm:grid-cols-3" style={{ gap: "0.5cm" }}>
              {[
                { label: "Vocabulary Pattern", value: result.metrics.vocabulary_score, color: "var(--accent-primary)" },
                { label: "Burstiness Uniformity", value: result.metrics.burstiness_score, color: "var(--accent-secondary)" },
                { label: "Perplexity Diversity", value: result.metrics.perplexity_score, color: "var(--accent-cyan)" },
              ].map((m) => (
                <div
                  key={m.label}
                  className="rounded-2xl p-4 sm:p-5 shadow-sm flex flex-col justify-center items-start"
                  style={{ background: "var(--subtle-bg)", border: "1px solid var(--border-primary)" }}
                >
                  <div
                    className="text-2xl sm:text-3xl font-black tabular-nums leading-none"
                    style={{ color: m.color, fontFamily: "'Fira Code', monospace" }}
                  >
                    {m.value}%
                  </div>
                  <div className="text-xs sm:text-sm font-semibold mt-2" style={{ color: "var(--text-muted)" }}>
                    {m.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ─── Navigation Tabs Bar (Interactive & Reliable Click Switcher) ─── */}
      <div
        className="glass-card flex overflow-x-auto p-2 sm:p-2.5 rounded-2xl shadow-lg relative z-30 pointer-events-auto"
        style={{ gap: "0.5cm" }}
      >
        {TABS.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              id={`tab-${tab.id}`}
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setActiveTab(tab.id);
              }}
              className={`tab-pill flex items-center gap-2.5 flex-1 justify-center py-3.5 px-6 text-sm sm:text-base font-extrabold rounded-xl transition-all cursor-pointer relative z-30 select-none ${
                isActive ? "active shadow-md" : ""
              }`}
              style={{ whiteSpace: "nowrap", minWidth: 0 }}
            >
              <span className="pointer-events-none flex items-center gap-2.5">
                {tab.icon}
                <span className="inline">{tab.label}</span>
              </span>
            </button>
          );
        })}
      </div>

      {/* ─── Tab 1: AI Metrics Breakdown ─── */}
      {activeTab === "breakdown" && (
        <div className="animate-fade-in flex flex-col" style={{ gap: "0.5cm" }}>
          <div className="glass-card p-7 sm:p-9 shadow-xl flex flex-col" style={{ gap: "0.5cm" }}>
            <h3
              className="text-lg sm:text-xl font-extrabold flex items-center gap-2.5"
              style={{ color: "var(--text-primary)" }}
            >
              <BarChart2 size={20} style={{ color: "var(--accent-primary)" }} />
              Detection Signal Breakdown
            </h3>
            <div className="flex flex-col" style={{ gap: "0.5cm" }}>
              <MetricBar
                label="Vocabulary Pattern Score"
                value={result.metrics.vocabulary_score}
                color="#06B6D4"
                tooltip="Frequency of AI-typical phrases and formal phrasing patterns"
                delay={0}
              />
              <MetricBar
                label="Sentence Uniformity (Burstiness)"
                value={result.metrics.burstiness_score}
                color="#0E7490"
                tooltip="How uniform the sentence-length distribution is — AI tends to be more uniform"
                delay={80}
              />
              <MetricBar
                label="Lexical Diversity (Perplexity Proxy)"
                value={result.metrics.perplexity_score}
                color="#A5F3FC"
                tooltip="Ratio of unique to total content words — low ratio suggests AI"
                delay={160}
              />
            </div>
          </div>

          {/* Document Stats Grid - Uses Full Width Across 6 Columns */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 stagger-children" style={{ gap: "0.5cm" }}>
            <StatCard
              icon={<Hash size={18} />}
              label="Word Count"
              value={result.document_stats.word_count.toLocaleString()}
              color="#06B6D4"
              delay={0}
            />
            <StatCard
              icon={<AlignLeft size={18} />}
              label="Sentences"
              value={result.document_stats.sentence_count}
              color="#0E7490"
              delay={80}
            />
            <StatCard
              icon={<TrendingUp size={18} />}
              label="Avg Sentence Length"
              value={result.document_stats.avg_sentence_length}
              sub="words"
              color="#A5F3FC"
              delay={160}
            />
            <StatCard
              icon={<FileText size={18} />}
              label="Characters"
              value={result.document_stats.char_count.toLocaleString()}
              color="#06B6D4"
              delay={240}
            />
            <StatCard
              icon={<Sparkles size={18} />}
              label="AI Sentences"
              value={result.document_stats.ai_sentences}
              color="#EF4444"
              delay={320}
            />
            <StatCard
              icon={<Brain size={18} />}
              label="Human Sentences"
              value={result.document_stats.human_sentences}
              color="#10B981"
              delay={400}
            />
          </div>
        </div>
      )}

      {/* ─── Tab 2: Visual Analytics / Charts ─── */}
      {activeTab === "charts" && (
        <div className="animate-fade-in flex flex-col" style={{ gap: "0.5cm" }}>
          <div className="grid grid-cols-1 lg:grid-cols-2" style={{ gap: "0.5cm" }}>
            {/* Radar Chart */}
            <div className="glass-card p-7 sm:p-8 shadow-xl">
              <h3
                className="text-lg font-extrabold flex items-center gap-2.5"
                style={{ color: "var(--text-primary)", marginBottom: "0.5cm" }}
              >
                <Layers size={18} style={{ color: "#06B6D4" }} />
                Signal Radar Profile
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.08)" />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: "var(--text-secondary)", fontSize: 13, fontWeight: 600 }}
                  />
                  <Radar
                    name="AI Signals"
                    dataKey="score"
                    stroke={config.dialColor}
                    fill={config.dialColor}
                    fillOpacity={0.22}
                    strokeWidth={2.5}
                  />
                  <Tooltip content={<CustomTooltip />} />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Pie Chart – Sentence Distribution */}
            <div className="glass-card p-7 sm:p-8 shadow-xl">
              <h3
                className="text-lg font-extrabold flex items-center gap-2.5"
                style={{ color: "var(--text-primary)", marginBottom: "0.5cm" }}
              >
                <MessageSquare size={18} style={{ color: "#F59E0B" }} />
                Sentence Category Breakdown
              </h3>
              {pieData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={65}
                      outerRadius={105}
                      paddingAngle={5}
                      dataKey="value"
                      strokeWidth={0}
                    >
                      {pieData.map((entry, idx) => (
                        <Cell
                          key={`cell-${idx}`}
                          fill={entry.color}
                          fillOpacity={0.9}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const d = payload[0];
                          return (
                            <div
                              style={{
                                background: "#0f172a",
                                border: "1px solid rgba(99,102,241,0.3)",
                                borderRadius: 12,
                                padding: "10px 16px",
                                fontSize: 13,
                                color: "#f1f5f9",
                              }}
                            >
                              <div style={{ color: d.payload.color, fontWeight: 700 }}>
                                {d.payload.name}
                              </div>
                              <div className="mt-1 font-semibold">{d.payload.value} sentences</div>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <Legend
                      formatter={(value) => (
                        <span style={{ color: "var(--text-secondary)", fontSize: 13, fontWeight: 600 }}>{value}</span>
                      )}
                    />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div
                  className="flex items-center justify-center h-64 text-sm"
                  style={{ color: "var(--text-muted)" }}
                >
                  No sentence data available
                </div>
              )}
            </div>
          </div>

          {/* Bar Chart – Readability Overview */}
          <div className="glass-card p-7 sm:p-8 shadow-xl">
            <h3
              className="text-lg font-extrabold flex items-center gap-2.5"
              style={{ color: "var(--text-primary)", marginBottom: "0.5cm" }}
            >
              <BarChart2 size={18} style={{ color: "#0E7490" }} />
              Readability Overview (Normalized %)
            </h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={readabilityBarData} barSize={44}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="rgba(255,255,255,0.05)"
                  vertical={false}
                />
                <XAxis
                  dataKey="name"
                  tick={{ fill: "var(--text-secondary)", fontSize: 13, fontWeight: 600 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "var(--text-muted)", fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                  domain={[0, 100]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar
                  dataKey="value"
                  name="Score"
                  radius={[8, 8, 0, 0]}
                  fill="url(#readabilityGrad)"
                />
                <defs>
                  <linearGradient id="readabilityGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#06B6D4" stopOpacity={0.9} />
                    <stop offset="100%" stopColor="#0E7490" stopOpacity={0.6} />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* ─── Tab 3: Readability Suite ─── */}
      {activeTab === "readability" && (
        <div className="glass-card p-8 sm:p-10 animate-fade-in shadow-xl flex flex-col" style={{ gap: "0.5cm" }}>
          <h3
            className="text-xl font-black flex items-center gap-2.5"
            style={{ color: "var(--text-primary)" }}
          >
            <BookOpen size={20} style={{ color: "var(--accent-primary)" }} />
            Readability Analysis Suite
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3" style={{ gap: "0.5cm" }}>
            {[
              {
                label: "Flesch-Kincaid Grade",
                value: result.readability.flesch_kincaid_grade,
                desc: "U.S. grade level required",
                color: "#06B6D4",
                suffix: "grade",
                tooltip: "Lower = easier to read",
              },
              {
                label: "Flesch Reading Ease",
                value: result.readability.flesch_reading_ease,
                desc: getReadabilityLabel(result.readability.flesch_reading_ease),
                color: "#0E7490",
                suffix: "/100",
                tooltip: "Higher = easier to read (max 100)",
              },
              {
                label: "Gunning Fog Index",
                value: result.readability.gunning_fog_index,
                desc: "Years of education needed",
                color: "#F59E0B",
                suffix: "yrs",
                tooltip: "12 = high school, 17 = college graduate",
              },
            ].map((metric) => (
              <div
                key={metric.label}
                className="metric-card p-7 text-center tooltip flex flex-col justify-between"
                data-tip={metric.tooltip}
                style={{ borderColor: `${metric.color}25`, gap: "0.5cm" }}
              >
                <div
                  className="text-5xl sm:text-6xl font-black tabular-nums"
                  style={{
                    color: metric.color,
                    fontFamily: "'Fira Code', monospace",
                    textShadow: `0 0 28px ${metric.color}40`,
                    lineHeight: 1,
                  }}
                >
                  {metric.value}
                  <span
                    className="text-base font-semibold ml-1.5"
                    style={{ color: "var(--text-muted)" }}
                  >
                    {metric.suffix}
                  </span>
                </div>
                <div
                  className="font-extrabold text-base"
                  style={{ color: "var(--text-primary)" }}
                >
                  {metric.label}
                </div>
                <div
                  className="text-xs font-bold px-3 py-1 rounded-full inline-block uppercase tracking-wider self-center"
                  style={{ color: metric.color, background: `${metric.color}18` }}
                >
                  {metric.desc}
                </div>
              </div>
            ))}
          </div>

          {/* Readability guide */}
          <div
            className="rounded-2xl p-6 text-sm flex flex-col"
            style={{
              background: "var(--subtle-bg)",
              border: "1px solid var(--border-primary)",
              gap: "0.5cm",
            }}
          >
            <div className="font-extrabold text-base flex items-center gap-2" style={{ color: "var(--accent-primary)" }}>
              📖 Reading Ease Scale Reference
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3" style={{ gap: "0.5cm" }}>
              {[
                { range: "90–100", label: "Very Easy", sub: "5th grade" },
                { range: "70–89", label: "Easy", sub: "6th grade" },
                { range: "60–69", label: "Standard", sub: "7–8th grade" },
                { range: "50–59", label: "Fairly Difficult", sub: "10th grade" },
                { range: "30–49", label: "Difficult", sub: "College level" },
                { range: "0–29", label: "Very Confusing", sub: "Professional" },
              ].map((r) => (
                <div
                  key={r.range}
                  className="text-xs sm:text-sm font-medium p-2.5 rounded-xl"
                  style={{ background: "var(--bg-glass)", color: "var(--text-secondary)" }}
                >
                  <span style={{ color: "var(--text-primary)", fontWeight: 800 }}>{r.range}</span>{" "}
                  — {r.label}
                  <span style={{ color: "var(--text-muted)" }}> ({r.sub})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── Tab 4: Sentence Inspector ─── */}
      {activeTab === "sentences" && (
        <div className="glass-card p-8 sm:p-10 animate-fade-in shadow-xl flex flex-col" style={{ gap: "0.5cm" }}>
          <div className="flex items-center justify-between flex-wrap gap-4 border-b pb-5" style={{ borderColor: "var(--border-primary)" }}>
            <h3
              className="text-xl font-extrabold flex items-center gap-2.5"
              style={{ color: "var(--text-primary)" }}
            >
              <Eye size={20} style={{ color: "var(--accent-primary)" }} />
              Sentence-Level Highlight Inspector
            </h3>
            <div className="flex items-center gap-4 text-xs font-bold flex-wrap">
              {[
                { label: "AI Generated", bg: "rgba(239, 68, 68, 0.35)", border: "#EF4444" },
                { label: "Mixed AI/Human", bg: "rgba(245, 158, 11, 0.3)", border: "#F59E0B" },
                { label: "Human Written", bg: "rgba(16, 185, 129, 0.25)", border: "#10B981" },
              ].map((legend) => (
                <span key={legend.label} className="flex items-center gap-2 px-3 py-1 rounded-lg" style={{ background: "var(--subtle-bg)" }}>
                  <span
                    className="inline-block w-3.5 h-3.5 rounded-sm border shadow-xs"
                    style={{
                      background: legend.bg,
                      borderColor: legend.border,
                    }}
                  />
                  <span style={{ color: "var(--text-secondary)" }}>{legend.label}</span>
                </span>
              ))}
            </div>
          </div>

          <div
            className="rounded-2xl p-6 sm:p-8 text-base sm:text-lg transition-all"
            style={{
              background: "var(--input-bg)",
              border: "1px solid var(--border-primary)",
              maxHeight: "650px",
              minHeight: "350px",
              overflowY: "auto",
              lineHeight: "0.5cm",
            }}
          >
            {result.sentence_analysis.map((s) => (
              <span
                key={s.id}
                className={`sentence-${s.label} transition-all`}
                title={`AI Probability: ${s.ai_probability}% · Label: ${s.label}`}
              >
                {s.text}{" "}
              </span>
            ))}
          </div>

          <div
            className="text-xs sm:text-sm font-semibold flex items-center gap-2"
            style={{ color: "var(--text-muted)" }}
          >
            <span>💡</span> Hover over highlighted text to see individual sentence AI probability scores.
          </div>
        </div>
      )}

      {/* ─── Action Buttons with 0.5cm Gap ─── */}
      <div className="flex justify-center flex-wrap" style={{ gap: "0.5cm" }}>
        <button
          onClick={onReset}
          id="analyze-another-btn"
          className="btn-glow px-10 py-4.5 text-base sm:text-lg font-black flex items-center gap-3 rounded-2xl cursor-pointer shadow-xl"
        >
          <span className="flex items-center gap-2.5">
            <ArrowLeft size={18} />
            Analyze Another Document
          </span>
        </button>

        <button
          id="export-report-btn"
          className="px-8 py-4.5 text-base sm:text-lg font-extrabold flex items-center gap-3 rounded-2xl transition-all cursor-pointer shadow-md"
          style={{
            background: "var(--subtle-bg)",
            border: "1px solid var(--border-primary)",
            color: "var(--text-primary)",
          }}
          onClick={() => {
            const reportText = `
Detectra AI Integrity Suite — Analysis Report
================================================
File: ${result.filename} (${result.file_size_kb} KB)
Document Type: ${result.document_type_name}
Analyzed at: ${new Date().toLocaleString()}

VERDICT: ${result.verdict}
Overall AI Probability: ${result.overall_ai_probability}%

DETECTION SIGNALS
─────────────────
Vocabulary Pattern Score: ${result.metrics.vocabulary_score}%
Sentence Uniformity (Burstiness): ${result.metrics.burstiness_score}%
Lexical Diversity (Perplexity): ${result.metrics.perplexity_score}%

READABILITY
───────────
Flesch-Kincaid Grade: ${result.readability.flesch_kincaid_grade}
Flesch Reading Ease: ${result.readability.flesch_reading_ease}/100
Gunning Fog Index: ${result.readability.gunning_fog_index}

DOCUMENT STATS
──────────────
Word Count: ${result.document_stats.word_count}
Sentence Count: ${result.document_stats.sentence_count}
Avg Sentence Length: ${result.document_stats.avg_sentence_length} words
AI Sentences: ${result.document_stats.ai_sentences}
Mixed Sentences: ${result.document_stats.mixed_sentences}
Human Sentences: ${result.document_stats.human_sentences}

Generated by Detectra AI Integrity Suite
            `.trim();
            const blob = new Blob([reportText], { type: "text/plain" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `detectra-report-${Date.now()}.txt`;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          <Download size={18} />
          Export Detailed Report
        </button>
      </div>
    </div>
  );
}
