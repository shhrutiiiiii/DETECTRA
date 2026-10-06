export interface DocumentType {
  id: string;
  name: string;
  description: string;
}

export interface SentenceAnalysis {
  id: number;
  text: string;
  ai_probability: number;
  label: "ai" | "human" | "mixed";
}

export interface AnalysisMetrics {
  perplexity_score: number;
  burstiness_score: number;
  vocabulary_score: number;
}

export interface ReadabilityMetrics {
  flesch_kincaid_grade: number;
  flesch_reading_ease: number;
  gunning_fog_index: number;
}

export interface DocumentStats {
  word_count: number;
  char_count: number;
  sentence_count: number;
  avg_sentence_length: number;
  ai_sentences: number;
  human_sentences: number;
  mixed_sentences: number;
}

export interface AnalysisResult {
  document_type: string;
  document_type_name: string;
  overall_ai_probability: number;
  verdict: string;
  verdict_color: "red" | "orange" | "yellow" | "green";
  metrics: AnalysisMetrics;
  readability: ReadabilityMetrics;
  document_stats: DocumentStats;
  sentence_analysis: SentenceAnalysis[];
  filename: string;
  file_size_kb: number;
}

export type UploadMode = "file" | "text";
export type AnalysisStatus = "idle" | "uploading" | "analyzing" | "done" | "error";
