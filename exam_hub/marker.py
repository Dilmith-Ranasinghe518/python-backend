import re
from typing import Dict, Any, Optional

def word_count(text: str) -> int:
    if not text:
        return 0
    words = [w for w in re.split(r'\s+', text.strip()) if w]
    return len(words)

def simple_mark(
    extracted_text: str,
    question_type: str,
    question_number: Optional[int] = None,
    paper_markdown: str = ""
) -> Dict[str, str]:
    text = (extracted_text or "").strip()
    wc = word_count(text)
    qtype = question_type.lower() if question_type else "structured"
    out_of = 20 if qtype == "structured" else 40

    if not text:
        return {
            "marks_text": f"0/{out_of}",
            "feedback": (
                f"0/{out_of}\n\n"
                "- No readable text found in the upload.\n"
                "- Upload a clearer photo (good lighting, no blur) or a PDF with selectable text.\n\n"
                "Model outline:\n"
                "- Answer the required points clearly with headings."
            )
        }

    # Heuristic scoring
    clean_markdown = re.sub(r'[^a-zA-Z0-9\s]', ' ', paper_markdown.lower())
    words = [w for w in clean_markdown.split() if len(w) >= 6]
    keywords = list(dict.fromkeys(words))[:24]

    lower_text = text.lower()
    hit = sum(1 for k in keywords if k in lower_text)

    target_words = 120 if qtype == "structured" else 220
    length_score = min(1.0, wc / target_words)
    keyword_score = (hit / len(keywords)) if keywords else 0.0
    raw = 0.25 + 0.55 * length_score + 0.20 * keyword_score
    score = max(0, min(out_of, round(raw * out_of)))

    missing = [k for k in keywords if k not in lower_text][:6]

    feedback_lines = [
        f"{score}/{out_of}",
        "",
        "- Strengths:",
        f"  - Clear writing volume: ~{wc} words.",
        f"  - Covered key terms: {hit}/{len(keywords) if keywords else 0}.",
        "",
        "- Improve:"
    ]

    if missing:
        feedback_lines.append(f"  - Try to include: {', '.join(missing)}.")
    else:
        feedback_lines.append("  - Add more specific facts and examples.")

    feedback_lines.extend([
        "  - Use short paragraphs and bullet points for clarity.",
        "",
        "Model outline:",
        "- Start with definitions / key idea",
        "- Explain the main points with examples",
        "- Conclude with a summary"
    ])

    feedback = "\n".join(feedback_lines)
    return {
        "marks_text": f"{score}/{out_of}",
        "feedback": feedback
    }
