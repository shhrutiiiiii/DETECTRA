"""
Detectra AI Integrity Suite - Backend API
FastAPI backend for multi-document AI detection across
student essays, resumes, research papers, and cover letters.
"""

import os
import io
import re
import time
import logging
from pathlib import Path

import nltk
import numpy as np
import textstat
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# NLTK setup
NLTK_DATA_PATH = os.path.join(os.path.dirname(__file__), "nltk_data")
os.makedirs(NLTK_DATA_PATH, exist_ok=True)
nltk.data.path.insert(0, NLTK_DATA_PATH)

for pkg in ["punkt", "punkt_tab", "averaged_perceptron_tagger", "stopwords"]:
    try:
        if "punkt" in pkg:
            nltk.data.find(f"tokenizers/{pkg}")
        elif "tagger" in pkg:
            nltk.data.find(f"taggers/{pkg}")
        else:
            nltk.data.find(f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, download_dir=NLTK_DATA_PATH, quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Detectra AI Integrity Suite API",
    description="AI Content Detection API for essays, resumes, research papers, and cover letters.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

DOCUMENT_PROFILES = {
    "essay": {
        "name": "Homework / Assignment Essay",
        "perplexity_weight": 0.45,
        "burstiness_weight": 0.30,
        "vocabulary_weight": 0.25,
        "description": "Optimised for academic tone and structure",
    },
    "resume": {
        "name": "Resume / CV",
        "perplexity_weight": 0.30,
        "burstiness_weight": 0.40,
        "vocabulary_weight": 0.30,
        "description": "Optimised for bullet-points, work history, and skills",
    },
    "research": {
        "name": "Research Paper / Thesis",
        "perplexity_weight": 0.50,
        "burstiness_weight": 0.25,
        "vocabulary_weight": 0.25,
        "description": "Optimised for academic rigor and citation structure",
    },
    "cover_letter": {
        "name": "Cover Letter / SOP",
        "perplexity_weight": 0.35,
        "burstiness_weight": 0.35,
        "vocabulary_weight": 0.30,
        "description": "Optimised for personal narrative voice",
    },
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not HAS_PYPDF2:
        raise HTTPException(status_code=500, detail="PyPDF2 not installed")
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    return clean_text(text)


def extract_text_from_docx(file_bytes: bytes) -> str:
    if not HAS_DOCX:
        raise HTTPException(status_code=500, detail="python-docx not installed")
    doc = DocxDocument(io.BytesIO(file_bytes))
    text = " ".join(para.text for para in doc.paragraphs if para.text.strip())
    return clean_text(text)


def extract_text_from_txt(file_bytes: bytes) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return clean_text(file_bytes.decode(enc))
        except UnicodeDecodeError:
            continue
    return clean_text(file_bytes.decode("utf-8", errors="replace"))


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()


STOP_WORDS = set()
try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    pass

AI_PHRASE_PATTERNS = [
    r"\bdelve(s|d|ing)?\b", r"\bfoster(s|ed|ing)?\b", r"\bembark(s|ed|ing)?\b", r"\bleverage(s|d|ing)?\b",
    r"\bunleash(es|ed|ing)?\b", r"\bseamless(ly)?\b", r"\bvibrant\b", r"\brobust(ly)?\b",
    r"\blandscape\b", r"\btailored\b", r"\bintricate(ly)?\b", r"\bcomprehensive(ly)?\b",
    r"\bsignificant(ly)?\b", r"\bfacilitate(s|d|ing)?\b", r"\bsynergy\b", r"\bparadigm(s)?\b",
    r"\bholistic(ally)?\b", r"\boptimiz(e|es|ed|ing)\b", r"\bpivotal\b", r"\bcatalyst\b",
    r"\bstrive(s|d|ing)?\b", r"\bnuanced?\b", r"\bultimately\b", r"\bfurthermore\b",
    r"\bmoreover\b", r"\badditionally\b", r"\bconsequently\b", r"\bin conclusion\b",
    r"\bin summary\b", r"\bit is worth noting\b", r"\bit is important to note\b",
    r"\bnotably\b", r"\bone may argue\b", r"\bit is evident\b", r"\bkey aspects?\b",
    r"\bvarious aspects?\b", r"\btestament\b", r"\bbeacon\b", r"\btapestry\b",
    r"\bplay(s|ed)? a (crucial|pivotal|vital|key) role\b", r"\bserves? as a\b",
    r"\bgroundbreaking\b", r"\bever-evolving\b", r"\bshed(s)? light\b", r"\bdemystify\b",
    r"\bgame-changer\b", r"\bin order to\b", r"\baligned with\b", r"\bunderscores?\b",
    r"\bpromising horizon\b", r"\baforesaid\b", r"\bherein\b", r"\bnonetheless\b",
]

AI_PHRASE_RE = [re.compile(p, re.IGNORECASE) for p in AI_PHRASE_PATTERNS]


def compute_sentence_lengths(sentences):
    return [len(s.split()) for s in sentences if s.strip()]


def compute_burstiness(sentence_lengths):
    if len(sentence_lengths) < 3:
        return 0.5
    arr = np.array(sentence_lengths, dtype=float)
    mean, std = arr.mean(), arr.std()
    if mean == 0:
        return 0.5
    cv = std / mean
    if cv <= 0.40:
        score = 0.85 + (0.40 - cv) * 0.375
    elif cv >= 0.65:
        score = max(0.05, 0.35 - (cv - 0.65) * 0.5)
    else:
        score = 0.35 + (0.65 - cv) * 2.0
    return round(min(1.0, max(0.0, score)), 4)


def compute_perplexity_proxy(sentences, text):
    if not sentences:
        return 0.5
    word_count = max(1, len(text.split()))

    ai_transitions = len(re.findall(
        r"\b(furthermore|moreover|additionally|in conclusion|in summary|consequently|notably|it is worth noting|it is important to note|it is evident|ultimately)\b",
        text, re.I
    ))
    trans_density = ai_transitions / (word_count / 100.0)
    trans_score = min(1.0, trans_density / 1.5)

    human_matches = len(re.findall(
        r"\b(i'm|i've|i'd|i'll|didn't|couldn't|wasn't|it's|don't|won't|can't|we've|okay|honestly|totally|embarrassing|hindsight|pretty|stuff|gonna|wanna)\b",
        text, re.I
    ))
    human_density = human_matches / (word_count / 100.0)
    human_discount = min(0.6, human_density * 0.15)

    lengths = [len(s.split()) for s in sentences]
    avg_len = sum(lengths) / len(lengths) if lengths else 15
    len_score = 0.8 if 16 <= avg_len <= 26 else 0.4

    score = (0.5 * trans_score + 0.5 * len_score) - human_discount
    return round(min(1.0, max(0.05, score)), 4)


def compute_vocabulary_sophistication(text):
    word_count = max(1, len(text.split()))
    hits = sum(1 for pattern in AI_PHRASE_RE if pattern.search(text))
    density = hits / (word_count / 100.0)
    score = min(1.0, density / 2.5)
    return round(score, 4)


def score_sentence(sentence, vocab_score):
    words = sentence.split()
    if len(words) < 4:
        return 0.1

    phrase_hits = sum(1 for p in AI_PHRASE_RE if p.search(sentence))
    has_ai_transition = bool(re.search(
        r"\b(furthermore|moreover|additionally|in conclusion|in summary|consequently|notably|it is worth noting|it is important to note|it is evident|ultimately|delve|leverage|holistic|pivotal|catalyst)\b",
        sentence, re.I
    ))
    has_human_marker = bool(re.search(
        r"\b(i'm|i've|i'd|didn't|couldn't|wasn't|it's|don't|won't|can't|okay|honestly|totally|embarrassing|hindsight)\b",
        sentence, re.I
    ))

    base_score = 0.35
    if phrase_hits > 0:
        base_score += 0.35 * min(2, phrase_hits)
    if has_ai_transition:
        base_score += 0.25
    if has_human_marker:
        base_score -= 0.40

    combined = 0.6 * base_score + 0.4 * vocab_score
    return round(min(1.0, max(0.05, combined)), 4)


def analyze_text(text, doc_type):
    profile = DOCUMENT_PROFILES.get(doc_type, DOCUMENT_PROFILES["essay"])
    sentences = sent_tokenize(text)
    if not sentences:
        raise HTTPException(status_code=422, detail="Could not extract any sentences from the document.")

    word_count = len(text.split())
    char_count = len(text)
    lengths = compute_sentence_lengths(sentences)
    burstiness_score = compute_burstiness(lengths)
    perplexity_score = compute_perplexity_proxy(sentences, text)
    vocabulary_score = compute_vocabulary_sophistication(text)

    overall_ai_prob = (
        profile["perplexity_weight"] * perplexity_score
        + profile["burstiness_weight"] * burstiness_score
        + profile["vocabulary_weight"] * vocabulary_score
    )
    overall_ai_prob = round(min(1.0, max(0.0, overall_ai_prob)), 4)

    try:
        flesch_kincaid = textstat.flesch_kincaid_grade(text)
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        gunning_fog = textstat.gunning_fog(text)
    except Exception:
        flesch_kincaid = 0.0
        flesch_reading_ease = 50.0
        gunning_fog = 0.0

    sentence_analysis = []
    for i, sent in enumerate(sentences):
        sent_score = score_sentence(sent, vocabulary_score)
        sentence_analysis.append({
            "id": i,
            "text": sent,
            "ai_probability": round(sent_score * 100, 1),
            "label": "ai" if sent_score >= 0.55 else "human" if sent_score <= 0.35 else "mixed",
        })

    ai_sentences = sum(1 for s in sentence_analysis if s["label"] == "ai")
    human_sentences = sum(1 for s in sentence_analysis if s["label"] == "human")
    mixed_sentences = sum(1 for s in sentence_analysis if s["label"] == "mixed")
    avg_sentence_length = round(sum(lengths) / len(lengths), 1) if lengths else 0

    prob_pct = round(overall_ai_prob * 100, 1)
    if prob_pct >= 70:
        verdict = "Highly AI-Generated"
        verdict_color = "red"
    elif prob_pct >= 45:
        verdict = "Likely AI-Assisted"
        verdict_color = "orange"
    elif prob_pct >= 25:
        verdict = "Mixed Content"
        verdict_color = "yellow"
    else:
        verdict = "Likely Human-Written"
        verdict_color = "green"

    return {
        "document_type": doc_type,
        "document_type_name": profile["name"],
        "overall_ai_probability": prob_pct,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "metrics": {
            "perplexity_score": round(perplexity_score * 100, 1),
            "burstiness_score": round(burstiness_score * 100, 1),
            "vocabulary_score": round(vocabulary_score * 100, 1),
        },
        "readability": {
            "flesch_kincaid_grade": round(flesch_kincaid, 1),
            "flesch_reading_ease": round(flesch_reading_ease, 1),
            "gunning_fog_index": round(gunning_fog, 1),
        },
        "document_stats": {
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": len(sentences),
            "avg_sentence_length": avg_sentence_length,
            "ai_sentences": ai_sentences,
            "human_sentences": human_sentences,
            "mixed_sentences": mixed_sentences,
        },
        "sentence_analysis": sentence_analysis,
    }


@app.get("/")
async def root():
    return {"message": "Detectra AI Integrity Suite API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}


@app.get("/document-types")
async def get_document_types():
    return {
        "types": [
            {
                "id": k,
                "name": v["name"],
                "description": v["description"],
            }
            for k, v in DOCUMENT_PROFILES.items()
        ]
    }


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    document_type: str = Form(default="essay"),
):
    if document_type not in DOCUMENT_PROFILES:
        raise HTTPException(status_code=400, detail=f"Invalid document type.")

    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ("pdf", "docx", "txt"):
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Please upload .pdf, .docx, or .txt files.",
        )

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")

    try:
        if ext == "pdf":
            text = extract_text_from_pdf(file_bytes)
        elif ext == "docx":
            text = extract_text_from_docx(file_bytes)
        else:
            text = extract_text_from_txt(file_bytes)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    if len(text.split()) < 20:
        raise HTTPException(
            status_code=422,
            detail="Document too short for analysis. Please provide at least 20 words.",
        )

    try:
        result = analyze_text(text, document_type)
        result["filename"] = filename
        result["file_size_kb"] = round(len(file_bytes) / 1024, 1)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze-text")
async def analyze_raw_text(
    text: str = Form(...),
    document_type: str = Form(default="essay"),
):
    if document_type not in DOCUMENT_PROFILES:
        raise HTTPException(status_code=400, detail="Invalid document type.")
    if len(text.split()) < 20:
        raise HTTPException(status_code=422, detail="Text too short. Please provide at least 20 words.")

    try:
        result = analyze_text(clean_text(text), document_type)
        result["filename"] = "pasted-text"
        result["file_size_kb"] = round(len(text.encode()) / 1024, 2)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)

