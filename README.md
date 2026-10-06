# 🎓 AcademiCheck AI Integrity Suite

> A full-stack AI detection application that identifies AI-generated content across academic and professional documents. Upload essays, resumes, research papers, and cover letters to receive a comprehensive integrity report with sentence-level highlighting and visual analytics.

![AcademiCheck](https://img.shields.io/badge/AcademiCheck-AI%20Integrity%20Suite-6366f1?style=for-the-badge&logo=graduation-cap&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38bdf8?style=flat-square&logo=tailwindcss)

---

## 🗂️ Project Structure

```
AI-Detector/
├── backend/                    # Python FastAPI backend
│   ├── app.py                  # Main API + AI detection engine
│   ├── requirements.txt        # Python dependencies
│   ├── uploads/                # Temporary upload directory
│   └── nltk_data/              # Auto-downloaded NLTK models
│
├── frontend/                   # Next.js 16 + Tailwind CSS frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # Main application page
│   │   │   ├── layout.tsx      # Root layout + SEO metadata
│   │   │   └── globals.css     # Design system styles
│   │   ├── components/
│   │   │   ├── Header.tsx              # Top navigation (AcademiCheck brand)
│   │   │   ├── FileUploadZone.tsx      # Drag-and-drop file upload
│   │   │   ├── DocumentTypeSelector.tsx # Color-themed dropdown
│   │   │   ├── ScoreDial.tsx           # Animated SVG score dial
│   │   │   └── ResultsDashboard.tsx    # Full results + Recharts visuals
│   │   ├── lib/
│   │   │   └── api.ts          # Axios API client
│   │   └── types/
│   │       └── index.ts        # TypeScript interfaces
│   └── next.config.ts          # API proxy → localhost:8000
│
└── test_files/                 # Sample documents for testing
    ├── sample_ai_essay.txt     # High AI-probability essay (~70–85%)
    ├── sample_human_sop.txt    # Low AI-probability SOP (~15–35%)
    ├── sample_resume.txt       # Mixed-content resume
    └── sample_research_paper.txt  # AI-heavy research paper
```

---

## ⚙️ Prerequisites

- **Python 3.10+** (tested on 3.13)
- **Node.js 18+** with npm
- **pip** package manager

---

## 🚀 Running Locally

### Step 1 — Start the Backend (FastAPI)

```powershell
# Navigate to the backend directory
cd AI-Detector\backend

# Create a virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at: **http://localhost:8000**  
Interactive API docs: **http://localhost:8000/docs**

> **Note:** On first run, NLTK will automatically download required models (`punkt`, `punkt_tab`, `stopwords`). This may take a few seconds.

---

### Step 2 — Start the Frontend (Next.js)

Open a **new terminal window**:

```powershell
# Navigate to the frontend directory
cd AI-Detector\frontend

# Install Node dependencies (first time only)
npm install

# Start the development server
npm run dev
```

The frontend will be available at: **http://localhost:3000**

---

## ✅ Testing the Application

### Quick API Health Check

```powershell
# Health check
curl http://localhost:8000/health

# Test with the AI essay sample
curl -X POST http://localhost:8000/analyze `
  -F "file=@..\test_files\sample_ai_essay.txt" `
  -F "document_type=essay"
```

### Browser Test Workflow

1. Open **http://localhost:3000**
2. Select **"Homework / Assignment Essay"** from the dropdown
3. Upload `test_files/sample_ai_essay.txt` (expect 🔴 **70–85% AI score**)
4. Explore the 4 result tabs: AI Metrics · Visuals · Readability · Sentence View
5. Click **Export Report** to download a plain-text summary

### Test with Human Text

1. Switch to **"Paste Text"** mode
2. Select **"Cover Letter / SOP"**
3. Paste `test_files/sample_human_sop.txt` content
4. Expect 🟢 **Low AI score (~15–35%)**

---

## 🧠 Detection Engine

AcademiCheck uses a **multi-signal heuristic approach** (no external API required):

| Signal | Description | Weight Range |
|--------|-------------|------|
| **Vocabulary Patterns** | Matches 30+ AI-typical phrases ("delve", "leverage", "holistic", etc.) | 25–30% |
| **Sentence Uniformity (Burstiness)** | Measures sentence-length variance — AI writes more uniformly | 25–40% |
| **Lexical Diversity (Perplexity Proxy)** | Unique-word ratio — AI tends to repeat more | 25–50% |

Weights are **tuned per document type**:
- **Essays** → Perplexity-heavy (45%)
- **Resumes** → Burstiness-heavy (40%)
- **Research Papers** → Highest perplexity weight (50%)
- **Cover Letters** → Balanced approach

### Verdict Thresholds

| Score | Verdict | Color |
|-------|---------|-------|
| ≥ 70% | Highly AI-Generated | 🔴 Red |
| 45–69% | Likely AI-Assisted | 🟠 Orange |
| 25–44% | Mixed Content | 🟡 Yellow |
| < 25% | Likely Human-Written | 🟢 Green |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API root info |
| `GET` | `/health` | Health check |
| `GET` | `/document-types` | List all document type profiles |
| `POST` | `/analyze` | Upload file (.pdf/.docx/.txt) for analysis |
| `POST` | `/analyze-text` | Submit raw pasted text for analysis |

### Example Response

```json
{
  "document_type": "essay",
  "document_type_name": "Homework / Assignment Essay",
  "overall_ai_probability": 72.4,
  "verdict": "Highly AI-Generated",
  "verdict_color": "red",
  "metrics": {
    "perplexity_score": 68.2,
    "burstiness_score": 71.5,
    "vocabulary_score": 81.0
  },
  "readability": {
    "flesch_kincaid_grade": 14.2,
    "flesch_reading_ease": 38.5,
    "gunning_fog_index": 17.1
  },
  "document_stats": {
    "word_count": 512,
    "sentence_count": 24,
    "avg_sentence_length": 21.3,
    "ai_sentences": 14,
    "human_sentences": 6,
    "mixed_sentences": 4
  },
  "sentence_analysis": [
    { "id": 0, "text": "...", "ai_probability": 78.5, "label": "ai" },
    ...
  ]
}
```

---

## 🎨 UI Features

- **Dark mode glassmorphism** with animated gradient orbs
- **Animated SVG score dial** with dual-glow gradient ring
- **4-tab results dashboard**: AI Metrics · Visuals · Readability · Sentence View
- **Interactive Recharts**: RadarChart, PieChart, BarChart for visual analysis
- **Export Report** button — downloads plain-text integrity report
- **Color-coded sentence highlighting**: 🔴 AI · 🟠 Mixed · 🟢 Human
- **Drag-and-drop** file upload with per-extension color theming
- **Paste mode** with real-time word count progress (green when ≥ 20 words)
- **Staggered animations** for metric cards on results load
- **Trust indicators** showing supported formats and privacy

---

## 🔧 Troubleshooting

**Backend won't start?**
```powershell
# Check if port 8000 is in use
netstat -an | findstr 8000

# Kill process on port 8000 (PowerShell)
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess
```

**NLTK download errors?**
```python
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

**Frontend can't reach API?**
- Ensure backend is running on port 8000
- Check `frontend/next.config.ts` for the proxy rewrite config
- Verify CORS origins include `http://localhost:3000` in `backend/app.py`

**"Module not found" errors in frontend?**
```powershell
cd AI-Detector\frontend
Remove-Item -Recurse -Force node_modules, .next
npm install
npm run dev
```

---

## 📦 Dependencies

### Backend
| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.115 | Web framework |
| `uvicorn` | 0.32 | ASGI server |
| `nltk` | 3.9 | NLP tokenization |
| `textstat` | 0.7.3 | Readability metrics |
| `PyPDF2` | 3.0.1 | PDF extraction |
| `python-docx` | 1.1.2 | DOCX extraction |
| `numpy` | 2.1 | Numerical analysis |

### Frontend
| Package | Purpose |
|---------|---------|
| `next` | React framework |
| `tailwindcss` | Utility CSS |
| `axios` | HTTP client |
| `lucide-react` | Icon library |
| `recharts` | Interactive charts |
| `framer-motion` | Animation library |

---

*AcademiCheck AI Integrity Suite — Built with FastAPI + Next.js 16 + Tailwind CSS + Recharts*
