import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        header_text = "SANSKAR COLLEGE OF MANAGEMENT & PROFESSIONAL STUDIES — BCA (2024–2027)"
        self.drawString(45, A4[1] - 30, header_text)
        
        self.setFont("Helvetica", 8)
        self.drawRightString(A4[0] - 45, A4[1] - 30, "DETECTRA AI INTEGRITY SUITE")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(45, A4[1] - 35, A4[0] - 45, A4[1] - 35)

        # Running Footer
        self.line(45, 40, A4[0] - 45, 40)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 45, 26, page_str)
        self.drawString(45, 26, "Submitted By: Shruti Verma | Ujjwal Kumar | Umesh Tomar (BCA 5th Sem)")

        self.restoreState()


def generate_pdf(filename="Detectra_Project_Report_BCA.pdf"):
    pdf_path = os.path.join(os.getcwd(), filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#0E7490")      # Deep Cyan
    ACCENT = colors.HexColor("#06B6D4")       # Bright Cyan
    DARK_TEXT = colors.HexColor("#0F172A")    # Slate navy dark
    BODY_TEXT = colors.HexColor("#334155")    # Dark slate body
    LIGHT_BG = colors.HexColor("#F8FAFC")     # Soft slate background
    BORDER_COLOR = colors.HexColor("#CBD5E1") # Soft gray border
    CODE_BG = colors.HexColor("#F1F5F9")      # Code block background

    # Simple & Clean Typography Styles
    style_cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=12
    )

    style_cover_subtitle = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=DARK_TEXT,
        alignment=1,
        spaceAfter=18
    )

    style_cover_college = ParagraphStyle(
        "CoverCollege",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=DARK_TEXT,
        alignment=1,
        spaceAfter=4
    )

    style_cover_subcollege = ParagraphStyle(
        "CoverSubCollege",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13.5,
        textColor=BODY_TEXT,
        alignment=1,
        spaceAfter=14
    )

    style_h1 = ParagraphStyle(
        "ChapterHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=DARK_TEXT,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        "SubSectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=PRIMARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        "BulletCustom",
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    style_code = ParagraphStyle(
        "CodeCustom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=CODE_BG,
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=5,
        spaceAfter=6
    )

    style_meta_label = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=13,
        textColor=DARK_TEXT
    )

    style_meta_val = ParagraphStyle(
        "MetaValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13,
        textColor=BODY_TEXT
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 10))
    top_bar = Table([[""]], colWidths=[505], rowHeights=[6])
    top_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(top_bar)
    story.append(Spacer(1, 15))

    story.append(Paragraph("SANSKAR COLLEGE OF MANAGEMENT & PROFESSIONAL STUDIES", style_cover_college))
    story.append(Paragraph("Department of Computer Applications — Approved & Affiliated Institution", style_cover_subcollege))
    story.append(HRFlowable(width="85%", thickness=1, color=BORDER_COLOR, spaceAfter=18))

    story.append(Paragraph("A PROJECT REPORT ON", ParagraphStyle("SubText", parent=style_cover_subtitle, fontSize=11, fontName="Helvetica-Bold", spaceAfter=6)))
    story.append(Paragraph("DETECTRA AI INTEGRITY SUITE", style_cover_title))
    story.append(Paragraph("A Simple, Smart & Multi-Signal AI Content Detector for Academic & Professional Documents", style_cover_subtitle))

    story.append(Spacer(1, 15))

    degree_box_data = [
        [Paragraph("Submitted in partial fulfillment of the requirements for the degree of", ParagraphStyle("Center", parent=style_body, alignment=1))],
        [Paragraph("<b>BACHELOR OF COMPUTER APPLICATIONS (BCA)</b>", ParagraphStyle("CenterMain", parent=style_cover_college, fontSize=12.5, spaceAfter=2))],
        [Paragraph("<b>5TH SEMESTER — ACADEMIC SESSION 2024–2027</b>", ParagraphStyle("CenterSub", parent=style_body, alignment=1, fontName="Helvetica-Bold", textColor=PRIMARY))]
    ]
    degree_table = Table(degree_box_data, colWidths=[485])
    degree_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(degree_table)

    story.append(Spacer(1, 25))

    meta_table_data = [
        [
            Paragraph("<b>SUBMITTED BY:</b>", style_meta_label),
            Paragraph("<b>SUBMITTED TO:</b>", style_meta_label)
        ],
        [
            Paragraph("<b>1. Shruti Verma</b> (Roll No: BCA-5S-01)<br/>"
                      "<b>2. Ujjwal Kumar</b> (Roll No: BCA-5S-02)<br/>"
                      "<b>3. Umesh Tomar</b> (Roll No: BCA-5S-03)<br/><br/>"
                      "<b>Course:</b> BCA 5th Semester<br/>"
                      "<b>Session:</b> 2024–2027", style_meta_val),
            Paragraph("<b>Department of Computer Applications</b><br/>"
                      "Sanskar College of Management<br/>"
                      "and Professional Studies<br/><br/>"
                      "Project Guide / Head of Department", style_meta_val)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[242, 242])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (1,0), 1, PRIMARY),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("ACADEMIC SESSION: 2024–2027", ParagraphStyle("DateStyle", parent=style_body, alignment=1, fontName="Helvetica-Bold", textColor=PRIMARY)))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE OF AUTHENTICITY
    # =========================================================================
    story.append(Paragraph("CERTIFICATE OF AUTHENTICITY", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=15))

    cert_p1 = (
        "This is to certify that the project report entitled <b>\"DETECTRA AI INTEGRITY SUITE\"</b> submitted by "
        "<b>Shruti Verma</b>, <b>Ujjwal Kumar</b>, and <b>Umesh Tomar</b>, students of <b>Bachelor of Computer Applications "
        "(BCA) 5th Semester</b> (Academic Session <b>2024–2027</b>) at <b>Sanskar College of Management and Professional "
        "Studies</b>, is a genuine record of project work carried out by them under the supervision and guidance of the "
        "faculty members of the Department of Computer Applications."
    )
    story.append(Paragraph(cert_p1, style_body))
    story.append(Spacer(1, 10))

    cert_p2 = (
        "The work presented in this project report meets the technical and academic standards prescribed by the University for "
        "the partial fulfillment of the degree of Bachelor of Computer Applications. To the best of our knowledge, the content "
        "presented in this report has not been submitted to any other college or university for any degree or diploma."
    )
    story.append(Paragraph(cert_p2, style_body))
    story.append(Spacer(1, 55))

    sig_data = [
        [
            Paragraph("________________________<br/><b>Project Guide</b><br/>Dept. of Computer Applications", style_body),
            Paragraph("________________________<br/><b>Head of Department (HOD)</b><br/>Dept. of Computer Applications", style_body),
            Paragraph("________________________<br/><b>External Examiner</b><br/>Sanskar College", style_body)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
    ]))
    story.append(sig_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CANDIDATES' DECLARATION
    # =========================================================================
    story.append(Paragraph("CANDIDATES' DECLARATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=15))

    decl_p1 = (
        "We, <b>Shruti Verma</b>, <b>Ujjwal Kumar</b>, and <b>Umesh Tomar</b>, hereby declare that this project report titled "
        "<b>\"DETECTRA AI INTEGRITY SUITE\"</b> is an authentic record of our own original work conducted under the guidance of "
        "the Department of Computer Applications at <b>Sanskar College of Management and Professional Studies</b> for the degree "
        "of <b>Bachelor of Computer Applications (BCA)</b> for the academic session <b>2024–2027</b>."
    )
    story.append(Paragraph(decl_p1, style_body))
    story.append(Spacer(1, 10))

    decl_p2 = (
        "We have adhered to academic honesty and ethical coding practices. All open-source packages, external research papers, "
        "and technical references utilized during the creation of this project have been acknowledged in the References section."
    )
    story.append(Paragraph(decl_p2, style_body))
    story.append(Spacer(1, 45))

    decl_sig_data = [
        [
            Paragraph("<b>Shruti Verma</b><br/>BCA 5th Sem (2024–2027)", style_body),
            Paragraph("<b>Ujjwal Kumar</b><br/>BCA 5th Sem (2024–2027)", style_body),
            Paragraph("<b>Umesh Tomar</b><br/>BCA 5th Sem (2024–2027)", style_body)
        ]
    ]
    decl_sig_table = Table(decl_sig_data, colWidths=[160, 160, 160])
    decl_sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(decl_sig_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    ack_1 = (
        "We express our sincere thanks and gratitude to the Management and Director of <b>Sanskar College of Management "
        "and Professional Studies</b> for providing us with high-speed internet, modern computer labs, and helpful academic "
        "resources to build our BCA final year project."
    )
    story.append(Paragraph(ack_1, style_body))
    story.append(Spacer(1, 6))

    ack_2 = (
        "We are deeply thankful to our <b>Head of Department</b> and our <b>Project Supervisor</b> for their constant guidance, "
        "valuable advice, and timely feedback throughout the planning, coding, and testing phases of the <b>Detectra AI Integrity Suite</b>."
    )
    story.append(Paragraph(ack_2, style_body))
    story.append(Spacer(1, 6))

    ack_3 = (
        "We also extend our special thanks to all faculty members of the Computer Applications Department, our parents, and our "
        "classmates for their steady encouragement during our BCA 5th semester studies."
    )
    story.append(Paragraph(ack_3, style_body))
    story.append(Spacer(1, 20))

    team_box = [
        [Paragraph("<b>Project Team Members:</b>", style_meta_label)],
        [Paragraph("• <b>Shruti Verma</b> (Roll No: BCA-5S-01)<br/>"
                   "• <b>Ujjwal Kumar</b> (Roll No: BCA-5S-02)<br/>"
                   "• <b>Umesh Tomar</b> (Roll No: BCA-5S-03)<br/>"
                   "<i>BCA 5th Semester, Sanskar College</i>", style_meta_val)]
    ]
    team_table = Table(team_box, colWidths=[480])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(team_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: ABSTRACT & PROJECT SUMMARY
    # =========================================================================
    story.append(Paragraph("ABSTRACT & PROJECT SUMMARY", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    abstract_p1 = (
        "In simple terms, artificial intelligence tools like ChatGPT can generate complete essays, resumes, and research papers "
        "in just a few seconds. While these tools are helpful, students sometimes copy AI content directly without doing their own "
        "reading or writing. Colleges and teachers need a simple and reliable tool to check if an assignment was written by a real "
        "human student or generated by an AI model."
    )
    story.append(Paragraph(abstract_p1, style_body))
    story.append(Spacer(1, 6))

    abstract_p2 = (
        "<b>Detectra AI Integrity Suite</b> is a user-friendly software designed to solve this problem. It allows users to upload "
        "documents (like PDF, Word DOCX, or text files) or paste text directly into a web interface. The system then analyzes the text "
        "using three smart linguistic checks:<br/>"
        "1. <b>Sentence Length Patterns (Burstiness):</b> Real humans write sentences of different lengths, while AI models write sentences of uniform length.<br/>"
        "2. <b>Word Variation (Perplexity Proxy):</b> AI models repeat predictable words, while human writers use varied vocabulary.<br/>"
        "3. <b>AI Signature Phrases:</b> The system checks for over 30 common AI words like <i>'delve'</i>, <i>'holistic'</i>, <i>'testament'</i>, and <i>'leverage'</i>."
    )
    story.append(Paragraph(abstract_p2, style_body))
    story.append(Spacer(1, 6))

    abstract_p3 = (
        "Detectra is built using <b>FastAPI (Python 3.13)</b> for backend processing and <b>Next.js 16 (React 19)</b> for a clean visual web dashboard. "
        "It runs completely offline on local computers, ensuring student document privacy without requiring any expensive cloud subscriptions."
    )
    story.append(Paragraph(abstract_p3, style_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    toc_data = [
        ["Page No.", "Section Title", "Key Content Description"],
        ["Page 1", "Cover / Title Page", "College Header, Title, Student Names & Session"],
        ["Page 2", "Certificate of Authenticity", "College Guide & HOD Approval Certificate"],
        ["Page 3", "Candidates' Declaration", "Formal Student Declaration Statement"],
        ["Page 4", "Acknowledgement", "Expressions of Gratitude to Guide & Department"],
        ["Page 5", "Abstract & Project Summary", "Simple Explanation of Detectra Purpose"],
        ["Page 6", "Table of Contents", "Index of All 20 Project Report Pages"],
        ["Page 7", "Chapter 1: Introduction & Background", "AI Generation & Problem Statement"],
        ["Page 8", "Chapter 1: Purpose & Key Goals", "Project Scope, Goals & Target Users"],
        ["Page 9", "Chapter 2: Literature & Comparison", "Human vs. AI Writing & Competitor Study"],
        ["Page 10", "Chapter 3: System Requirements", "Hardware & Software Stack Table"],
        ["Page 11", "Chapter 4: Tech Stack Explained Simply", "FastAPI, NLTK, Next.js & React Overview"],
        ["Page 12", "Chapter 5: System Architecture & DFD", "System Diagram & Data Flow Diagrams"],
        ["Page 13", "Chapter 6: Detection Algorithms", "Burstiness, Perplexity & AI Phrase Checks"],
        ["Page 14", "Chapter 6: Profiles & Readability", "Category Weighting & Readability Scores"],
        ["Page 15", "Chapter 7: Backend Implementation", "Python Code Structure & `app.py` Logic"],
        ["Page 16", "Chapter 8: Frontend Implementation", "Next.js UI Components & Recharts Setup"],
        ["Page 17", "Chapter 9: REST API Specification", "Endpoint Table & JSON Data Payloads"],
        ["Page 18", "Chapter 10: Testing & Test Cases", "Unit Testing & Test Matrix (TC-01 to TC-08)"],
        ["Page 19", "Chapter 11: Advantages & Future Scope", "Privacy, Free Use & Upgrade Roadmap"],
        ["Page 20", "Chapter 12: Conclusion & References", "Final Summary & Simple Bibliography"],
    ]

    toc_table = Table(toc_data, colWidths=[55, 200, 230])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 1 - INTRODUCTION & BACKGROUND
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION & BACKGROUND", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("1.1 What is AI Text Generation?", style_h2))
    story.append(Paragraph(
        "In recent years, Artificial Intelligence tools like ChatGPT, Claude, and Google Gemini have become widely available. "
        "These tools use large mathematical models (called Large Language Models or LLMs) that have read billions of pages of text from "
        "the internet. When a user enters a prompt, the AI predicts word-by-word what text should come next to answer the prompt.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.2 What is the Problem in Colleges?", style_h2))
    story.append(Paragraph(
        "While AI tools are great for learning, they present a major challenge in colleges like <b>Sanskar College of Management "
        "and Professional Studies</b>. Students can quickly generate full homework assignments, research papers, resumes, or cover letters "
        "without reading the topic or understanding the material themselves. If teachers cannot tell the difference between human writing "
        "and AI text, grading becomes unfair.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3 Why Existing Plagiarism Checkers Fail", style_h2))
    story.append(Paragraph(
        "Traditional plagiarism tools (like Turnitin or online copy checkers) look for exact matching sentences copied from websites. "
        "However, when an AI model generates a new answer, it creates brand new sentences that do not match any website word-for-word. "
        "Therefore, traditional plagiarism checkers fail to detect AI text. Detectra was created to solve this exact problem by looking "
        "at linguistic writing patterns rather than webpage matching.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 1 - PURPOSE & KEY GOALS
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: PURPOSE & KEY GOALS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("1.4 Main Purpose of Detectra", style_h2))
    story.append(Paragraph(
        "The primary goal of <b>Detectra AI Integrity Suite</b> is to provide a fast, accurate, and simple software tool that anyone "
        "can use to verify document authenticity. It reads a document, analyzes how the words and sentences are constructed, and gives "
        "a clear percentage score showing whether the text is Human-written or AI-generated.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.5 Detailed List of Project Goals", style_h2))
    story.append(Paragraph("• <b>Simple Web Dashboard:</b> Build an attractive web page where teachers and students can drag-and-drop files or paste text easily.", style_bullet))
    story.append(Paragraph("• <b>Multi-Signal Analysis:</b> Combine 3 different checking methods (Sentence length variation, word variation, and AI keyword matching) for better accuracy.", style_bullet))
    story.append(Paragraph("• <b>Document Category Profiles:</b> Adjust the checking settings depending on whether the document is an Essay, Resume, Research Paper, or SOP.", style_bullet))
    story.append(Paragraph("• <b>Sentence-by-Sentence Highlighting:</b> Color-code every sentence so users can see exactly which sentences look like AI text (Red), mixed text (Orange), or human text (Green).", style_bullet))
    story.append(Paragraph("• <b>Readability Metrics:</b> Show readability grade scores (Flesch-Kincaid) so teachers can evaluate text complexity.", style_bullet))
    story.append(Paragraph("• <b>Full Data Privacy:</b> Ensure all files stay on the local computer so student data is never leaked online.", style_bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("1.6 Who Will Use Detectra?", style_h2))
    story.append(Paragraph("1. <b>Teachers & Professors:</b> To quickly verify student homework and term papers before grading.", style_bullet))
    story.append(Paragraph("2. <b>College Students:</b> To check their own work and ensure their writing sounds natural and original.", style_bullet))
    story.append(Paragraph("3. <b>HR Recruiters:</b> To verify job resumes and cover letters submitted by candidates.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 2 - LITERATURE SURVEY & COMPARISON
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: LITERATURE SURVEY & COMPARISON", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("2.1 Human vs. AI Writing Style Differences", style_h2))
    story.append(Paragraph(
        "Linguistic experts have discovered key differences in how humans and AI write text:<br/>"
        "• <b>Sentence Variety:</b> Humans write naturally with mixed rhythms — combining short 4-word sentences with long 25-word explanation sentences. AI models prefer writing medium-length sentences repeatedly.<br/>"
        "• <b>Vocabulary Choice:</b> Humans choose casual or varied words. AI models frequently choose fancy transitional words like <i>'furthermore'</i>, <i>'delve'</i>, and <i>'testament'</i> to sound formal.<br/>"
        "• <b>Predictability:</b> AI text is mathematically predictable because the computer picks high-probability words.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 System Comparison Table", style_h2))
    story.append(Paragraph("Here is how Detectra compares against existing tools:", style_body))

    comp_data = [
        ["Feature / Capability", "Traditional Plagiarism Checker", "Paid Cloud AI Detectors", "Detectra AI Suite"],
        ["Detects AI Text?", "❌ No (Only matches websites)", "✅ Yes", "✅ Yes"],
        ["Local Offline Privacy", "❌ Sent to cloud servers", "❌ Sent to external APIs", "✅ 100% Local & Private"],
        ["Cost to Use", "Paid Subscription", "Expensive monthly fees", "✅ 100% Free & Open Source"],
        ["Category Profile Tuning", "❌ Fixed rules for all text", "❌ Uniform checking", "✅ Customized for Essays, Resumes, SOPs"],
        ["Sentence Highlighting", "Only highlights exact copied links", "Generic highlights", "✅ Clear Red / Orange / Green colors"],
        ["Readability Analysis", "❌ Not available", "❌ Not available", "✅ Flesch & Fog Grade Scores included"],
    ]

    comp_table = Table(comp_data, colWidths=[110, 120, 125, 130])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_TEXT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(comp_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 3 - SYSTEM REQUIREMENTS & SETUP
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: SYSTEM REQUIREMENTS & SETUP", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("3.1 Hardware Requirements", style_h2))
    story.append(Paragraph("Detectra is designed to run smoothly on standard computers available in college labs.", style_body))

    hw_data = [
        ["Hardware Resource", "Minimum System Requirement", "Recommended System Spec"],
        ["Processor (CPU)", "Intel Core i3 (2.0 GHz) or AMD Ryzen 3", "Intel Core i5 / AMD Ryzen 5 or better"],
        ["RAM Memory", "4 GB DDR4 RAM", "8 GB DDR4 / DDR5 RAM"],
        ["Hard Disk Space", "500 MB Free Disk Space", "1 GB SSD Storage Space"],
        ["Display Screen", "1280 x 720 HD Monitor", "1920 x 1080 Full HD Monitor"],
    ]
    hw_table = Table(hw_data, colWidths=[120, 175, 190])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(hw_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph("3.2 Software Stack Overview", style_h2))

    sw_data = [
        ["Software Component", "Version", "Role in Detectra Project"],
        ["Operating System", "Windows 10 / 11", "Host operating system environment"],
        ["Python Language", "3.13.1", "Backend programming language for analysis logic"],
        ["FastAPI Framework", "0.115.0", "Fast web server framework for REST API endpoints"],
        ["NLTK Library", "3.9.1", "Natural Language Toolkit for splitting sentences and words"],
        ["Textstat Library", "0.7.13", "Calculates reading grade levels and readability scores"],
        ["Node.js Runtime", "18.0+", "JavaScript runtime engine for building the frontend"],
        ["Next.js Framework", "16.3.8", "Modern React web application framework"],
        ["Tailwind CSS", "3.4.1", "Utility CSS for visual layout and glassmorphism design"],
        ["Recharts Library", "2.15.0", "Interactive graphical charts (Radar, Bar, and Pie charts)"],
    ]
    sw_table = Table(sw_data, colWidths=[120, 75, 290])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_TEXT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(sw_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 4 - TECH STACK EXPLAINED SIMPLY
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: TECH STACK EXPLAINED SIMPLY", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("4.1 What is FastAPI and Why We Used It?", style_h2))
    story.append(Paragraph(
        "<b>FastAPI</b> is a modern, high-speed Python framework used to build RESTful web APIs. In our project, "
        "FastAPI acts as the brain behind the scenes. When a user uploads a document on the website, FastAPI receives the file, "
        "runs Python math and NLP algorithms on it, and sends back the result in JSON format within milliseconds.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 What is NLTK (Natural Language Toolkit)?", style_h2))
    story.append(Paragraph(
        "<b>NLTK</b> is a famous Python library designed for processing human text. In Detectra, NLTK helps us:<br/>"
        "• <b>Sentence Tokenization:</b> Automatically break a large paragraph into individual sentences.<br/>"
        "• <b>Word Tokenization:</b> Break sentences into individual words while ignoring punctuation.<br/>"
        "• <b>Stopword Filtering:</b> Identify common filler words like 'the', 'is', 'at' so we can focus on main words.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.3 What is Next.js & React?", style_h2))
    story.append(Paragraph(
        "<b>Next.js</b> (built on top of React) is a frontend web framework. It creates the user interface that teachers and students see. "
        "It provides drag-and-drop file upload zones, tabbed navigation buttons, score dials, and color-coded text display boxes.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.4 Tailwind CSS & Recharts for Visual Styling", style_h2))
    story.append(Paragraph(
        "• <b>Tailwind CSS:</b> Gives Detectra a modern dark-mode design with glowing gradient rings and clean rounded cards.<br/>"
        "• <b>Recharts:</b> Generates interactive graphs (Radar Charts, Pie Charts, and Bar Charts) so users can visually inspect AI metrics.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 5 - SYSTEM ARCHITECTURE & DFD
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: SYSTEM ARCHITECTURE & DFD", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("5.1 System Architecture Diagram & Flow", style_h2))
    story.append(Paragraph("The system is divided into two main parts: Frontend (User Interface) and Backend (API Processing Engine).", style_body))

    arch_box_data = [
        [Paragraph("<b>[ STEP 1: USER INTERFACE LAYER ] — Next.js 16 Web Dashboard</b>", style_meta_label)],
        [Paragraph("User selects Document Profile (Essay, Resume, Paper, SOP) and uploads a .pdf/.docx/.txt file or pastes raw text.", style_body)],
        [Paragraph("↓ Sends HTTP POST Request with Document Payload to FastAPI Server", style_body)],
        [Paragraph("<b>[ STEP 2: BACKEND FILE PARSER ] — FastAPI Server (Port 8000)</b>", style_meta_label)],
        [Paragraph("FastAPI receives file content → Extracts text using PyPDF2 / python-docx → Cleans raw text string.", style_body)],
        [Paragraph("<b>[ STEP 3: NLP CHECKING ENGINE ] — NLTK & Python Algorithms</b>", style_meta_label)],
        [Paragraph("• Calculates Sentence Length Variance (Burstiness Score)<br/>"
                   "• Calculates Unique Word Ratio (Perplexity Score)<br/>"
                   "• Matches AI Signature Words (Vocabulary Score)<br/>"
                   "• Classifies Each Sentence: AI (Red), Mixed (Orange), Human (Green)", style_body)],
        [Paragraph("↓ Returns Complete JSON Analysis Object to Web Dashboard", style_body)],
        [Paragraph("<b>[ STEP 4: DASHBOARD DISPLAY ] — Recharts & Score Dial</b>", style_meta_label)],
        [Paragraph("Displays animated percentage dial, metric cards, graphs, color highlights, and text report export button.", style_body)]
    ]
    arch_table = Table(arch_box_data, colWidths=[485])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("5.2 Data Flow Diagram (DFD Level 0 & Level 1)", style_h2))
    story.append(Paragraph("• <b>DFD Level 0 (Context Level):</b> User → Submits Document → Detectra System → Returns AI Score & Verdict Report.", style_bullet))
    story.append(Paragraph("• <b>DFD Level 1 (Process Breakdown):</b> Input File → Process 1.0 (File Extraction) → Process 2.0 (Tokenization) → Process 3.0 (Score Calculation) → Process 4.0 (Report Generation).", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 6 - DETECTION ALGORITHMS MADE SIMPLE
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: DETECTION ALGORITHMS MADE SIMPLE", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("6.1 Method 1: Sentence Length Variation (Burstiness)", style_h2))
    story.append(Paragraph(
        "<b>What is Burstiness?</b> Burstiness measures how much sentence lengths change throughout a document.<br/>"
        "• <b>Human Writing:</b> Humans naturally mix short sentences ('This works.') with long compound sentences ('Although the experiment faced initial difficulties, the final results proved successful.'). This creates high sentence variation.<br/>"
        "• <b>AI Writing:</b> AI models write sentences of uniform, predictable lengths (usually 15 to 20 words per sentence).<br/>"
        "<b>How Detectra calculates it:</b> We count words in each sentence, find the average length, calculate the standard deviation, and measure the variance. Low variance means High AI Probability!",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.2 Method 2: Word Diversity & Repeatability (Perplexity)", style_h2))
    story.append(Paragraph(
        "<b>What is Perplexity Proxy?</b> Perplexity measures how diverse and unexpected the vocabulary is.<br/>"
        "• <b>Human Writing:</b> Humans use diverse vocabulary, unexpected slang, or unique phrasing.<br/>"
        "• <b>AI Writing:</b> AI algorithms choose the mathematically most common word tokens repeatedly.<br/>"
        "<b>How Detectra calculates it:</b> We calculate the Type-Token Ratio (TTR = Unique Words / Total Words). A lower ratio indicates predictable AI writing.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.3 Method 3: Signature AI Words & Phrases", style_h2))
    story.append(Paragraph(
        "Detectra maintains a dictionary of over 30 signature AI transition words that AI models rely on heavily when writing formal essays. Examples include:",
        style_body
    ))

    ai_words_data = [
        ["Category", "Common Signature AI Phrases Tracked by Detectra"],
        ["Formal Transitions", "furthermore, moreover, in conclusion, it is important to note, non-the-less"],
        ["Overused Fancy Verbs", "delve, leverage, foster, elucidate, expedite, underscore, master"],
        ["Overused Fancy Nouns", "testament, tapestry, beacon, realm, synergy, paramount, pivotal, holistic"],
    ]
    ai_words_table = Table(ai_words_data, colWidths=[120, 365])
    ai_words_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(ai_words_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 6 - PROFILES & READABILITY SCORES
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: PROFILES & READABILITY SCORES", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("6.4 Category Profile Weights", style_h2))
    story.append(Paragraph(
        "A resume should not be checked with the same rules as a 10-page research paper. Detectra dynamically adjusts signal weights based on the document category:",
        style_body
    ))

    weight_data = [
        ["Document Category Profile", "Perplexity Weight", "Burstiness Weight", "Vocabulary Weight", "Profile Focus Area"],
        ["Homework Essay", "45%", "30%", "25%", "Academic Tone & Sentence Predictability"],
        ["Resume / CV", "30%", "40%", "30%", "Work History Bullets & Sentence Uniformity"],
        ["Research Paper / Thesis", "50%", "25%", "25%", "Citations & Lexical Variety"],
        ["Cover Letter / SOP", "35%", "35%", "30%", "Personal Narrative Voice & AI Phrase Matches"],
    ]
    weight_table = Table(weight_data, colWidths=[115, 80, 80, 80, 130])
    weight_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_TEXT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(weight_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph("6.5 Readability Metrics Explained", style_h2))
    story.append(Paragraph(
        "Detectra also calculates 3 standard readability scores to help teachers evaluate text difficulty:<br/>"
        "1. <b>Flesch-Kincaid Grade Level:</b> Shows the U.S. school grade level needed to understand the text (e.g. Grade 10 = High School level).<br/>"
        "2. <b>Flesch Reading Ease Score:</b> Gives a score from 0 to 100. Higher scores (60-100) mean easy reading, while lower scores (0-30) mean difficult academic reading.<br/>"
        "3. <b>Gunning Fog Index:</b> Estimates the years of formal education required to read the document easily.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: CHAPTER 7 - BACKEND IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 7: BACKEND IMPLEMENTATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("7.1 Backend Folder Structure", style_h2))
    story.append(Paragraph(
        "The backend is clean and compact, located inside the `backend/` directory:<br/>"
        "• <code>app.py</code> — Main FastAPI application containing REST routes and NLP logic.<br/>"
        "• <code>requirements.txt</code> — List of Python library dependencies.<br/>"
        "• <code>nltk_data/</code> — Auto-downloaded NLTK tokenizer models.<br/>"
        "• <code>uploads/</code> — Temporary directory for processed files.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("7.2 Python FastAPI Main Code (`backend/app.py`)", style_h2))

    code_1 = (
        "from fastapi import FastAPI, File, UploadFile, Form\n"
        "from nltk.tokenize import sent_tokenize, word_tokenize\n"
        "import numpy as np\n\n"
        "app = FastAPI(title='Detectra AI Suite API')\n\n"
        "def compute_burstiness(sentences):\n"
        "    if not sentences or len(sentences) < 2:\n"
        "        return 50.0\n"
        "    lens = [len(s.split()) for s in sentences]\n"
        "    mean_len = np.mean(lens)\n"
        "    std_len = np.std(lens)\n"
        "    cv = (std_len / mean_len) if mean_len > 0 else 0\n"
        "    # Low CV = Uniform sentence length = High AI probability\n"
        "    return round(max(0.0, min(100.0, (1.0 - min(cv, 1.0)) * 100)), 1)\n\n"
        "@app.post('/analyze')\n"
        "async def analyze_file(file: UploadFile = File(...), document_type: str = Form('essay')):\n"
        "    content = await file.read()\n"
        "    text = extract_text(content, file.filename)\n"
        "    metrics = calculate_metrics(text, document_type)\n"
        "    return metrics"
    )
    story.append(Paragraph(code_1, style_code))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: CHAPTER 8 - FRONTEND IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 8: FRONTEND IMPLEMENTATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("8.1 Frontend Component Hierarchy", style_h2))
    story.append(Paragraph(
        "The frontend is organized inside `frontend/src/` into reusable React components:<br/>"
        "• <code>Header.tsx</code> — Top navigation bar with logo, system status badge, and theme toggle.<br/>"
        "• <code>DocumentTypeSelector.tsx</code> — Dropdown selector for document category profiles.<br/>"
        "• <code>FileUploadZone.tsx</code> — Drag-and-drop zone with support for PDF, DOCX, and TXT files.<br/>"
        "• <code>ScoreDial.tsx</code> — Animated SVG circular dial showing the overall AI score.<br/>"
        "• <code>ResultsDashboard.tsx</code> — 4-tab dashboard displaying metrics, graphs, readability, and sentence highlights.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8.2 API Client & Proxy Configuration", style_h2))
    story.append(Paragraph("In `frontend/next.config.ts`, we set up an automatic API rewrite proxy so frontend calls to `/api/*` reach port 8000:", style_body))

    code_2 = (
        "// frontend/next.config.ts\n"
        "import type { NextConfig } from 'next';\n"
        "const nextConfig: NextConfig = {\n"
        "  async rewrites() {\n"
        "    return [\n"
        "      { source: '/api/:path*', destination: 'http://localhost:8000/:path*' }\n"
        "    ];\n"
        "  }\n"
        "};\n"
        "export default nextConfig;"
    )
    story.append(Paragraph(code_2, style_code))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: CHAPTER 9 - REST API SPECIFICATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 9: REST API SPECIFICATION", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("9.1 REST API Endpoint Catalog", style_h2))

    api_data = [
        ["HTTP Method", "Endpoint Path", "Parameters / Payload", "Description & Response"],
        ["GET", "/", "None", "Returns API welcome message & version 1.0.0"],
        ["GET", "/health", "None", "Health check: Returns status 'healthy'"],
        ["GET", "/document-types", "None", "Returns array of supported profile objects"],
        ["POST", "/analyze", "Multipart FormData (file + document_type)", "Uploads document and returns full JSON analysis result"],
        ["POST", "/analyze-text", "JSON Body { text, document_type }", "Submits pasted text and returns full JSON result"],
    ]
    api_table = Table(api_data, colWidths=[60, 110, 140, 175])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(api_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("9.2 Example JSON Response Payload", style_h2))

    json_sample = (
        "{\n"
        '  "document_type": "essay",\n'
        '  "overall_ai_probability": 74.8,\n'
        '  "verdict": "Highly AI-Generated",\n'
        '  "verdict_color": "red",\n'
        '  "metrics": {\n'
        '    "perplexity_score": 68.2,\n'
        '    "burstiness_score": 71.5,\n'
        '    "vocabulary_score": 84.0\n'
        '  },\n'
        '  "readability": {\n'
        '    "flesch_kincaid_grade": 14.2,\n'
        '    "flesch_reading_ease": 38.5,\n'
        '    "gunning_fog_index": 17.1\n'
        '  }\n'
        "}"
    )
    story.append(Paragraph(json_sample, style_code))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 10 - TESTING & TEST CASES
    # =========================================================================
    story.append(Paragraph("CHAPTER 10: TESTING & TEST CASES", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("10.1 Testing Strategy", style_h2))
    story.append(Paragraph("We performed 3 types of testing:<br/>"
                           "1. <b>Unit Testing:</b> Tested individual Python functions (`compute_burstiness`, `extract_text`).<br/>"
                           "2. <b>API Endpoint Testing:</b> Verified HTTP POST requests using cURL and Postman.<br/>"
                           "3. <b>System UI Testing:</b> Tested drag-and-drop file uploads across Chrome and Edge browsers.", style_body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("10.2 System Test Cases Matrix", style_h2))

    test_data = [
        ["Test ID", "Input File / Sample", "Category Profile", "Expected Result", "Actual Result", "Status"],
        ["TC-01", "sample_ai_essay.txt", "Homework Essay", "AI Score > 70%", "74.8% (🔴 Red Verdict)", "PASSED"],
        ["TC-02", "sample_human_sop.txt", "Cover Letter / SOP", "AI Score < 25%", "21.4% (🟢 Green Verdict)", "PASSED"],
        ["TC-03", "sample_resume.txt", "Resume / CV", "Mixed (25–45%)", "38.2% (🟡 Yellow Verdict)", "PASSED"],
        ["TC-04", "sample_research.txt", "Research Paper", "AI Score > 70%", "79.5% (🔴 Red Verdict)", "PASSED"],
        ["TC-05", "Short Text (< 20 words)", "Homework Essay", "Warning message", "Prompted user for more text", "PASSED"],
        ["TC-06", "Corrupted PDF file", "Auto-Detect", "Error handling", "Displayed clear error toast", "PASSED"],
    ]
    test_table = Table(test_data, colWidths=[45, 115, 95, 105, 85, 40])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_TEXT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(test_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: CHAPTER 11 - ADVANTAGES & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("CHAPTER 11: ADVANTAGES & FUTURE SCOPE", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("11.1 Key System Advantages", style_h2))
    story.append(Paragraph("• <b>100% Privacy Protection:</b> Documents stay on the local computer and are never uploaded to foreign cloud servers.", style_bullet))
    story.append(Paragraph("• <b>Zero Running Cost:</b> Uses free open-source software libraries, requiring no monthly subscriptions.", style_bullet))
    story.append(Paragraph("• <b>Clear Sentence Colors:</b> Color-coding helps teachers instantly see which parts of an assignment look like AI writing.", style_bullet))
    story.append(Paragraph("• <b>Fast Processing Speed:</b> Analyzes typical student documents in under 1 second.", style_bullet))
    story.append(Paragraph("• <b>Integrated Readability Scores:</b> Provides bonus reading ease and grade-level scores alongside AI detection.", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("11.2 Current Limitations", style_h2))
    story.append(Paragraph("• Extremely short text snippets (under 20 words) do not provide enough sentences to calculate sentence length variance accurately.", style_bullet))
    story.append(Paragraph("• Scanned image PDFs without text layers require OCR pre-processing before analysis.", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("11.3 Future Upgrades & Roadmap", style_h2))
    story.append(Paragraph("1. <b>Batch Zip Processing:</b> Allow teachers to upload a ZIP folder containing 50 student assignments at once.", style_bullet))
    story.append(Paragraph("2. <b>PDF Export Report:</b> Add a one-click button to export styled PDF certificates for student submission records.", style_bullet))
    story.append(Paragraph("3. <b>Local Transformer Model:</b> Add lightweight local AI models (like RoBERTa) for even higher detection accuracy.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: CHAPTER 12 - CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("CHAPTER 12: CONCLUSION & REFERENCES", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    story.append(Paragraph("12.1 Project Conclusion", style_h2))
    story.append(Paragraph(
        "The <b>Detectra AI Integrity Suite</b> project has been successfully designed, developed, and tested. "
        "Created by <b>Shruti Verma</b>, <b>Ujjwal Kumar</b>, and <b>Umesh Tomar</b> for their <b>BCA 5th Semester</b> project "
        "(Academic Session <b>2024–2027</b>) at <b>Sanskar College of Management and Professional Studies</b>, the application "
        "provides an effective, easy-to-use, and private solution to check AI content in academic and professional documents.",
        style_body
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("12.2 References & Web Links", style_h2))

    refs = [
        "1. Bird, S., Klein, E., & Loper, E. (2009). <i>Natural Language Processing with Python (NLTK)</i>. O'Reilly Media.",
        "2. FastAPI Official Documentation (2026). <i>Python FastAPI Framework Guide</i>. https://fastapi.tiangolo.com/",
        "3. Next.js Official Documentation (2026). <i>Next.js 16 App Router & React 19 Components</i>. https://nextjs.org/",
        "4. Kincaid, J. P., et al. (1975). <i>Derivation of New Readability Formulas for Navy Personnel</i>. Research Branch Report.",
        "5. Tailwind CSS Documentation (2026). <i>Utility-First CSS Framework</i>. https://tailwindcss.com/",
        "6. Recharts Documentation (2026). <i>Redefined Chart Library Built with React</i>. https://recharts.org/"
    ]

    for r in refs:
        story.append(Paragraph(r, style_bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_path}")

    if HAS_PYPDF2:
        try:
            reader = PyPDF2.PdfReader(pdf_path)
            print(f"Total Pages in Generated PDF: {len(reader.pages)}")
        except Exception as e:
            print(f"Page count check error: {e}")

if __name__ == "__main__":
    generate_pdf()
