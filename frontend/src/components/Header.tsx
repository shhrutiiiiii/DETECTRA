"use client";

import React, { useEffect, useState } from "react";
import { Zap, Shield, GraduationCap, Sun, Moon } from "lucide-react";

export default function Header() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");

  useEffect(() => {
    const saved = localStorage.getItem("detectra_theme") as "dark" | "light" | null;
    if (saved) {
      setTheme(saved);
      document.documentElement.setAttribute("data-theme", saved);
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    localStorage.setItem("detectra_theme", nextTheme);
    document.documentElement.setAttribute("data-theme", nextTheme);
  };

  return (
    <header className="relative z-10 w-full px-10 sm:px-16 py-8 border-b border-[#06B6D4]/15 backdrop-blur-md transition-colors duration-300">
      <div className="max-w-[1700px] mx-auto flex items-center justify-between">
        {/* Top-Left Logo with Half-Block Line & Side Spacing */}
        <div className="flex items-center gap-6 py-2 pl-2">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center shadow-xl shadow-[#06B6D4]/25 flex-shrink-0 transition-transform hover:scale-105"
            style={{
              background: "linear-gradient(135deg, #06B6D4, #0E7490)",
            }}
          >
            <GraduationCap size={28} color="white" />
          </div>
          <div className="flex flex-col justify-center py-1 gap-[0.2mm]">
            <div
              className="text-3xl sm:text-4xl font-black tracking-tight leading-none mb-[0.2mm]"
              style={{ fontFamily: "'Fira Code', monospace" }}
            >
              <span className="gradient-text">Detectra</span>
            </div>
            <div
              className="text-xs sm:text-sm font-extrabold tracking-[0.22em] uppercase opacity-95 mt-[0.2mm]"
              style={{ color: "var(--accent-primary)" }}
            >
              DETECTRA INTEGRITY AI SUITE
            </div>
          </div>
        </div>

        {/* Nav Pills & Actions */}
        <div className="flex items-center gap-4 md:gap-6">
          <nav className="hidden md:flex items-center gap-3.5">
            {[
              { icon: <Zap size={16} />, label: "Instant Analysis" },
              { icon: <Shield size={16} />, label: "Privacy First" },
            ].map((item) => (
              <div
                key={item.label}
                className="flex items-center gap-2.5 px-4.5 py-3 rounded-full text-xs font-extrabold tracking-wide transition-all shadow-sm"
                style={{
                  background: "var(--subtle-bg)",
                  border: "1px solid var(--border-primary)",
                  color: "var(--text-secondary)",
                }}
              >
                <span style={{ color: "var(--accent-primary)" }}>{item.icon}</span>
                {item.label}
              </div>
            ))}
          </nav>

          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle Theme"
            className="flex items-center gap-2.5 px-4.5 py-3 rounded-full text-xs font-extrabold transition-all duration-300 hover:scale-105 cursor-pointer shadow-sm"
            style={{
              background: theme === "dark" ? "rgba(255, 255, 255, 0.08)" : "rgba(6, 182, 212, 0.12)",
              border: "1px solid var(--border-primary)",
              color: "var(--text-primary)",
            }}
          >
            {theme === "dark" ? (
              <>
                <Sun size={17} className="text-amber-400" />
                <span className="hidden sm:inline">Light Mode</span>
              </>
            ) : (
              <>
                <Moon size={17} className="text-[#06B6D4]" />
                <span className="hidden sm:inline">Dark Mode</span>
              </>
            )}
          </button>

          {/* Status Badge */}
          <div
            className="px-4.5 py-3 rounded-full text-xs font-extrabold flex items-center gap-2.5 shadow-sm"
            style={{
              background: "rgba(16, 185, 129, 0.12)",
              border: "1px solid rgba(16, 185, 129, 0.3)",
              color: "var(--green-human)",
            }}
          >
            <span className="w-2.5 h-2.5 rounded-full bg-[#10B981] animate-pulse" />
            <span className="hidden xs:inline">System</span> Ready
          </div>
        </div>
      </div>
    </header>
  );
}
