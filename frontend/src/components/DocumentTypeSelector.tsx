"use client";

import React from "react";
import { DocumentType } from "@/types";
import { FileText, User, BookOpen, Mail, CheckCircle2, Circle } from "lucide-react";

const DOC_TYPE_CONFIG: Record<
  string,
  { icon: React.ReactNode; color: string; bg: string; badge: string; focusText: string }
> = {
  essay: {
    icon: <FileText size={22} />,
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.14)",
    badge: "Academic Essay",
    focusText: "Tuned for logical structure, essay vocabulary & argument flow",
  },
  resume: {
    icon: <User size={22} />,
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.14)",
    badge: "Resume / CV",
    focusText: "Tuned for bullet points, action verbs & work experience",
  },
  research: {
    icon: <BookOpen size={22} />,
    color: "#0E7490",
    bg: "rgba(14, 116, 144, 0.14)",
    badge: "Research / Thesis",
    focusText: "Tuned for formal citations, passive voice & academic rigor",
  },
  cover_letter: {
    icon: <Mail size={22} />,
    color: "#A5F3FC",
    bg: "rgba(165, 243, 252, 0.14)",
    badge: "Cover Letter",
    focusText: "Tuned for personal narrative, SOP voice & emotional flow",
  },
};

interface DocumentTypeSelectorProps {
  documentTypes: DocumentType[];
  selected: string;
  onChange: (id: string) => void;
  disabled?: boolean;
}

export default function DocumentTypeSelector({
  documentTypes,
  selected,
  onChange,
  disabled,
}: DocumentTypeSelectorProps) {
  return (
    <div className="flex flex-col gap-5 sm:gap-6 w-full" id="document-type-selector">
      {documentTypes.map((dt) => {
        const config = DOC_TYPE_CONFIG[dt.id] ?? DOC_TYPE_CONFIG.essay;
        const isSelected = dt.id === selected;

        return (
          <button
            key={dt.id}
            type="button"
            onClick={() => !disabled && onChange(dt.id)}
            disabled={disabled}
            className="group relative flex items-center justify-between text-left p-6 sm:p-7 rounded-2xl transition-all duration-250 cursor-pointer min-h-[110px] md:min-h-[120px]"
            style={{
              background: isSelected
                ? "var(--bg-glass)"
                : "var(--subtle-bg)",
              border: isSelected
                ? `2px solid ${config.color}`
                : "1px solid var(--border-primary)",
              boxShadow: isSelected
                ? `0 12px 32px -6px ${config.color}35`
                : "none",
              opacity: disabled ? 0.6 : 1,
            }}
          >
            <div className="flex items-center gap-5 min-w-0 flex-1">
              <span
                className="w-13 h-13 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center flex-shrink-0 transition-transform duration-300 group-hover:scale-105 shadow-sm"
                style={{
                  background: config.bg,
                  color: config.color,
                }}
              >
                {config.icon}
              </span>
              <div className="min-w-0 flex-1 space-y-1.5">
                <div className="font-extrabold text-base sm:text-lg leading-snug flex items-center justify-between gap-3" style={{ color: "var(--text-primary)" }}>
                  <span className="truncate">{dt.name}</span>
                  <span className="text-[11px] font-extrabold px-3 py-1 rounded-md uppercase tracking-wider hidden sm:inline flex-shrink-0" style={{ background: "var(--subtle-bg)", color: "var(--text-muted)", border: "1px solid var(--border-primary)" }}>
                    {config.badge}
                  </span>
                </div>
                <div className="text-xs sm:text-sm leading-relaxed text-balance" style={{ color: "var(--text-secondary)" }}>
                  {dt.description || config.focusText}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2 flex-shrink-0 ml-5">
              {isSelected ? (
                <span className="w-8 h-8 rounded-full flex items-center justify-center shadow-sm" style={{ background: `${config.color}22`, color: config.color }}>
                  <CheckCircle2 size={20} />
                </span>
              ) : (
                <span className="w-8 h-8 rounded-full flex items-center justify-center" style={{ color: "var(--text-muted)" }}>
                  <Circle size={20} />
                </span>
              )}
            </div>
          </button>
        );
      })}
    </div>
  );
}
