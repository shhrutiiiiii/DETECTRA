"use client";

import React, { useEffect, useRef, useState } from "react";

interface ScoreDialProps {
  score: number; // 0–100
  color: string; // CSS color string
  size?: number;
  label?: string;
}

export default function ScoreDial({
  score,
  color,
  size = 180,
  label = "AI Score",
}: ScoreDialProps) {
  const [displayScore, setDisplayScore] = useState(0);
  const animRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    let current = 0;
    const target = score;
    const duration = 900; // ms
    const steps = 60;
    const step = target / steps;
    const interval = duration / steps;

    const tick = () => {
      current = Math.min(current + step, target);
      setDisplayScore(Math.round(current));
      if (current < target) {
        animRef.current = setTimeout(tick, interval);
      }
    };
    tick();
    return () => {
      if (animRef.current) clearTimeout(animRef.current);
    };
  }, [score]);

  const strokeWidth = size * 0.065;
  const radius = (size - strokeWidth * 2 - 4) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (displayScore / 100) * circumference;

  // Create gradient id unique to this instance
  const gradientId = `dial-gradient-${color.replace(/[^a-zA-Z0-9]/g, "")}`;

  return (
    <div
      className="score-dial-container"
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ transform: "rotate(-90deg)" }}
      >
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={color} stopOpacity="0.7" />
            <stop offset="100%" stopColor={color} stopOpacity="1" />
          </linearGradient>
          <filter id="dial-glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={strokeWidth}
        />

        {/* Secondary track glow */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth + 6}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          opacity={0.12}
        />

        {/* Progress arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={`url(#${gradientId})`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          filter="url(#dial-glow)"
          style={{
            transition: "stroke-dashoffset 0.05s ease",
          }}
        />
      </svg>

      {/* Center text */}
      <div
        className="absolute inset-0 flex flex-col items-center justify-center"
        style={{ transform: "none" }}
      >
        <span
          className="font-black tabular-nums leading-none"
          style={{
            fontSize: size * 0.23 + "px",
            color,
            fontFamily: "'Fira Code', monospace",
            textShadow: `0 0 24px ${color}55`,
          }}
        >
          {displayScore}
          <span style={{ fontSize: size * 0.11 + "px", opacity: 0.8 }}>%</span>
        </span>
        <span
          className="font-semibold uppercase tracking-widest mt-1"
          style={{
            color: "rgba(255,255,255,0.3)",
            fontSize: size * 0.065 + "px",
            letterSpacing: "0.12em",
          }}
        >
          {label}
        </span>
      </div>
    </div>
  );
}
