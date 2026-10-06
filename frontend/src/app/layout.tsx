import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Detectra AI Integrity Suite — AI Content Detection Platform",
  description:
    "Detectra intelligently detects AI-generated content across student essays, resumes, research papers, and cover letters. Upload your document and get a comprehensive integrity report with sentence-level highlighting in seconds.",
  keywords: [
    "AI detection",
    "plagiarism checker",
    "AI content detector",
    "ChatGPT detector",
    "essay checker",
    "resume checker",
    "academic integrity",
    "Detectra",
  ],
  authors: [{ name: "Detectra" }],
  openGraph: {
    title: "Detectra AI Integrity Suite",
    description: "Detect AI-generated content in academic and professional documents.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
