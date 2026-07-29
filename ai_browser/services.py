import os
import re
from typing import Dict, Any, Optional, List

def extract_important_sentences(text: str, max_sentences: int = 5) -> List[str]:
    if not text:
        return []
    clean = re.sub(r'\s+', ' ', text.strip())
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean) if len(s.strip()) > 15]
    return sentences[:max_sentences]

def extract_keywords(text: str, top_n: int = 8) -> List[str]:
    if not text:
        return []
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{5,}\b', text)]
    stopwords = {'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'whatever', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves'}
    filtered = [w for w in words if w not in stopwords]
    freq: Dict[str, int] = {}
    for w in filtered:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)
    return sorted_words[:top_n]

def build_summary(title: str, content: str) -> str:
    sentences = extract_important_sentences(content, 4)
    keywords = extract_keywords(content, 5)
    summary_lines = sentences if sentences else [f"This page appears to focus on {title}."]
    return f"Summary for \"{title}\":\n\n" + "\n".join(summary_lines) + f"\n\nCore concepts: {', '.join(keywords)}."

def build_key_points(title: str, content: str) -> str:
    sentences = extract_important_sentences(content, 5)
    if not sentences:
        return f"Key points for \"{title}\":\n- Focuses on main concept of {title}."
    points = [f"- {s}" for s in sentences]
    return f"Key takeaways for \"{title}\":\n\n" + "\n".join(points)

def build_quiz(title: str, content: str) -> str:
    keywords = extract_keywords(content, 4)
    if not keywords:
        keywords = ["concept", "process", "result"]
    q1 = f"1. What is the primary focus of '{title}'?\n   A) {keywords[0].capitalize()} and related principles\n   B) Unrelated topics\n   C) Historical timeline\n   D) None of the above"
    q2 = f"2. Which of the following is a key element discussed in the text?\n   A) {keywords[1].capitalize() if len(keywords) > 1 else 'Analysis'}\n   B) Static default\n   C) Irrelevant noise\n   D) External factor"
    return f"Practice Quiz for \"{title}\":\n\n{q1}\n\n{q2}\n\n(Answer Key: 1-A, 2-A)"

def build_flashcards(title: str, content: str) -> str:
    keywords = extract_keywords(content, 4)
    cards = []
    for idx, kw in enumerate(keywords, 1):
        cards.append(f"Card {idx}:\nFront: What is {kw.capitalize()}?\nBack: A key concept highlighted in {title}.")
    if not cards:
        cards.append(f"Card 1:\nFront: Main Subject\nBack: {title}")
    return f"Flashcards for \"{title}\":\n\n" + "\n\n".join(cards)

def build_explanation(title: str, content: str) -> str:
    sentences = extract_important_sentences(content, 2)
    keywords = extract_keywords(content, 4)
    lead = sentences[0] if sentences else f"This page discusses {title}."
    return f"Explanation for \"{title}\":\n\n{lead}\n\nKey underlying topics include: {', '.join(keywords)}."

def answer_tutor_question(prompt: str, title: str = "", content: str = "", provider: str = "gemini") -> Dict[str, Any]:
    norm = prompt.lower()
    if not content and not title:
        return {
            "response": "I do not have page context yet. Please read/load a page first, then ask again.",
            "provider": provider,
            "grounded": False
        }

    if 'summary' in norm:
        resp = build_summary(title, content)
    elif 'key point' in norm or 'takeaway' in norm:
        resp = build_key_points(title, content)
    elif 'quiz' in norm:
        resp = build_quiz(title, content)
    elif 'flashcard' in norm:
        resp = build_flashcards(title, content)
    elif 'explain' in norm:
        resp = build_explanation(title, content)
    else:
        sentences = extract_important_sentences(content, 2)
        keywords = extract_keywords(content, 5)
        resp_lines = [f"Grounded answer for '{title}':\n"]
        if sentences:
            resp_lines.append(" ".join(sentences))
        if keywords:
            resp_lines.append(f"\nCore concepts: {', '.join(keywords)}.")
        resp_lines.append("\nYou can also request a summary, key points, quiz, or flashcards.")
        resp = "\n".join(resp_lines)

    return {
        "response": resp,
        "provider": provider,
        "grounded": True
    }
